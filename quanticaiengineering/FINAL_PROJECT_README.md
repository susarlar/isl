# 🚀 Quantic AI Engineering - Policy RAG System - FINAL PROJECT

## 📋 Project Overview

A complete **Retrieval-Augmented Generation (RAG)** system for querying company policies using:
- **Groq LLM API** (openai/gpt-oss-120b reasoning model)
- **FAISS Vector Store** for efficient similarity search
- **Sentence Transformers** for embeddings (all-MiniLM-L6-v2)
- **Flask Web Application** with REST API
- **11 comprehensive policy documents** (~195K characters)

## ✅ Completed Requirements

### 1. Document Corpus ✓
- ✅ 12 policy documents (employee handbook, remote work, security, privacy, leave, expenses, professional development, safety, social media, communication, IT equipment, evaluation metrics)
- ✅ Total: ~195,275 characters, 28,241 words
- ✅ Formats supported: Markdown, TXT, PDF, HTML

### 2. Ingestion & Indexing ✓
- ✅ Document parsing and cleaning ([app/document_loader.py](app/document_loader.py))
- ✅ Hybrid chunking (headings + token windows with overlap) ([app/chunking.py](app/chunking.py))
- ✅ Embedding generation with sentence-transformers ([app/embeddings.py](app/embeddings.py))
- ✅ FAISS vector store with optional ChromaDB support ([app/vector_store.py](app/vector_store.py))
- ✅ 659 chunks created and indexed

### 3. RAG Pipeline ✓
- ✅ Top-k retrieval (configurable, default k=5)
- ✅ Optional re-ranking using keyword matching
- ✅ Context injection with citations
- ✅ **Guardrails implemented:**
  - Refuses answers outside corpus
  - Length limits (max_tokens=1024)
  - Always cites sources ([Source: filename.md] format)

### 4. Success Metrics ✓
Defined in [policies/EVALUATION_METRICS.md](policies/EVALUATION_METRICS.md):
- ✅ **Information Quality**: Groundedness (≥95%), Citation Accuracy (≥98%), Answer Relevance (≥4.2/5.0)
- ✅ **System Performance**: Latency P95 (<3s), Throughput (≥50 QPS), Error Rate (<0.5%)

### 5. Environment & Reproducibility ✓
- ✅ Virtual environment (venv/)
- ✅ requirements.txt with 50+ dependencies
- ✅ README.md with complete documentation
- ✅ Fixed seeds (RANDOM_SEED=42) in [config.py](config.py)
- ✅ Groq API integration

### 6. Web Application ✓
- ✅ Flask web server ([app/web_app.py](app/web_app.py))
- ✅ **Endpoints:**
  - `GET /` - Modern chat interface with real-time responses
  - `POST /chat` - API endpoint returning answers with citations and snippets
  - `GET /health` - JSON status endpoint
  - `GET /api/docs` - API documentation
  - `GET /stats` - System statistics

## 🏗️ System Architecture

```
┌─────────────────┐
│  User Question  │
└────────┬────────┘
         │
         ▼
┌─────────────────────────────────┐
│   Flask Web App / API           │
│   (app/web_app.py)              │
└────────┬────────────────────────┘
         │
         ▼
┌─────────────────────────────────┐
│   RAG System                    │
│   (app/rag_system.py)           │
│   • Top-k Retrieval             │
│   • Optional Re-ranking         │
│   • Guardrails                  │
└────┬───────────────────┬────────┘
     │                   │
     ▼                   ▼
┌─────────────┐   ┌──────────────┐
│  FAISS      │   │   Groq LLM   │
│  Vector DB  │   │   (120B)     │
│  (659       │   │              │
│  chunks)    │   └──────────────┘
└─────────────┘
     │
     ▼
┌─────────────────────────────────┐
│   Policy Documents              │
│   (policies/*.md)               │
└─────────────────────────────────┘
```

## 📦 Project Structure

