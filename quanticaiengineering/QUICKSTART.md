# Policy Corpus RAG Application - Quick Start Guide

## For Windows Users

### Option 1: PowerShell Setup Script (Recommended)
```powershell
# Run the automated setup script
.\setup.ps1
```

If you get an execution policy error:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
.\setup.ps1
```

### Option 2: Manual Setup
```powershell
# 1. Create virtual environment
py -m venv venv

# 2. Activate virtual environment
.\venv\Scripts\Activate.ps1

# 3. Upgrade pip
python -m pip install --upgrade pip

# 4. Install dependencies
pip install -r requirements.txt

# 5. Create .env file
copy .env.example .env
# Edit .env and add your GROQ_API_KEY
```

---

## For macOS/Linux Users

### Option 1: Bash Setup Script (Recommended)
```bash
# Make script executable
chmod +x setup.sh

# Run the setup script
./setup.sh
```

### Option 2: Manual Setup
```bash
# 1. Create virtual environment
python3 -m venv venv

# 2. Activate virtual environment
source venv/bin/activate

# 3. Upgrade pip
python -m pip install --upgrade pip

# 4. Install dependencies
pip install -r requirements.txt

# 5. Create .env file
cp .env.example .env
# Edit .env and add your GROQ_API_KEY
```

---

## After Setup

### 1. Get Your Groq API Key
Visit https://console.groq.com and create a free account to get your API key.

### 2. Configure Environment
Edit the `.env` file and add your API key:
```bash
GROQ_API_KEY=your_actual_api_key_here
```

### 3. Verify Configuration
```bash
python config.py
```

You should see output showing your configuration settings.

### 4. Build Vector Database
```bash
python scripts/build_vector_db.py
```

This will process all policy documents and create the searchable index.

### 5. Start Querying
```bash
python app/query.py
```

Try example queries:
- "How much PTO do I get?"
- "What's the remote work policy?"
- "How do I submit expenses?"

---

## Troubleshooting

### Python Not Found
**Windows:** Install Python from python.org or Microsoft Store
**macOS:** `brew install python3`
**Linux:** `sudo apt-get install python3 python3-venv`

### Virtual Environment Won't Activate (Windows)
Run PowerShell as Administrator:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Dependency Installation Fails
Try upgrading pip first:
```bash
python -m pip install --upgrade pip
pip install --upgrade setuptools wheel
pip install -r requirements.txt
```

### FAISS Installation Issues
**Windows:**
```bash
pip install faiss-cpu
```

**macOS (Apple Silicon):**
```bash
conda install -c pytorch faiss-cpu
```

### Groq API Errors
- Check your API key is correct in .env
- Verify you're within rate limits (30 req/min free tier)
- Check https://status.groq.com for service status

---

## Project Structure Reminder

```
quantic_ai_engineering/
├── .env                    # Your API keys (create from .env.example)
├── config.py               # Configuration with fixed seeds
├── requirements.txt        # Python dependencies
├── README.md              # Full documentation
├── QUICKSTART.md          # This file
├── setup.ps1              # Windows setup script
├── setup.sh               # macOS/Linux setup script
├── policies/              # Policy documents corpus
├── app/                   # Application code (to be created)
├── scripts/               # Utility scripts (to be created)
└── data/                  # Generated data and indexes
```

---

## Next Steps

Once setup is complete:

1. **Review the corpus:** Check the 11 policy documents in `policies/`
2. **Understand metrics:** Read `policies/EVALUATION_METRICS.md`
3. **Build the app:** Create RAG implementation in `app/`
4. **Run evaluations:** Test against defined metrics
5. **Iterate and improve:** Tune based on evaluation results

---

## Need Help?

- **Full Documentation:** See [README.md](README.md)
- **Metrics Guide:** See [policies/EVALUATION_METRICS.md](policies/EVALUATION_METRICS.md)
- **Groq Docs:** https://console.groq.com/docs

---

**Last Updated:** February 22, 2026
