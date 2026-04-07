# Deployed Application

## Live URL

> **Update this file after you deploy to Render.**
>
> Example: `https://quantic-policy-rag.onrender.com`

**Deployed URL:** _(add your Render URL here once deployed)_

---

## Deployment Instructions

### 1. Create a Render Account
Sign up at https://render.com (free starter tier is sufficient).

### 2. Connect GitHub Repository
- In Render dashboard → **New +** → **Web Service**
- Connect your GitHub account and select `quanticaiengineering` repo

### 3. Configure the Service
Render will auto-detect `render.yaml` in the repo root and pre-fill most fields.

Manually set the following **secret** environment variable in the Render dashboard:

| Variable | Value |
|---|---|
| `GROQ_API_KEY` | Your Groq API key from https://console.groq.com |

All other environment variables are specified in `render.yaml`.

### 4. First Deploy
The build step runs:
```
pip install -r requirements.txt
```
The start command runs:
```
gunicorn app.web_app:app --workers 2 --threads 2 --bind 0.0.0.0:$PORT --timeout 120
```

> **Note:** The `data/vector_store/` FAISS index is committed to the repository so
> no rebuild step is needed at deploy time.

### 5. Set Up CI/CD Auto-Deploy
To enable automatic deployment when CI passes:
1. In Render dashboard → your service → **Settings** → **Deploy Hook** → copy the URL
2. In GitHub repo → **Settings** → **Secrets and variables** → **Actions**
3. Add secret `RENDER_DEPLOY_HOOK_URL` with the copied Render deploy hook URL

The GitHub Actions workflow (`.github/workflows/ci.yml`) will then automatically
deploy to Render on every successful push to `main`.

---

## Endpoints

| Endpoint | Description |
|---|---|
| `GET /` | Web chat interface |
| `GET /ping` | Liveness probe / keep-warm (no model access) |
| `POST /chat` | REST API — submit a question, receive answer + citations |
| `POST /batch` | CSV upload (≤5 MB, ≤100 rows) → bulk answers |
| `GET /health` | Health check with model stats |
| `GET /api/docs` | API documentation |
| `GET /stats` | System statistics |

---

## VPS Deployment (Arch Linux)

### Systemd service (`/etc/systemd/system/policyrag.service`)

```ini
[Unit]
Description=Quantic Policy RAG
After=network.target

[Service]
User=http
Group=http
WorkingDirectory=/opt/policyrag
EnvironmentFile=/opt/policyrag/.env
ExecStart=/opt/policyrag/venv/bin/gunicorn server:app \
    --preload \
    --workers 1 \
    --threads 2 \
    --worker-class gthread \
    --bind 127.0.0.1:8000 \
    --timeout 120 \
    --log-level info
Restart=on-failure
RestartSec=5

[Install]
WantedBy=multi-user.target
```

`--preload` loads the model once in the master process; the single worker inherits it via copy-on-write, so the model is never loaded twice.

### Keep-warm cron (optional, for Render free tier)

```
*/9 * * * * curl -s https://your-app.onrender.com/ping > /dev/null
```