```
quantic_ai_engineering/
├── app/
│   ├── __init__.py
│   ├── document_loader.py      # Load & parse documents (MD/PDF/HTML/TXT)
│   ├── chunking.py              # Hybrid chunking strategy
│   ├── embeddings.py            # Sentence-transformers embeddings
│   ├── vector_store.py          # FAISS vector store
│   ├── prompts.py               # Prompt templates with guardrails
│   ├── rag_system.py            # Complete RAG pipeline
│   ├── query.py                 # CLI interface
│   └── web_app.py               # Flask web application ⭐
├── scripts/
│   ├── __init__.py
│   └── build_vector_db.py       # Build vector database
├── policies/
│   ├── employee_handbook.md
│   ├── remote_work_policy.md
│   ├── information_security_policy.md
│   ├── data_privacy_policy.md
│   ├── leave_and_time_off.md
│   ├── expense_reimbursement_policy.md
│   ├── professional_development_policy.md
│   ├── workplace_safety_policy.md
│   ├── social_media_policy.md
│   ├── email_communication_policy.md
│   ├── equipment_it_usage_policy.md
│   └── EVALUATION_METRICS.md
├── templates/
│   └── index.html               # Web chat interface ⭐
├── static/
│   └── .gitkeep
├── data/
│   └── vector_store/
│       ├── faiss_index.bin      # FAISS index
│       ├── metadata.pkl         # Chunk metadata
│       └── build_stats.json     # Build statistics
├── config.py                    # Configuration with seeds
├── requirements.txt             # Python dependencies
├── .env                         # API keys
├── README.md                    # This file
└── WEB_APP_GUIDE.md            # Web app documentation ⭐
```

## 🚀 Quick Start Guide

### 1. Setup Environment
```powershell
# Create virtual environment (already done)
# py -m venv venv

# Activate venv
.\venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure API Key
Add your Groq API key to `.env`:
```
GROQ_API_KEY=your_groq_api_key_here
GROQ_MODEL=openai/gpt-oss-120b
```

### 3. Build Vector Database
```powershell
.\venv\Scripts\python.exe scripts/build_vector_db.py
```

**Output:**
- 12 documents loaded
- 659 chunks created
- Embeddings generated (384 dimensions)
- FAISS index saved to `data/vector_store/`

### 4. Start Web Application ⭐
```powershell
.\venv\Scripts\python.exe app/web_app.py
```

**Access:**
- Web UI: http://localhost:5000
- API: http://localhost:5000/chat
- Health: http://localhost:5000/health

### 5. Alternative: CLI Interface
```powershell
# Interactive mode
.\venv\Scripts\python.exe app/query.py

