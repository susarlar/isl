# Quantic AI Engineering - Policy RAG Web Application

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- Virtual environment activated
- Vector database built
- Groq API key configured

### Install Dependencies
```powershell
.\venv\Scripts\pip.exe install Flask flask-cors
```

### Start the Web Server
```powershell
.\venv\Scripts\python.exe app/web_app.py
```

Or with custom settings:
```powershell
.\venv\Scripts\python.exe app/web_app.py --host 0.0.0.0 --port 5000 --debug
```

The server will start on `http://localhost:5000`

## 📡 API Endpoints

### 1. Web Chat Interface
- **URL**: `GET /`
- **Description**: Interactive web chat interface
- **Access**: Open `http://localhost:5000` in your browser

### 2. Chat API
- **URL**: `POST /chat`
- **Description**: Submit questions and get answers with citations
- **Request Body**:
  ```json
  {
    "question": "What is the remote work policy?",
    "top_k": 5
  }
  ```
- **Response**:
  ```json
  {
    "answer": "...",
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
    "timestamp": "2026-02-22T10:30:00",
    "status": "success"
  }
  ```

### 3. Health Check
- **URL**: `GET /health`
- **Description**: Check system status
- **Response**:
  ```json
  {
    "status": "healthy",
    "timestamp": "2026-02-22T10:30:00",
    "model": "openai/gpt-oss-120b",
    "vector_store": {
      "total_chunks": 659,
      "unique_sources": 12
    },
    "uptime": "running",
    "version": "0.1.0"
  }
  ```

### 4. API Documentation
- **URL**: `GET /api/docs`
- **Description**: Get API documentation
- **Response**: JSON with endpoint details

### 5. System Statistics
- **URL**: `GET /stats`
- **Description**: Get detailed system statistics
- **Response**: JSON with RAG system stats

## 🧪 Testing the API

### Using curl
```powershell
# Health check
curl http://localhost:5000/health

# Ask a question
curl -X POST http://localhost:5000/chat `
  -H "Content-Type: application/json" `
  -d '{\"question\": \"What is the remote work policy?\"}'

# Get API docs
curl http://localhost:5000/api/docs
```

### Using PowerShell
```powershell
# Health check
Invoke-RestMethod -Uri "http://localhost:5000/health"

# Ask a question
$body = @{
    question = "What is the remote work policy?"
    top_k = 5
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:5000/chat" `
    -Method Post `
    -ContentType "application/json" `
    -Body $body
```

### Using Python
```python
import requests

# Health check
response = requests.get("http://localhost:5000/health")
print(response.json())

# Ask a question
response = requests.post(
    "http://localhost:5000/chat",
    json={
        "question": "What is the remote work policy?",
        "top_k": 5
    }
)
print(response.json())
```

## 🎨 Web Interface Features

The web chat interface (`/`) provides:

1. **Interactive Chat**: Clean, modern chat interface
2. **Real-time Responses**: Instant answers to policy questions
3. **Source Citations**: Each answer includes:
   - Source document filename
   - Relevant section heading
   - Text snippet from source
   - Relevance score (0-100%)
4. **Example Questions**: Quick-start buttons for common queries
5. **Confidence Indicators**: Visual badges showing answer confidence
6. **Response Metrics**: Processing time and performance stats

## 🔒 Security Features

- CORS enabled for API access
- Input validation on all endpoints
- Error handling and logging
- Rate limiting ready (can be added)

## 📊 Monitoring

The application logs all requests and errors. View logs in the console where the server is running.

## 🛠️ Production Deployment

For production, use a WSGI server like Gunicorn:

```powershell
pip install gunicorn

# Run with Gunicorn (Linux/Mac)
gunicorn -w 4 -b 0.0.0.0:5000 app.web_app:app

# Or use waitress for Windows
pip install waitress
waitress-serve --port=5000 app.web_app:app
```

## 📝 Example Queries

Try these questions in the chat interface:

1. "What is the remote work policy?"
2. "How many days of PTO do employees get?"
3. "What are the security requirements for handling confidential data?"
4. "Can I expense meals while traveling?"
5. "What is the parental leave policy?"
6. "How do I report a security incident?"
7. "What are the requirements for professional development reimbursement?"
8. "What should I do if I forget my password?"
9. "What are the company holidays?"
10. "Can I use social media to talk about my work?"

## 🐛 Troubleshooting

### Server won't start
- Check if vector database exists: `data/vector_store/`
- Verify Groq API key in `.env` file
- Ensure all dependencies installed: `pip install -r requirements.txt`

### "Vector database not found" error
Run the build script first:
```powershell
.\venv\Scripts\python.exe scripts/build_vector_db.py
```

### Port already in use
Use a different port:
```powershell
.\venv\Scripts\python.exe app/web_app.py --port 8000
```

## 📚 Architecture

```
Web Request → Flask App → RAG System → Vector Store (FAISS)
                                    → Embeddings (Sentence Transformers)
                                    → LLM (Groq)
                                    ↓
                              Response with Citations
```

## 🔄 Development Workflow

1. **Make changes** to code
2. **Restart server** (Ctrl+C then rerun)
3. **Test in browser** at `http://localhost:5000`
4. **Check logs** in terminal

For auto-reload during development, add `--debug` flag.
