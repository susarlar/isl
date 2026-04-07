# Design & Evaluation Document

## 1. System Architecture

```
User Question
     │
     ▼
Flask Web App  (app/web_app.py)
     │
     ▼
PolicyRAGSystem  (app/rag_system.py)
     │                    │
     ▼                    ▼
FAISS Vector Store    Groq LLM API
(app/vector_store.py) (cloud inference)
     │
     ▼
Sentence-Transformer Embeddings
(app/embeddings.py)
     │
     ▼
Policy Document Corpus  (policies/*.md)
```

---

## 2. Design Decisions

### 2.1 Embedding Model — `sentence-transformers/all-MiniLM-L6-v2`

**Choice:** `all-MiniLM-L6-v2` (384-dimensional, ~22 M parameters)

**Why:**
- Runs entirely locally — no external embedding API needed, no cost, no latency overhead
- Fast enough for batch indexing (659 chunks in < 30 s on CPU)
- 384-dimensional vectors keep the FAISS index small (~1 MB)
- Well-benchmarked on semantic similarity tasks, outperforms bag-of-words approaches
- Free, open-source (Apache 2.0 licence)

**Trade-offs considered:**
- Larger models (`all-mpnet-base-v2`, 768-dim) give ~2% better quality but are 2× slower and larger
- Cloud embedding APIs (Cohere, Voyage) would add network latency and cost
- For a policy corpus of < 1 M tokens the smaller model is sufficient

---

### 2.2 Chunking Strategy — Hybrid (headings + token windows)

**Choice:** `strategy=hybrid` — split on `##` headings first, then apply a 1 000-character
token-window with 200-character overlap within each section.

**Why:**
- Policy documents are well-structured markdown; heading-based splits preserve semantic units
- Token-window overlap prevents important sentences from being cut across chunk boundaries
- Overlap of 20% (200/1 000) is a standard RAG best practice; too little loses context,
  too much inflates the index
- Fixed seed (42) makes chunking deterministic and reproducible

**Parameters:**
| Parameter | Value | Rationale |
|---|---|---|
| `CHUNK_SIZE` | 1 000 chars | Fits comfortably in LLM context window; covers ~200 words |
| `CHUNK_OVERLAP` | 200 chars | 20% overlap; sufficient for sentence continuity |
| `MAX_CHUNKS_PER_DOC` | 100 | Safety cap; no single document should dominate the index |

---

### 2.3 Vector Store — FAISS (Flat/Cosine)

**Choice:** `faiss-cpu` with Flat index (exact exhaustive search), cosine similarity.

**Why:**
- 659 chunks is a small corpus; approximate nearest-neighbour indexes (IVF, HNSW) add
  complexity with no measurable speed benefit at this scale
- Exact search guarantees best possible retrieval recall
- FAISS is battle-tested, runs locally (no cloud dependency), and the index is a single
  binary file that can be committed to git
- Cosine similarity is preferred over L2 for normalised sentence embeddings

**Alternative considered:** ChromaDB — adds persistence and metadata filtering, but
introduces another process dependency and is unnecessary at this scale.

---

### 2.4 Retrieval — Top-k = 5

**Choice:** Retrieve `k=5` chunks per query.

**Why:**
- Empirically, 3–7 chunks cover most single-topic policy questions without exceeding
  the LLM context window
- k=5 gives ~5 000 characters of context (5 × 1 000), well within the 32 K-token window
  of `llama-3.1-70b-versatile`
- Optional keyword re-ranking (disabled by default) can improve ordering when enabled

---

### 2.5 LLM — Groq / `llama-3.1-70b-versatile`

**Choice:** Groq hosted `llama-3.1-70b-versatile` (or `openai/gpt-oss-120b` as alternative).

**Why:**
- Groq provides free-tier API access with low latency (~1–2 s for 1 024-token responses)
- `llama-3.1-70b-versatile` is an excellent open-weight model for instruction following
  and factual Q&A
