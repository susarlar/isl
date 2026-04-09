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
        max_tokens: int = 3000,
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

        Args:
            question: User's question
            top_k: Number of chunks to retrieve (overrides default)
            return_metadata: Whether to return detailed metadata

        Returns:
            Dictionary with answer, sources, and optional metadata
        """
        start_time = time.time()
        k = top_k or self.top_k

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
        "aptitude skill pearls supreme talent insight alraune bazaar scroll",
        "fish tank percent power fish skills ocean top category",
        "family stella blessing power aptitude to blessed fellow",
        "artifacts awakening quenching stone materia oils reforge",
        "awakening stars gates limit break aptitude slot",
        "costume essence typing boost fellow power",
        "building service level training diligent inspiring brave informed unfettered",
        "fellow power formula aptitude multiplier sigma percent flat",
        "museum antique trophy per typing",
        "item consumable flat power bonus main carry",
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

        # Step 2: Keyword-match pass for named entities
        question_lower = question.lower()
        mentioned_entities = {
            name for name in self._KEYWORD_ENTITIES
            if name in question_lower
        }

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
            per_domain_k = 3  # top 3 chunks per domain
            for subquery in self._POWER_DOMAIN_SUBQUERIES:
                sub_emb = self.embedding_generator.embed_query(subquery)
                sub_results = self.vector_store.search(sub_emb, k=per_domain_k)
                # Score domain chunks at ~0.5 so they participate in the
                # merge without dominating. The domain expansion is a safety
                # net to ensure coverage, not a replacement for primary search.
                for chunk, score in sub_results:
                    domain_results.append((chunk, 0.5 + float(score) * 0.2))

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

        if mentioned_entities and is_power_query:
            # Both named entity AND power optimization → reserve slots for each
            # k=18 typical split: 8 keyword + 6 domain + 4 dense
            keyword_quota = max(k // 2, 1)
            domain_quota = max(k // 3, 1)
            dense_quota = k - keyword_quota - domain_quota
            _add_unique(keyword_results, keyword_quota)
            _add_unique(domain_results, domain_quota)
            _add_unique(dense_results, dense_quota)
        elif mentioned_entities:
            # Named entity query, no power intent
            # k=18 typical split: 12 keyword + 6 dense
            keyword_quota = int(k * 0.65)
            dense_quota = k - keyword_quota
            _add_unique(keyword_results, keyword_quota)
            _add_unique(dense_results, dense_quota)
        elif is_power_query:
            # Power optimization without a specific fellow
            # k=18 typical split: 10 domain + 8 dense
            domain_quota = int(k * 0.55)
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