# Single query
.\venv\Scripts\python.exe app/query.py "What is the remote work policy?"
```

## 🌐 Web Application Features

### Chat Interface (`/`)
- 💬 Real-time chat with policy assistant
- 📚 Source citations with snippets
- 📊 Confidence indicators (High/Medium/Low)
- ⏱️ Response time metrics
- 🎯 Example question buttons

### API Endpoint (`POST /chat`)
**Request:**
```json
{
  "question": "What is the remote work policy?",
  "top_k": 5
}
```

**Response:**
```json
{
  "answer": "To be eligible for remote work, you must...",
  "sources": [
    {
      "filename": "remote_work_policy.md",
      "title": "Eligibility Criteria",
      "score": 0.95,
      "snippet": "Employees are eligible for remote work if...",
      "chunk_id": "remote_work_policy_chunk_0001"
    }
  ],
  "confidence": 0.92,
  "processing_time": 2.5,
  "status": "success"
}
```

## 🛡️ Guardrails Implemented

### 1. Corpus-Only Answers
System prompt enforces:
```
"ONLY answer questions about information present in the provided policy documents"
```

Out-of-corpus questions receive:
```
"I can only answer questions about our company policies. 
This topic is not covered in our policy documentation."
```

### 2. Citation Requirements
Every answer includes:
- Source document filename
- Relevant section/heading
- Text snippet from source
- Relevance score (0-1)

Format: `[Source: remote_work_policy.md]`

### 3. Length Limits
- Max tokens: 1024 (configurable)
- Typical responses: 2-5 paragraphs
- Concise, focused answers

## 📊 Performance Metrics

### Current System Stats
- **Documents**: 12 policy files
- **Total Chunks**: 659
- **Avg Chunk Size**: 291 characters
- **Embedding Dimension**: 384
- **Vector Store**: FAISS (Flat index, cosine similarity)
- **Model**: openai/gpt-oss-120b (65K context window)

### Typical Response Times
- Retrieval: ~0.1-0.3s
- Generation: ~1-2s
- **Total**: ~1.5-2.5s

## 🧪 Testing

### Test the Web API
```powershell
# PowerShell
$body = @{
    question = "How many days of PTO do employees get?"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:5000/chat" `
    -Method Post `
    -ContentType "application/json" `
    -Body $body
```

### Example Questions to Try
1. "What is the remote work policy?"
2. "How many days of PTO do employees get?"
3. "What are the security requirements for handling confidential data?"
4. "Can I expense meals while traveling?"
5. "What is the parental leave policy?"
6. "How do I report a security incident?"
7. "What are the requirements for professional development reimbursement?"
8. "What is the speed of light?" (tests out-of-corpus refusal)

## 🔧 Configuration

All settings in [config.py](config.py):

```python
# Reproducibility
RANDOM_SEED = 42
EMBEDDING_SEED = 42
EVAL_SEED = 42

# Model Settings
GROQ_MODEL = "openai/gpt-oss-120b"
TEMPERATURE = 0.1
MAX_TOKENS = 1024

# Retrieval Settings
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200
TOP_K_DOCUMENTS = 5

# Embedding Model
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
```

## 📚 Documentation

- [WEB_APP_GUIDE.md](WEB_APP_GUIDE.md) - Web application documentation
- [EVALUATION_METRICS.md](policies/EVALUATION_METRICS.md) - Success metrics
- [QUICKSTART.md](QUICKSTART.md) - Quick start guide
- [SETUP_STATUS.md](SETUP_STATUS.md) - Setup status

## 🐛 Troubleshooting

### Vector Database Not Found
```powershell
# Rebuild the database
.\venv\Scripts\python.exe scripts/build_vector_db.py
```

### Port Already in Use
```powershell
# Use different port
.\venv\Scripts\python.exe app/web_app.py --port 8000
```

### Module Not Found
```powershell
# Reinstall dependencies
pip install -r requirements.txt
```

## 🎯 Key Features Demonstrated

1. ✅ **Complete RAG Pipeline**: Document loading → Chunking → Embedding → Vector storage → Retrieval → Generation
2. ✅ **Multiple Interfaces**: Web UI, REST API, CLI
3. ✅ **Guardrails**: Corpus-only answers, citations, length limits
4. ✅ **Reproducibility**: Fixed seeds, documented configuration
5. ✅ **Production Ready**: Error handling, logging, health checks
6. ✅ **Modern UI**: Clean chat interface with real-time responses
7. ✅ **API First**: RESTful API with JSON responses
8. ✅ **Comprehensive Documentation**: Multiple guides and examples

## 📄 License

This is a student project for Quantic AI Engineering course.

## 👨‍💻 Development

### Add New Policies
1. Add `.md` file to `policies/` directory
2. Rebuild vector database:
   ```powershell
   .\venv\Scripts\python.exe scripts/build_vector_db.py
   ```
3. Restart web app

### Modify Guardrails
Edit prompts in [app/prompts.py](app/prompts.py):
- `SYSTEM_PROMPT` - System-level instructions
- `QUERY_TEMPLATE` - User query template
- Citation format and validation

## 🚀 Next Steps

Potential enhancements:
- [ ] Add user authentication
- [ ] Implement conversation history
- [ ] Add multi-turn dialogue support
- [ ] Deploy to cloud (Azure/AWS)
- [ ] Add analytics dashboard
- [ ] Implement feedback collection
- [ ] Add A/B testing for prompts
- [ ] Integrate evaluation metrics

---

**Built with ❤️ for Quantic AI Engineering**

For questions or issues, refer to the documentation files or review the code comments.
