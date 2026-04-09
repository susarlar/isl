"""
RAG System Module
=================

Complete Retrieval-Augmented Generation pipeline:
1. Top-k retrieval from vector store
2. Optional re-ranking
3. Context injection with citations
4. LLM generation with Groq
5. Guardrails and validation
"""

import sys
import os
import time
from pathlib import Path
from typing import List, Dict, Optional, Tuple
import logging

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.embeddings import EmbeddingGenerator
from app.vector_store import FAISSVectorStore
from app.chunking import Chunk
from app.prompts import (
    format_messages,
    format_citations,
    check_answer_validity,
    SYSTEM_PROMPT,
)
from config import (
    LLM_PROVIDER,
    ANTHROPIC_API_KEY,
    ANTHROPIC_MODEL,
    GROQ_API_KEY,
    GROQ_MODEL,
    TOP_K_DOCUMENTS,
    VECTOR_STORE_PATH,
    EMBEDDING_MODEL,
    set_seeds,
)

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class IsekaiRAGSystem:
    """RAG system for Isekai Slow Life game strategy queries."""

    def __init__(
        self,
        vector_db_path: str = str(VECTOR_STORE_PATH),
        model_name: Optional[str] = None,
        api_key: Optional[str] = None,
        top_k: int = TOP_K_DOCUMENTS,
        enable_reranking: bool = False,
        temperature: float = 0.1,
        max_tokens: int = 4096,
        provider: Optional[str] = None,
    ):
        """
        Initialize the RAG system.

        Args:
            vector_db_path: Path to vector database
            model_name: Model name (overrides provider default)
            api_key: API key (overrides env var)
            top_k: Number of chunks to retrieve
            enable_reranking: Whether to enable re-ranking
            temperature: LLM temperature
            max_tokens: Maximum tokens in response
            provider: 'anthropic' or 'groq' (defaults to LLM_PROVIDER env var)
        """
        self.vector_db_path = vector_db_path
        self.provider = (provider or LLM_PROVIDER).lower()
        self.top_k = top_k
        self.enable_reranking = enable_reranking
        self.temperature = temperature
        self.max_tokens = max_tokens

        # Set model and API key based on provider
        if self.provider == "anthropic":
            self.model_name = model_name or ANTHROPIC_MODEL
            self.api_key = api_key or ANTHROPIC_API_KEY or os.getenv("ANTHROPIC_API_KEY")
            if not self.api_key:
                raise ValueError("Anthropic API key not provided")
        elif self.provider == "groq":
            self.model_name = model_name or GROQ_MODEL
            self.api_key = api_key or GROQ_API_KEY or os.getenv("GROQ_API_KEY")
            if not self.api_key:
                raise ValueError("Groq API key not provided")
        else:
            raise ValueError(f"Unknown provider: {self.provider}. Use 'anthropic' or 'groq'.")

        # Initialize components
        logger.info(f"Initializing RAG system with provider: {self.provider}, model: {self.model_name}")
        self._load_components()
        logger.info("✓ RAG system ready")

    def _load_components(self):
        """Load all necessary components."""
        # Load embedding generator
        logger.info("Loading embedding model...")
        self.embedding_generator = EmbeddingGenerator(model_name=EMBEDDING_MODEL)

        # Load vector store
        logger.info(f"Loading vector database from: {self.vector_db_path}")
        self.vector_store = FAISSVectorStore(
            embedding_dimension=self.embedding_generator.embedding_dimension
        )

        index_file = Path(self.vector_db_path) / "faiss_index.bin"
        if not index_file.exists():
            logger.warning(
                "Vector database not found at %s — building now…",
                self.vector_db_path,
            )
            self._build_vector_store()
        else:
            self.vector_store.load(self.vector_db_path)

        # Initialize LLM client based on provider
        if self.provider == "anthropic":
            logger.info("Initializing Anthropic client...")
            from anthropic import Anthropic
            self.client = Anthropic(api_key=self.api_key)
        else:
            logger.info("Initializing Groq client...")
            from groq import Groq
            self.client = Groq(api_key=self.api_key)

        logger.info(f"✓ Loaded {len(self.vector_store.chunks)} chunks")

    def _build_vector_store(self):
        """Build the vector store from policy documents when no index exists."""
        from app.document_loader import load_documents
        from app.chunking import chunk_documents
        from config import CHUNK_SIZE, CHUNK_OVERLAP

        logger.info("Loading game knowledge documents…")
        documents = load_documents("knowledge")
        if not documents:
            raise RuntimeError("No knowledge documents found in knowledge/ directory.")
        logger.info("Loaded %d documents", len(documents))

        logger.info("Chunking documents…")
        chunks = chunk_documents(
            documents, chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP, strategy="hybrid"
        )
        logger.info("Created %d chunks", len(chunks))

        logger.info("Generating embeddings via Groq API…")
        embeddings = self.embedding_generator.embed_chunks(chunks, batch_size=20, show_progress=True)
        logger.info("Generated %d embeddings", len(embeddings))

        self.vector_store.add_embeddings(embeddings, chunks)
        self.vector_store.save(self.vector_db_path)
        logger.info("Vector store built and saved to %s", self.vector_db_path)

    def query(
        self, question: str, top_k: Optional[int] = None, return_metadata: bool = False
    ) -> Dict[str, any]:
        """
        Query the RAG system.

        When AGENTIC_RAG is enabled, uses a multi-stage pipeline:
          1. Retrieve a large pool of chunks (RERANKER_INITIAL_K = 50)
          2. Haiku reranks/filters to the best RERANKER_FINAL_K chunks
          3. Sonnet generates the answer from the curated chunks
          4. (Optional) Haiku critiques the answer for hallucinations

        When AGENTIC_RAG is disabled, falls back to the original single-stage
        pipeline with hybrid retrieval + direct generation.
        """
        from config import (
            AGENTIC_RAG_ENABLED, RERANKER_MODEL, RERANKER_INITIAL_K,
            RERANKER_FINAL_K, CRITIC_ENABLED,
        )

        start_time = time.time()
        k = top_k or self.top_k

        if AGENTIC_RAG_ENABLED:
            return self._query_agentic(
                question, k, return_metadata, start_time,
                RERANKER_MODEL, RERANKER_INITIAL_K, RERANKER_FINAL_K,
                CRITIC_ENABLED,
            )

        # --- Original (non-agentic) path ---
        # Step 1: Retrieve relevant chunks
        logger.info(f"Retrieving top-{k} chunks...")
        retrieved_chunks, retrieval_time = self._retrieve(question, k)

        if not retrieved_chunks:
            return {
                "answer": "I couldn't find relevant information in the game knowledge base to answer your question.",
                "sources": [],
                "confidence": 0.0,
                "retrieval_time": retrieval_time,
                "generation_time": 0.0,
                "total_time": time.time() - start_time,
            }

        # Step 2: Optional re-ranking
        if self.enable_reranking:
            logger.info("Re-ranking chunks...")
            retrieved_chunks, rerank_time = self._rerank(question, retrieved_chunks)
        else:
            rerank_time = 0.0

        # Step 3: Generate answer
        logger.info("Generating answer...")
        answer, generation_time = self._generate(question, retrieved_chunks)

        # Step 4: Validate answer
        validation = check_answer_validity(answer)

        # Step 5: Extract sources
        sources = self._extract_sources(retrieved_chunks)

        # Calculate confidence based on retrieval scores
        confidence = self._calculate_confidence(retrieved_chunks)

        # Prepare response
        response = {
            "answer": answer,
            "sources": sources,
            "confidence": confidence,
            "retrieval_time": retrieval_time,
            "generation_time": generation_time,
            "total_time": time.time() - start_time,
            "is_valid": validation["is_valid"],
            "is_refusal": validation["is_refusal"],
        }

        if return_metadata:
            response["metadata"] = {
                "chunks_retrieved": len(retrieved_chunks),
                "top_k": k,
                "model": self.model_name,
                "reranking_enabled": self.enable_reranking,
                "reranking_time": rerank_time,
                "validation": validation,
                "retrieved_chunks": [
                    {
                        "chunk_id": chunk.chunk_id,
                        "score": score,
                        "source": chunk.metadata.get("filename"),
                        "heading": chunk.metadata.get("heading"),
                        "preview": chunk.content[:100] + "...",
                    }
                    for chunk, score in retrieved_chunks
                ],
            }

        return response

    # Known proper-noun entities in the game. Dense retrieval is weak at
    # differentiating named entities, so we do a keyword fallback pass: if the
    # query mentions any of these names, we force-include chunks that mention
    # them into the retrieved set. Extends naturally as the knowledge base
    # grows — only the names that actually appear in both the query AND at
    # least one chunk will have effect, so false positives are harmless.
    _KEYWORD_ENTITIES = {
        # The 5 typings — essential for typing-scoped queries like
        # "unfettered fishing strategy" or "best brave family"
        "inspiring", "diligent", "brave", "informed", "unfettered",
        # Top-tier 120-apt UR fellows
        "amaterasu", "sunna", "master tongxuan", "tongxuan", "leon", "heracles",
        "orivita", "aegle", "neptune", "phanes", "nemetona", "andras", "ao li",
        "hermes", "freesia", "nyar", "beelzebub", "gale", "thora", "tomoe",
        "rimuru", "kerr & bel & ros", "tamamo", "phinphynx", "ixtchel",
        "athena", "nierus", "umbra", "gabrael", "kuku", "lokia", "anpu",
        # Common SSR / event fellows
        "mio", "mulberry", "crysta", "kaye", "milim nava", "iori", "salvo",
        "avril", "stephanie", "super", "mammon", "ira", "avar", "acedia",
        "lux", "mescal", "shlomo", "trady", "black", "magellan", "jewlry",
        "loya", "augustine", "bubo", "eter", "flos", "onikiri", "tigirl",
        "paat", "myner", "frogella", "thalia", "healora", "benimaru", "fafnir",
        "tohru", "elma", "kanna", "lucoa", "shiki", "emma", "mushimi",
        # SR standalone Stella fellows
        "rani", "elise", "liz", "angie",
        # Low-rarity fellows users might ask about
        "fifi", "woolf", "maxim", "pump", "belle", "prim", "nalu",
        # UR+ and other notable fellows
        "beryl", "fawna", "rudeus", "aisha greyrat",
        # Specific fish names (for fishing queries)
        "sea angel", "drakenberg monster", "goddess sponge", "sperm whale",
        "giant squid", "helicoprion", "mosasaurus", "barreleye", "pirarucu",
        "snow leopard", "narwhal", "fin whale", "axolotl", "megakarp",
        "nudibranch", "dumbo octopus", "piranhape", "megalodon",
        # UR families
        "phantanyl", "tsukuyomi", "namiko", "mors", "mia", "curren", "nirvana",
        "skogul", "usuri", "cranelia", "wadjetta", "shuna",
        # SSR families (partial — high-value ones)
        "lancelot", "hestia", "hanamiya rica", "vlad", "raphael", "thubran",
        "kagura", "futaba", "bridget", "sera", "lilith", "denier", "kosuzu",
        "lina", "baity", "bren", "lud", "alanna", "connie", "bathery", "holly",
        "phetia", "nibel", "emiru", "jin yu", "puffair", "pan pan", "penglia",
        "chitana", "lunaria", "leopolda", "devileer", "squaky", "willo",
        "sylthel", "sachiko", "sylphiette", "mercuria", "loo",
    }

    # Common typos and short-form aliases → canonical entity name.
    # When an alias is found in the query, we look for chunks containing the
    # canonical form (not the alias). This lets queries like "Belzebub main
    # strategy" or "Amateratsu fish" still boost the right chunks.
    _KEYWORD_ALIASES = {
        # Beelzebub variants
        "belzebub": "beelzebub",
        "beelzebul": "beelzebub",
        "beelzebup": "beelzebub",
        "belzebuth": "beelzebub",
        # Amaterasu variants
        "amateratsu": "amaterasu",
        "amaterazu": "amaterasu",
        "ameterasu": "amaterasu",
        # Orivita variants
        "oravita": "orivita",
        "orivitta": "orivita",
        "orvita": "orivita",
        # Master Tongxuan short form
        "tongxuan": "master tongxuan",
        "tong xuan": "master tongxuan",
        "master tong": "master tongxuan",
        # Other common typos
        "nemetonia": "nemetona",
        "fanes": "phanes",
        "ixchel": "ixtchel",
        "ictchel": "ixtchel",
        "neptnune": "neptune",
        # Star notation: docs use unicode "6★" but users type "6-star" / "6 star"
        "6-star": "6★",
        "6 star": "6★",
        "6star": "6★",
        "5-star": "5★",
        "5 star": "5★",
        "5star": "5★",
        "4-star": "4★",
        "4 star": "4★",
        "4star": "4★",
        "3-star": "3★",
        "3 star": "3★",
        "3star": "3★",
        # Awakening phrasing — user types "awakening" but doc sections often
        # use "Acquaint Stone" or "Awakening Gate". Map as aliases so both
        # types of query boost the right chunks.
        "awakening gate": "awakening gate",
        "awaken fellow": "awakening",
        "awakening requirement": "acquaint stone",
    }

    # Domain concepts (not named entities) that should trigger keyword boost
    # when present in the query. Covers EVERY game system so no domain-specific
    # query hits zero keyword matches.
    #
    # WARNING: Do NOT add phrases that appear many times in table-heavy chunks
    # (e.g., "fellow power" appears dozens of times in fishing.md fish tables).
    # Over-broad keywords cause scoring saturation. Keep phrases specific
    # enough that they identify the actual topic.
    #
    # SYSTEMATIC COVERAGE (every game system represented):
    _KEYWORD_DOMAIN_PHRASES = {
        # --- Stella groups & patterns ---
        "empyrean sound", "ancient magi", "divine gospel",
        "family stella", "fellow stella", "stella level", "pattern a",
        "pattern b", "pattern c", "pattern d", "category stella",
        # --- Aptitude / talent system ---
        "supreme talent", "outstanding talent", "ordinary talent",
        "aptitude slot", "aptitude cap", "level cap",
        "skill pearl",
        "insight", "alraune", "proficiency",
        "bazaar scroll", "farm point",
        # --- Awakening system ---
        "acquaint stone", "sub-fellow", "star gate", "awakening gate",
        "4-star", "5-star", "6-star", "4 star", "5 star", "6 star",
        "limit break",
        # --- Fishing system ---
        "fish tank", "advanced bait", "normal bait", "bait production",
        "gold crown", "fish skill",
        # --- Family / blessing / dating ---
        "family blessing", "fellow blessing", "advanced blessing",
        "blessing point", "plane ticket", "succubus tonic", "crystal travel",
        "bond", "student rarity", "field trip", "date point",
        # --- Artifact system ---
        "artifact", "materia", "magic ore", "quenching stone",
        "reforge oil", "breakthrough materia", "magic lamp", "kanna plush",
        # --- Costume system ---
        "costume", "fellow costume", "family costume", "costume essence",
        "costume shop", "quintessence",
        # --- Building / village system ---
        "village earning", "building earning", "family earning",
        "service level", "building training", "building upgrade",
        "blueprint", "hire card", "study note",
        # --- Museum system ---
        "museum antique", "museum coin", "museum card", "museum trophy",
        "excavation", "glory road",
        # --- Pearl currencies ---
        "white pearl", "black pearl",
        # --- Siege / PvP ---
        "siege", "trade post", "negotiation",
        # --- Other power sources ---
        "resonance power", "compendium", "scrapbook",
        "figure", "user avatar",
        "familiar", "familiar tower",
        "expo",
        "roaming", "bazaar", "fame",
        # --- Economy ---
        "power formula", "vip",
    }

    # Triggers that indicate the query is about maximizing / improving /
    # optimizing fellow power OR asking for a strategy / priority / action.
    # When any of these appear in the query, we run multi-domain expansion
    # retrieval to pull in chunks from every power source (fish, family,
    # aptitude, artifacts, etc.) even if the query doesn't mention those
    # domains explicitly.
    _POWER_QUERY_TRIGGERS = {
        # Power optimization intents
        "most power", "max power", "maximum power", "optimize", "optimise",
        "improve", "increase power", "boost", "biggest", "best way",
        "push power", "maximize", "maximise", "stronger", "strongest",
        "fellow power", "main carry", "action plan",
        "how to power", "how do i", "how do you", "help me improve",
        # Strategy / planning / priority intents (broader)
        "strategy", "what should", "what next", "where should", "what to do",
        "priority", "prioritize", "prioritise", "spending", "invest", "spend",
        "recommend", "suggestion", "advice", "plan", "focus on",
        "best for", "good for", "worth it", "what fish", "which fish",
    }

    # Canonical sub-queries to run when a power-optimization intent is
    # detected. Each pulls a different domain, ensuring the LLM sees content
    # from every major power source regardless of the original query's
    # semantic anchor.
    _POWER_DOMAIN_SUBQUERIES = [
        # Aptitude system — split into two sub-queries so the round-robin
        # guarantees both the talent tier overview AND the slot detail
        "supreme talent outstanding talent ordinary talent skill pearl tier cap 300 900",
        "aptitude slot insight books alraune essence bazaar scroll proficiency limit break",
        # Fish
        "fish tank percent power fish skills ocean top category typing",
        # Family
        "family stella blessing power aptitude to blessed fellow",
        # Artifacts — 3 sub-queries covering tier/awakening/materia
        "artifact tier hierarchy UR+ support echo magic lamp kanna plush equip",
        "materia leveling breakthrough refine magic ore artifact level 70 40",
        "reforge oils skill slots artifact awakening quenching stone cap",
        # Awakening
        "awakening stars gates limit break aptitude slot acquaint stone",
        # Costume
        "costume essence typing boost fellow power family costume",
        # Buildings
        "building service level training employee gold earning typing",
        # Formula / additive
        "fellow power formula aptitude multiplier additive percentage flat",
        # Museum
        "museum antique trophy per typing oyster narwhal sledge",
        # Items / consumables
        "item consumable flat power bonus main carry event reward",
        # Pearls (white / black / skill — all three)
        "white pearl black pearl bait production aptitude fellow power account boost",
    ]

    def _retrieve(
        self, question: str, k: int
    ) -> Tuple[List[Tuple[Chunk, float]], float]:
        """
        Retrieve top-k relevant chunks using hybrid dense + keyword search
        with domain expansion for power-optimization queries.

        Three-stage retrieval:
        1. Dense retrieval on the original query (captures user intent)
        2. Keyword match pass for named entities (Sunna, Hermes, etc.)
        3. For power-optimization intents, multi-query retrieval across
           every power domain (fish, family, aptitude, artifacts, awakening,
           buildings, costumes) so the LLM sees content from all major
           power sources, not just whichever one best matched the query.
        """
        start_time = time.time()

        # Step 1: Dense retrieval on the original query
        query_embedding = self.embedding_generator.embed_query(question)
        dense_k = max(k * 2, 20)
        dense_results = self.vector_store.search(query_embedding, k=dense_k)

        # Step 2: Keyword-match pass for named entities.
        # We find entities in the query via (a) direct substring match on
        # canonical names, (b) alias resolution for common typos, and
        # (c) multi-word domain phrases.
        question_lower = question.lower()

        # Direct canonical matches
        mentioned_entities = {
            name for name in self._KEYWORD_ENTITIES
            if name in question_lower
        }

        # Alias → canonical mapping for typos / short forms
        for alias, canonical in self._KEYWORD_ALIASES.items():
            if alias in question_lower:
                mentioned_entities.add(canonical)

        # Domain phrases (e.g., "empyrean sound", "skill pearl")
        for phrase in self._KEYWORD_DOMAIN_PHRASES:
            if phrase in question_lower:
                mentioned_entities.add(phrase)

        keyword_results: List[Tuple[Chunk, float]] = []
        if mentioned_entities:
            logger.info(f"Query mentions entities: {sorted(mentioned_entities)}")
            for chunk in self.vector_store.chunks:
                chunk_lower = chunk.content.lower()
                # Score = distinct entity hits + occurrence density.
                # distinct_hits counts how many different mentioned entities
                # the chunk contains. occurrence_hits counts total mentions
                # (so a fish table with "Unfettered" repeated 10 times beats
                # a generic chunk with "unfettered" once).
                distinct_hits = sum(1 for name in mentioned_entities if name in chunk_lower)
                if distinct_hits == 0:
                    continue
                occurrence_hits = sum(chunk_lower.count(name) for name in mentioned_entities)
                # Base 0.55 for any distinct hit, +0.05 per distinct entity above 1,
                # +0.02 per additional occurrence above distinct count, capped at 0.85.
                keyword_score = min(
                    0.55
                    + 0.05 * (distinct_hits - 1)
                    + 0.02 * (occurrence_hits - distinct_hits),
                    0.85,
                )
                keyword_results.append((chunk, keyword_score))
            keyword_results.sort(key=lambda x: x[1], reverse=True)
            keyword_results = keyword_results[:dense_k]

        # Step 3: Domain expansion for power-optimization queries
        # This is the key fix: for "how to maximize power for X" type
        # queries, we also retrieve from every power-source domain so the
        # LLM sees fish/family/artifacts/etc. content even though the
        # original query's embedding doesn't match those domains directly.
        is_power_query = any(trigger in question_lower for trigger in self._POWER_QUERY_TRIGGERS)
        domain_results: List[Tuple[Chunk, float]] = []
        if is_power_query:
            logger.info("Power-optimization intent detected — expanding to domain sub-queries")
            per_domain_k = 3  # top 3 chunks per domain sub-query

            # Round-robin: guarantee at least 1 chunk from EACH sub-query
            # makes it into domain_results with a high enough score to
            # survive the quota merge. Without this, 13 sub-queries compete
            # for ~6-7 domain quota slots and 6-7 domains get zero
            # representation (the Nierus/Informed query had 0 chunks for
            # supreme talent, black pearl, building service level, items).
            domain_round_robin: List[Tuple[Chunk, float]] = []
            domain_overflow: List[Tuple[Chunk, float]] = []

            for subquery in self._POWER_DOMAIN_SUBQUERIES:
                sub_emb = self.embedding_generator.embed_query(subquery)
                sub_results = self.vector_store.search(sub_emb, k=per_domain_k)
                for rank, (chunk, score) in enumerate(sub_results):
                    adjusted = 0.5 + float(score) * 0.2
                    if rank == 0:
                        # First result per sub-query gets a guaranteed slot
                        # with a higher base score to survive the merge
                        domain_round_robin.append((chunk, adjusted + 0.1))
                    else:
                        domain_overflow.append((chunk, adjusted))

            # Combine: round-robin first (1 per domain), then overflow
            domain_results = domain_round_robin + domain_overflow

        # Quota-based merge: reserve slots per retrieval source so that both
        # domain coverage (fish, family, aptitude, etc.) AND named-entity
        # specificity (Sunna, Hermes, etc.) are guaranteed in the final set.
        # Without quotas, whichever source scores highest would crowd out
        # the others — e.g., domain expansion would push out Sunna-specific
        # chunks because domain scores end up higher than keyword-boost scores.
        final_results: List[Tuple[Chunk, float]] = []
        used_ids: set[str] = set()

        def _add_unique(src_results: List[Tuple[Chunk, float]], quota: int):
            added = 0
            for chunk, score in src_results:
                if added >= quota:
                    break
                if chunk.chunk_id not in used_ids:
                    final_results.append((chunk, float(score)))
                    used_ids.add(chunk.chunk_id)
                    added += 1

        # Number of domain sub-queries determines how many round-robin
        # slots we need to guarantee full coverage.
        n_domains = len(self._POWER_DOMAIN_SUBQUERIES) if is_power_query else 0

        if mentioned_entities and is_power_query:
            # Both named entity AND power optimization → need all three.
            # With k=22 and 13 domains: ~8 keyword + 13 domain + 1 dense
            # (domain round-robin guarantees 1 per sub-query)
            keyword_quota = max(k - n_domains - 1, 4)
            domain_quota = n_domains + 1  # round-robin + 1 overflow
            dense_quota = max(k - keyword_quota - domain_quota, 1)
            _add_unique(keyword_results, keyword_quota)
            _add_unique(domain_results, domain_quota)
            _add_unique(dense_results, dense_quota)
        elif mentioned_entities:
            # Named entity query, no power intent
            keyword_quota = int(k * 0.65)
            dense_quota = k - keyword_quota
            _add_unique(keyword_results, keyword_quota)
            _add_unique(dense_results, dense_quota)
        elif is_power_query:
            # Power optimization without a specific fellow
            domain_quota = n_domains + 2
            dense_quota = k - domain_quota
            _add_unique(domain_results, domain_quota)
            _add_unique(dense_results, dense_quota)
        else:
            # Normal query — dense retrieval only, no quotas needed
            _add_unique(dense_results, k)

        # If quotas under-filled (e.g., not enough keyword chunks existed),
        # top up from the highest-scoring remaining chunks across all sources
        if len(final_results) < k:
            all_candidates: Dict[str, Tuple[Chunk, float]] = {}
            for chunk, score in dense_results + keyword_results + domain_results:
                if chunk.chunk_id in used_ids:
                    continue
                existing = all_candidates.get(chunk.chunk_id)
                if existing is None or float(score) > existing[1]:
                    all_candidates[chunk.chunk_id] = (chunk, float(score))
            leftover = sorted(all_candidates.values(), key=lambda x: x[1], reverse=True)
            for chunk, score in leftover[: k - len(final_results)]:
                final_results.append((chunk, score))
                used_ids.add(chunk.chunk_id)

        retrieval_time = time.time() - start_time

        logger.info(
            f"✓ Hybrid retrieval: {len(dense_results)} dense + "
            f"{len(keyword_results)} keyword + {len(domain_results)} domain → "
            f"{len(final_results)} merged in {retrieval_time:.3f}s"
        )
        if final_results:
            logger.info(f"  Top score: {final_results[0][1]:.4f}")

        return final_results, retrieval_time

    def _rerank(
        self, question: str, chunks_with_scores: List[Tuple[Chunk, float]]
    ) -> Tuple[List[Tuple[Chunk, float]], float]:
        """
        Re-rank retrieved chunks using LLM.

        This is an optional step that can improve result quality.
        """
        start_time = time.time()

        # Simple re-ranking based on keyword matching
        # (For production, consider using a cross-encoder model)

        question_lower = question.lower()
        question_keywords = set(question_lower.split())

        reranked = []
        for chunk, score in chunks_with_scores:
            # Calculate keyword overlap
            chunk_lower = chunk.content.lower()
            chunk_keywords = set(chunk_lower.split())

            overlap = len(question_keywords & chunk_keywords)
            keyword_score = overlap / max(len(question_keywords), 1)

            # Combine with original score (70% original, 30% keywords)
            combined_score = 0.7 * score + 0.3 * keyword_score

            reranked.append((chunk, combined_score))

        # Sort by combined score
        reranked.sort(key=lambda x: x[1], reverse=True)

        rerank_time = time.time() - start_time
        logger.info(f"✓ Re-ranked chunks in {rerank_time:.3f}s")

        return reranked, rerank_time

    def _generate(
        self, question: str, chunks_with_scores: List[Tuple[Chunk, float]]
    ) -> Tuple[str, float]:
        """Generate answer using the configured LLM provider."""
        start_time = time.time()

        # Extract just the chunks
        chunks = [chunk for chunk, score in chunks_with_scores]

        # Format messages (returns OpenAI/Groq-style with system in messages array)
        messages = format_messages(question, chunks, max_chunks=self.top_k)

        try:
            if self.provider == "anthropic":
                # Anthropic Messages API: separate system from user/assistant messages
                system_msg = next((m["content"] for m in messages if m["role"] == "system"), "")
                user_messages = [m for m in messages if m["role"] != "system"]

                response = self.client.messages.create(
                    model=self.model_name,
                    system=system_msg,
                    messages=user_messages,
                    temperature=self.temperature,
                    max_tokens=self.max_tokens,
                )
                answer = response.content[0].text.strip()
            else:
                # Groq / OpenAI-compatible API
                response = self.client.chat.completions.create(
                    model=self.model_name,
                    messages=messages,
                    temperature=self.temperature,
                    max_tokens=self.max_tokens,
                    top_p=0.95,
                    stream=False,
                )
                answer = response.choices[0].message.content.strip()

            generation_time = time.time() - start_time

            logger.info(f"✓ Generated answer in {generation_time:.3f}s")
            logger.info(f"  Answer length: {len(answer)} characters")

            return answer, generation_time

        except Exception as e:
            logger.error(f"Error generating answer: {e}")
            return f"Error generating answer: {str(e)}", time.time() - start_time

    # ===================================================================
    # Agentic RAG Pipeline
    # ===================================================================

    def _query_agentic(
        self, question, k, return_metadata, start_time,
        reranker_model, initial_k, final_k, critic_enabled,
    ):
        """
        Multi-stage agentic pipeline:
        1. Retrieve large pool (initial_k chunks)
        2. Haiku reranks to best final_k
        3. Sonnet generates answer
        4. Haiku critiques (optional)
        """
        from anthropic import Anthropic

        # Stage 1: Wide retrieval
        logger.info(f"[Agentic] Stage 1: Retrieving top-{initial_k} chunks...")
        all_chunks, retrieval_time = self._retrieve(question, initial_k)

        if not all_chunks:
            return {
                "answer": "I couldn't find relevant information in the game knowledge base.",
                "sources": [], "confidence": 0.0,
                "retrieval_time": retrieval_time, "generation_time": 0.0,
                "total_time": time.time() - start_time,
            }

        # Stage 2: Haiku reranker — reads all chunks and selects the best ones
        logger.info(f"[Agentic] Stage 2: Haiku reranking {len(all_chunks)} → {final_k}...")
        reranker_client = Anthropic(api_key=self.api_key)

        # Format chunks for Haiku with numbered IDs
        chunk_listing = ""
        for i, (chunk, score) in enumerate(all_chunks):
            source = chunk.metadata.get("filename", "?")
            heading = chunk.metadata.get("heading", "") or ""
            preview = chunk.content[:400]
            chunk_listing += f"\n---\n[CHUNK {i}] source={source} heading=\"{heading}\"\n{preview}\n"

        rerank_prompt = f"""You are a relevance filter for a game knowledge RAG system.

QUESTION: {question}

Below are {len(all_chunks)} retrieved chunks. Select the {final_k} MOST RELEVANT chunks
for answering this question comprehensively. Consider:
- Does the chunk directly address the question's topic?
- Does it contain specific numbers, formulas, or mechanics the answer needs?
- Does it cover a power domain (fish, family, artifacts, stella, aptitude, costumes,
  buildings, museum, pearls, awakening) that a comprehensive answer should include?
- Prefer chunks with SPECIFIC DATA over generic overviews.

CHUNKS:
{chunk_listing}

Return ONLY a JSON array of the chunk numbers you selected, in order of relevance.
Example: [3, 7, 0, 15, 22, 8, 1, 12, 5, 9, 14, 6, 11, 4, 10]

Selected chunks (JSON array):"""

        try:
            t0 = time.time()
            rerank_response = reranker_client.messages.create(
                model=reranker_model,
                system="You are a retrieval reranker. Return only a JSON array of chunk numbers. No explanation.",
                messages=[{"role": "user", "content": rerank_prompt}],
                max_tokens=200,
                temperature=0,
            )
            rerank_text = rerank_response.content[0].text.strip()
            rerank_time = time.time() - t0
            logger.info(f"[Agentic] Haiku rerank completed in {rerank_time:.2f}s")

            # Parse the JSON array
            import json
            # Handle cases where Haiku wraps in markdown code blocks
            if "```" in rerank_text:
                rerank_text = rerank_text.split("```")[1].strip()
                if rerank_text.startswith("json"):
                    rerank_text = rerank_text[4:].strip()
            selected_ids = json.loads(rerank_text)

            # Map back to chunks
            curated_chunks = []
            for idx in selected_ids[:final_k]:
                if 0 <= idx < len(all_chunks):
                    curated_chunks.append(all_chunks[idx])

            if not curated_chunks:
                logger.warning("[Agentic] Reranker returned no valid chunks, falling back to top-k")
                curated_chunks = all_chunks[:final_k]

            logger.info(f"[Agentic] Curated {len(curated_chunks)} chunks from {len(all_chunks)}")

        except Exception as e:
            logger.error(f"[Agentic] Reranker failed: {e}, falling back to top-k")
            curated_chunks = all_chunks[:final_k]
            rerank_time = 0.0

        # Stage 3: Sonnet generates the answer from curated chunks
        logger.info("[Agentic] Stage 3: Sonnet generating answer...")
        answer, generation_time = self._generate(question, curated_chunks)

        # Stage 4: Haiku critic (optional)
        critic_feedback = None
        if critic_enabled:
            logger.info("[Agentic] Stage 4: Haiku critiquing answer...")
            try:
                t0 = time.time()
                critic_response = reranker_client.messages.create(
                    model=reranker_model,
                    system="You are a quality checker for a game advisor bot. Be concise.",
                    messages=[{"role": "user", "content": f"""Review this answer for quality issues.

QUESTION: {question}

ANSWER:
{answer[:3000]}

Check for:
1. Does it say "stacks multiplicatively" or "compound exponentially" about % bonuses? (WRONG — they're additive)
2. Does it recommend Neptune as a main carry without warning? (WRONG — Neptune is not recommended)
3. Does it claim Fifi/Woolf/N-rarity fellows can have Stella? (WRONG — only SSR+ and 4 named SRs)
4. Does it say "I don't have information" about something that's actually in the answer? (CONTRADICTION)
5. Does it cover multiple power domains or is it narrowly focused on just 1-2?
6. Does it use specific numbers from the game data or just give vague advice?

If the answer is GOOD, respond with exactly: PASS
If there are issues, respond with: FAIL followed by a brief list of problems."""}],
                    max_tokens=300,
                    temperature=0,
                )
                critic_text = critic_response.content[0].text.strip()
                critic_time = time.time() - t0
                logger.info(f"[Agentic] Critic verdict: {critic_text[:50]}... ({critic_time:.2f}s)")

                if critic_text.startswith("FAIL"):
                    critic_feedback = critic_text
                    logger.warning(f"[Agentic] Critic flagged issues — re-prompting Sonnet")

                    # Re-prompt Sonnet with critique feedback
                    retry_question = (
                        f"{question}\n\n"
                        f"[SELF-CRITIQUE FEEDBACK — your previous answer had these issues:\n"
                        f"{critic_text}\n"
                        f"Please fix these issues in your revised answer.]"
                    )
                    answer, retry_time = self._generate(retry_question, curated_chunks)
                    generation_time += retry_time
                    logger.info(f"[Agentic] Sonnet revised answer in {retry_time:.2f}s")

            except Exception as e:
                logger.error(f"[Agentic] Critic failed: {e}, using original answer")

        # Validate + extract sources
        validation = check_answer_validity(answer)
        sources = self._extract_sources(curated_chunks)
        confidence = self._calculate_confidence(curated_chunks)

        response = {
            "answer": answer,
            "sources": sources,
            "confidence": confidence,
            "retrieval_time": retrieval_time,
            "generation_time": generation_time,
            "total_time": time.time() - start_time,
            "is_valid": validation["is_valid"],
            "is_refusal": validation["is_refusal"],
            "agentic": True,
            "chunks_retrieved": len(all_chunks),
            "chunks_curated": len(curated_chunks),
            "critic_feedback": critic_feedback,
        }

        if return_metadata:
            response["metadata"] = {
                "chunks_retrieved": len(all_chunks),
                "chunks_curated": len(curated_chunks),
                "top_k": initial_k,
                "final_k": final_k,
                "model": self.model_name,
                "reranker_model": reranker_model,
                "critic_enabled": critic_enabled,
                "critic_feedback": critic_feedback,
                "reranking_enabled": True,
                "reranking_time": rerank_time,
                "validation": validation,
                "retrieved_chunks": [
                    {
                        "chunk_id": chunk.chunk_id,
                        "score": score,
                        "source": chunk.metadata.get("filename"),
                        "heading": chunk.metadata.get("heading"),
                        "preview": chunk.content[:100] + "...",
                    }
                    for chunk, score in curated_chunks
                ],
            }

        return response

    def _extract_sources(
        self, chunks_with_scores: List[Tuple[Chunk, float]]
    ) -> List[Dict]:
        """Extract source information from chunks."""
        sources = []
        seen_sources = set()

        for chunk, score in chunks_with_scores:
            source_file = chunk.metadata.get("filename", "unknown.md")

            if source_file not in seen_sources:
                sources.append(
                    {
                        "filename": source_file,
                        "title": chunk.metadata.get("title", "Unknown Document"),
                        "score": float(score),
                        "chunk_id": chunk.chunk_id,
                    }
                )
                seen_sources.add(source_file)

        return sources

    def _calculate_confidence(
        self, chunks_with_scores: List[Tuple[Chunk, float]]
    ) -> float:
        """Calculate confidence score based on retrieval scores."""
        if not chunks_with_scores:
            return 0.0

        # Use top score as primary confidence indicator
        top_score = chunks_with_scores[0][1]

        # Consider score distribution (are multiple chunks relevant?)
        if len(chunks_with_scores) > 1:
            avg_top_3 = sum(score for _, score in chunks_with_scores[:3]) / min(
                3, len(chunks_with_scores)
            )
            confidence = 0.7 * top_score + 0.3 * avg_top_3
        else:
            confidence = top_score

        return float(min(confidence, 1.0))

    def stream_query(self, question: str, top_k: Optional[int] = None):
        """
        Query the RAG system with streaming response.

        Args:
            question: User's question
            top_k: Number of chunks to retrieve

        Yields:
            Chunks of the answer as they are generated
        """
        k = top_k or self.top_k

        # Retrieve chunks
        retrieved_chunks, _ = self._retrieve(question, k)

        if not retrieved_chunks:
            yield "I couldn't find relevant information in the game knowledge base to answer your question."
            return

        # Extract just the chunks
        chunks = [chunk for chunk, score in retrieved_chunks]

        # Format messages
        messages = format_messages(question, chunks, max_chunks=self.top_k)

        try:
            if self.provider == "anthropic":
                # Anthropic streaming
                system_msg = next((m["content"] for m in messages if m["role"] == "system"), "")
                user_messages = [m for m in messages if m["role"] != "system"]

                with self.client.messages.stream(
                    model=self.model_name,
                    system=system_msg,
                    messages=user_messages,
                    temperature=self.temperature,
                    max_tokens=self.max_tokens,
                ) as stream:
                    for text in stream.text_stream:
                        yield text
                return

            # Groq / OpenAI-compatible streaming
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=messages,
                temperature=self.temperature,
                max_tokens=self.max_tokens,
                top_p=0.95,
                stream=True,
            )

            for chunk in response:
                if chunk.choices[0].delta.content:
                    yield chunk.choices[0].delta.content

        except Exception as e:
            logger.error(f"Error in streaming: {e}")
            yield f"\n\nError: {str(e)}"

    def get_stats(self) -> Dict:
        """Get statistics about the RAG system."""
        store_stats = self.vector_store.get_stats()

        return {
            "model": self.model_name,
            "top_k": self.top_k,
            "reranking_enabled": self.enable_reranking,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
            "vector_store": store_stats,
            "embedding_model": EMBEDDING_MODEL,
            "embedding_dimension": self.embedding_generator.embedding_dimension,
        }