- Temperature 0.1 reduces hallucination — critical for a policy assistant
- `max_tokens=1024` prevents run-on answers while allowing complete policy explanations

---

### 2.6 Prompt Design & Guardrails

The system prompt (`app/prompts.py`) enforces:

1. **Corpus-only answers** — the model is instructed to answer *only* from the provided
   context and to say "I can only answer questions about our company policies" for
   out-of-corpus questions.
2. **Mandatory citation** — every answer must reference source document filenames in
   `[Source: filename.md]` format.
3. **Length limit** — `max_tokens=1024` hard cap.
4. **Post-generation validation** — `check_answer_validity()` scans the answer for
   refusal phrases and flags answers that lack citations.

---

### 2.7 Web Framework — Flask

**Choice:** Flask 3.1 with Flask-CORS and Gunicorn for production.

**Why:**
- Lightweight, well-understood, minimal boilerplate
- CORS enabled for API consumers
- Gunicorn provides multi-worker concurrency suitable for Render's starter tier
- Streamlit was considered but provides less control over the REST API shape

---

## 3. Evaluation Approach

### 3.1 Test Dataset

25 curated questions generated in `scripts/create_test_dataset.py`, covering:

| Category | # Questions |
|---|---|
| Leave & PTO | 4 |
| Remote Work | 3 |
| Expenses | 3 |
| Information Security | 3 |
| Professional Development | 2 |
| Social Media | 1 |
| Email & Communication | 1 |
| Workplace Safety | 1 |
| Employee Handbook | 2 |
| IT & Equipment | 1 |
| Data Privacy | 2 |
| Out-of-corpus (refusal tests) | 2 |

Each question includes:
- `expected_sources` — filenames that should be cited
- `gold_answer_keywords` — key terms expected in a correct answer
- `category` — topic label

### 3.2 Metrics

#### Information Quality

| Metric | Method | Target |
|---|---|---|
| **Groundedness** | Lexical overlap between answer sentences and retrieved context chunks. Sentence scored as grounded if ≥50% of non-stopword tokens appear in context. | ≥ 95% of sentences grounded |
| **Citation Accuracy** | % of source filenames listed in the response that were actually present in the top-k retrieved set | ≥ 98% |
| **Answer Relevance** | Keyword overlap proxy: combines question-token overlap, gold-keyword coverage, and answer length adequacy | ≥ 0.70 |

#### System Performance

| Metric | Method | Target |
|---|---|---|
| **Latency p50** | Wall-clock time from `rag.query()` call to return, 25-query run | < 2 000 ms |
| **Latency p95** | 95th percentile of 25-query run | < 3 000 ms |
| **Refusal rate** | % of in-corpus questions that trigger a refusal | < 5% |
| **Error rate** | % of queries that raise exceptions | < 0.5% |

### 3.3 How to Run Evaluation

```bash
# Build the vector database (if not already done)
python scripts/build_vector_db.py

# Generate test dataset
python scripts/create_test_dataset.py

# Run evaluation
python scripts/evaluate.py

# Results saved to data/evaluation_results.json
```

### 3.4 Expected Results

Based on the system configuration and manual spot-checks:

| Metric | Expected |
|---|---|
| Groundedness | ~92–96% |
| Citation Accuracy | ~95–99% |
| Answer Relevance | ~75–85% |
| Latency p50 | ~1.5–2.0 s |
| Latency p95 | ~2.5–3.0 s |
| Refusal rate (in-corpus) | < 3% |
| Refusal rate (out-of-corpus) | ~100% (expected behaviour) |

---

## 4. Potential Improvements

- **Cross-encoder re-ranking** — replace keyword re-ranking with a dedicated cross-encoder
  (e.g., `ms-marco-MiniLM-L6`) for higher precision
- **Hybrid search** — combine BM25 sparse retrieval with dense vector search
- **Conversation history** — maintain multi-turn context for follow-up questions
- **Larger embedding model** — `all-mpnet-base-v2` for ~2% quality gain
- **LLM-as-judge evaluation** — use Groq to score groundedness instead of lexical overlap
