# CLAUDE.md — Isekai Slow Life Fellow Power Advisor

## Project Overview

A RAG-powered chatbot that advises advanced Isekai: Slow Life players (level 45+) on Fellow Power optimization. Uses Flask + Groq LLM + FAISS vector store + sentence-transformers embeddings over a curated game knowledge base.

## Architecture

```
quanticaiengineering/
├── app/              # Core application modules
│   ├── rag_system.py     # Main RAG orchestration (IsekaiRAGSystem)
│   ├── query.py          # Query processing
│   ├── embeddings.py     # Embedding generation (sentence-transformers)
│   ├── vector_store.py   # FAISS vector store
│   ├── chunking.py       # Document chunking
│   ├── document_loader.py # Document ingestion
│   ├── prompts.py        # Prompt templates (game-focused)
│   ├── evaluation.py     # Evaluation metrics
│   └── web_app.py        # Flask web routes
├── knowledge/        # Game knowledge base (replaces policies/)
│   ├── fellow-power-overview.md
│   ├── fellow-leveling.md
│   ├── fellow-awakening.md
│   ├── skill-pearls.md
│   ├── costumes.md
│   ├── stella.md
│   ├── fishing.md
│   ├── fellow-tier-list.md
│   ├── artifacts.md
│   ├── family-blessings.md
│   ├── advanced-strategies.md
│   └── resource-guide.md
├── server.py         # Flask server entry point
├── config.py         # Centralized configuration
├── data/             # Vector store + test data
├── scripts/          # Build & evaluation scripts
├── tests/            # pytest test suite
├── templates/        # Jinja2 HTML templates
├── static/           # CSS/JS assets
└── wsgi.py           # WSGI entry point (gunicorn)
```

## Development Commands

```bash
cd quanticaiengineering

# Build vector DB from knowledge base
python scripts/build_vector_db.py

# Run locally
python server.py

# Run tests (no API key needed)
APP_ENV=test pytest tests/ -v

# Lint
flake8 app/ scripts/ tests/ config.py
```

## Key Configuration

- All config in `config.py`, driven by environment variables
- Knowledge base in `knowledge/` (was `policies/`)
- `APP_ENV=test` disables API key requirement
- Main RAG class: `IsekaiRAGSystem` (was `PolicyRAGSystem`)

## Target Audience

Advanced players (level 45+) in guild settings. The bot:
- Skips basic tutorials
- Gives specific numbers, formulas, breakpoints
- Advises on multiplier stacking and single-carry meta
- References specific fellows by name and aptitude

## Planned Enhancements

- Discord bot integration (with internal guild guides)
- Chunking/retrieval optimization for game content
- Additional game system coverage beyond Fellow Power

## Iron Loop Methodology

1. **Plan** — Define features in `plans/`
2. **Execute** — Implement with quality gates
3. **Review** — Run tests, lint, quality checks
4. **Iterate** — Refine based on feedback

### Quality Gates

- [ ] `flake8` passes
- [ ] `pytest tests/` passes
- [ ] No secrets in committed files
- [ ] Knowledge base accuracy verified