if __name__ == "__main__":
    # Test the RAG system
    print("=" * 70)
    print("RAG System Test")
    print("=" * 70)
    print()

    # Initialize RAG system
    try:
        rag = IsekaiRAGSystem()

        # Show stats
        print("System Statistics:")
        print("-" * 70)
        stats = rag.get_stats()
        for key, value in stats.items():
            if isinstance(value, dict):
                print(f"\n{key}:")
                for k, v in value.items():
                    print(f"  {k}: {v}")
            else:
                print(f"{key}: {value}")

        # Test queries
        print("\n\n" + "=" * 70)
        print("Test Queries")
        print("=" * 70)

        test_questions = [
            "What is the remote work policy?",
            "How many days of PTO do employees get?",
            "What is the speed of light?",  # Out of corpus
        ]

        for i, question in enumerate(test_questions, 1):
            print(f"\n\nQuery {i}: {question}")
            print("-" * 70)

            result = rag.query(question, return_metadata=True)

            print(f"\nAnswer:")
            print(result["answer"])

            print(f"\nSources:")
            for source in result["sources"]:
                print(
                    f"  - {source['title']} ({source['filename']}) [score: {source['score']:.4f}]"
                )

            print(f"\nMetrics:")
            print(f"  Confidence: {result['confidence']:.4f}")
            print(f"  Retrieval time: {result['retrieval_time']:.3f}s")
            print(f"  Generation time: {result['generation_time']:.3f}s")
            print(f"  Total time: {result['total_time']:.3f}s")
            print(f"  Valid: {result['is_valid']}")
            print(f"  Refusal: {result['is_refusal']}")

        print("\n" + "=" * 70)
        print("✓ RAG system test complete!")
        print("=" * 70)

    except FileNotFoundError as e:
        print(f"\n⚠️  {e}")
        print("\nPlease build the vector database first:")
        print("  python scripts/build_vector_db.py")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback

        traceback.print_exc()
