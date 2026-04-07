# AI Tool Usage

This document describes the AI tools used and how they contributed to the project.

## Tools Used

### 1. Claude (Anthropic) — Claude Code CLI

**Role:** Primary AI coding assistant throughout the project.

**How used:**
- Scaffolded the initial project structure and boilerplate (Flask app, config module, RAG pipeline)
- Generated the policy document corpus (all 11 `.md` files in `policies/`) as synthetic
  but realistic company policy documents
- Wrote and iterated on the core RAG pipeline (`app/rag_system.py`, `app/vector_store.py`,
  `app/embeddings.py`, `app/chunking.py`, `app/prompts.py`)
- Created the Flask web application (`app/web_app.py`) and HTML chat interface (`templates/index.html`)
- Designed and implemented the evaluation module (`app/evaluation.py`) with groundedness,
  citation accuracy, and latency metrics
- Created the test suite (`tests/`) and GitHub Actions CI/CD workflow (`.github/workflows/ci.yml`)
- Wrote all project documentation (`README.md`, `design-and-evaluation.md`, `deployed.md`, etc.)
- Reviewed code for security issues (e.g., identified and removed a hardcoded API key)

All generated code was reviewed, tested, and refined by the student before submission.

---

### 2. Groq (openai/gpt-oss-120b / llama-3.1-70b-versatile)

**Role:** LLM inference engine within the application itself.

**How used:**
- Powers the answer generation step of the RAG pipeline at runtime
- Not used during development/code generation

---

### 3. Sentence Transformers (HuggingFace)

**Role:** Embedding model for document indexing and query encoding.

**How used:**
- `all-MiniLM-L6-v2` generates dense vector representations of policy document chunks
  and user queries at runtime
- Not used interactively during development

---

## Summary

The bulk of the code and documentation was generated with AI assistance (Claude), then
reviewed and refined by the student. This approach allowed rapid prototyping and iteration
while ensuring the student understood each component through review and testing.

In accordance with the course policy, all use of AI tools is disclosed here.
