"""
Production entry point — gunicorn server:app --preload

Model loads ONCE synchronously at startup in the gunicorn master process.
Workers inherit the loaded model via copy-on-write fork (--preload flag).
All endpoints always return JSON — never bare HTML.
"""
import csv
import gc
import io
import json
import logging
import os
import secrets
import sys
import time
from datetime import datetime
from functools import wraps
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
os.environ.setdefault("APP_ENV", "production")

from flask import (
    Flask,
    jsonify,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from flask_cors import CORS

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

_MAX_UPLOAD_MB = int(os.environ.get("MAX_UPLOAD_MB", "5"))
_MAX_BATCH_ROWS = int(os.environ.get("MAX_BATCH_ROWS", "100"))

# Auth — shared password for guild members. Username is free-form so we know
# who sent what in the logs.
_APP_PASSWORD = os.environ.get("APP_PASSWORD", "chattyalmighty2026")
_SECRET_KEY = os.environ.get("SECRET_KEY") or secrets.token_hex(32)

# Disk-based per-user chat log (JSONL). One line per interaction so we can
# grep, tail, or parse with jq. Lives under logs/ which is gitignored.
_LOGS_DIR = Path(__file__).parent / "logs"
_LOGS_DIR.mkdir(exist_ok=True)
_CHAT_HISTORY_FILE = Path(
    os.environ.get("CHAT_HISTORY_FILE", str(_LOGS_DIR / "chat_history.jsonl"))
)

# ---------------------------------------------------------------------------
# Flask app
# ---------------------------------------------------------------------------

app = Flask(__name__, template_folder="templates", static_folder="static")
app.config["MAX_CONTENT_LENGTH"] = _MAX_UPLOAD_MB * 1024 * 1024  # hard limit before route
app.config["SECRET_KEY"] = _SECRET_KEY
app.config["SESSION_COOKIE_HTTPONLY"] = True
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"
CORS(app)


# ---------------------------------------------------------------------------
# Auth helpers
# ---------------------------------------------------------------------------


def _current_user():
    return session.get("username")


def login_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if not _current_user():
            # JSON endpoints get 401, browser pages get a redirect
            if request.path.startswith(("/chat", "/intake", "/batch", "/stats")) and request.method == "POST":
                return jsonify({"error": "Not authenticated", "status": "error"}), 401
            if request.is_json or request.path.startswith("/api"):
                return jsonify({"error": "Not authenticated", "status": "error"}), 401
            return redirect(url_for("login"))
        return view(*args, **kwargs)
    return wrapped


def _log_interaction(mode: str, question: str, answer: str, extra: dict = None):
    """Append a single JSONL record of a user interaction for guild review."""
    try:
        record = {
            "timestamp": datetime.now().isoformat(),
            "username": _current_user() or "anonymous",
            "mode": mode,
            "question": question,
            "answer": (answer or "")[:4000],  # cap to keep file bounded
        }
        if extra:
            record.update(extra)
        with _CHAT_HISTORY_FILE.open("a", encoding="utf-8") as fh:
            fh.write(json.dumps(record, ensure_ascii=False) + "\n")
    except Exception as exc:
        logger.warning("Failed to write chat history: %s", exc)

# ---------------------------------------------------------------------------
# RAG — loaded synchronously at startup.
# With `gunicorn --preload`, this runs once in the master process; workers
# inherit the loaded model via copy-on-write fork — no duplicate downloads.
# ---------------------------------------------------------------------------

_rag = None
_rag_error = None

if os.environ.get("APP_ENV") != "test":
    try:
        logger.info("Loading RAG system at startup…")
        from app.rag_system import IsekaiRAGSystem
        _rag = IsekaiRAGSystem()
        logger.info("RAG system ready.")
    except Exception as exc:
        _rag_error = str(exc)
        logger.error("RAG system failed to load: %s", exc, exc_info=True)


def get_rag():
    """Return the shared RAG instance or raise a descriptive RuntimeError."""
    if _rag is not None:
        return _rag
    if _rag_error:
        raise RuntimeError(f"RAG initialisation failed: {_rag_error}")
    raise RuntimeError("RAG system is not initialised.")


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = (request.form.get("username") or "").strip()
        password = request.form.get("password") or ""
        # Username is free-form but bounded; reject empty / overlong
        if not username or len(username) > 40:
            return render_template("login.html", error="Enter a valid in-game username."), 400
        if password != _APP_PASSWORD:
            logger.warning("Failed login attempt from username=%r", username)
            return render_template("login.html", error="Wrong password."), 401
        session.clear()
        session["username"] = username
        session.permanent = False
        logger.info("Login success: username=%r", username)
        return redirect(url_for("index"))
    # Already logged in? Bounce to chat.
    if _current_user():
        return redirect(url_for("index"))
    return render_template("login.html")


@app.route("/logout")
def logout():
    user = _current_user()
    session.clear()
    logger.info("Logout: username=%r", user)
    return redirect(url_for("login"))


@app.route("/")
@login_required
def index():
    return render_template("index.html", username=_current_user())


@app.route("/intake", methods=["GET", "POST"])
@login_required
def intake():
    """New-player intake questionnaire → prioritized Fellow Power action plan."""
    if request.method == "GET":
        return render_template("intake.html", username=_current_user())

    data = request.get_json(silent=True) or {}
    required = ["main_typing", "top_fellow",
                "current_power", "awakening_stars", "stella_level",
                "spending", "goal", "bottleneck"]
    missing = [f for f in required if not str(data.get(f, "")).strip()]
    if missing:
        return jsonify({"error": f"Missing fields: {', '.join(missing)}", "status": "error"}), 400

    try:
        rag = get_rag()
    except RuntimeError as exc:
        return jsonify({"error": str(exc), "status": "error"}), 503

    # Build a structured prompt that maximizes retrieval AND LLM synthesis.
    # The prompt is deliberately verbose and names the fellow explicitly so
    # the hybrid retrieval's keyword boost pulls fellow-specific chunks.
    # The spending level gates which fellows/events are accessible.
    fellow_name = data['top_fellow'].strip()
    typing = data['main_typing']
    spending = data['spending']
    goal = data['goal']
    bottleneck = data['bottleneck']
    extra = data.get('extra') or 'none'

    question = (
        f"Give me a comprehensive, prioritized action plan for a {typing} main "
        f"whose main carry is {fellow_name}.\n\n"
        f"PLAYER PROFILE:\n"
        f"- Main carry: {fellow_name}\n"
        f"- Main typing: {typing}\n"
        f"- Current Fellow Power: {data['current_power']}\n"
        f"- Awakening stars: {data['awakening_stars']}★\n"
        f"- Stella level: {data['stella_level']}\n"
        f"- Spending level: {spending}\n"
        f"- Goal: {goal}\n"
        f"- Biggest bottleneck: {bottleneck}\n"
        f"- Extra context: {extra}\n\n"
        f"INSTRUCTIONS FOR THE ADVISOR:\n"
        f"1. Look up {fellow_name} in the knowledge base — identify their rarity, "
        f"group, Stella pattern, and base aptitude. If {fellow_name} is not a viable "
        f"main carry (wrong rarity, not recommended), say so and suggest alternatives.\n"
        f"2. Look up which FAMILIES bless {fellow_name} in families-roster.md — list "
        f"them by rarity (UR first, then SSR) and recommend which to push first.\n"
        f"3. Address the player's GOAL ({goal}) and BOTTLENECK ({bottleneck}) specifically.\n"
        f"4. Cover ALL relevant power domains: aptitude slots + skill pearls, "
        f"fish (name specific fish for {typing}), family stella, artifacts "
        f"(tier hierarchy, awakening vs leveling, materia + breakthrough gate), "
        f"fellow stella (Pattern A if applicable), awakening gates, costumes, "
        f"buildings ({typing}-typed), consumable items, black pearls.\n"
        f"5. If spending level is F2P, do NOT recommend VIP-gated fellows "
        f"(Neptune, Shlomo, Mammon, Trady, Mescal) or expensive crystal sinks.\n"
        f"6. If spending level is Whale, mention VIP perks and direct-purchase "
        f"Stella options (e.g., Olympics for Heracles).\n"
        f"7. Use specific numbers from the knowledge base. Cite sources.\n"
    )

    try:
        t0 = time.time()
        result = rag.query(question=question, return_metadata=False)
        elapsed = round(time.time() - t0, 3)
        sources = result.get("sources", [])
        _log_interaction(
            mode="intake",
            question=question,
            answer=result["answer"],
            extra={
                "intake": data,
                "confidence": round(result.get("confidence", 0), 4),
                "processing_time": elapsed,
            },
        )
        return jsonify({
            "status": "success",
            "answer": result["answer"],
            "sources": [{"filename": s.get("filename", "")} for s in sources],
            "confidence": round(result.get("confidence", 0), 4),
            "processing_time": elapsed,
        })
    except Exception as exc:
        logger.error("Intake error: %s", exc, exc_info=True)
        return jsonify({"error": "Internal error", "status": "error"}), 500


@app.route("/ping")
def ping():
    """Ultra-lightweight keep-warm / liveness probe — no model access."""
    return jsonify({"status": "ok", "ts": int(time.time())}), 200


@app.route("/health")
def health():
    try:
        rag = get_rag()
        stats = rag.get_stats()
        return jsonify(
            {
                "status": "healthy",
                "timestamp": datetime.now().isoformat(),
                "version": "1.0.0",
                "model": stats.get("model"),
                "vector_store": stats.get("vector_store"),
            }
        )
    except RuntimeError as exc:
        return (
            jsonify(
                {
                    "status": "error",
                    "error": str(exc),
                    "timestamp": datetime.now().isoformat(),
                    "version": "1.0.0",
                }
            ),
            503,
        )
    except Exception as exc:
        return (
            jsonify({"status": "error", "error": str(exc), "timestamp": datetime.now().isoformat()}),
            503,
        )


@app.route("/chat", methods=["POST"])
@login_required
def chat():
    data = request.get_json()
    if not data or "question" not in data:
        return jsonify({"error": "Missing required field: question", "status": "error"}), 400
    question = data["question"].strip()
    if not question:
        return jsonify({"error": "Question cannot be empty", "status": "error"}), 400

    try:
        rag = get_rag()
    except RuntimeError as exc:
        return jsonify({"error": str(exc), "status": "error", "timestamp": datetime.now().isoformat()}), 503

    try:
        from config import TOP_K_DOCUMENTS
        top_k = int(data.get("top_k", TOP_K_DOCUMENTS))
        logger.info("chat | user=%s | q=%r", _current_user(), question[:200])
        t0 = time.time()
        result = rag.query(question=question, top_k=top_k, return_metadata=True)
        elapsed = round(time.time() - t0, 3)

        sources = []
        for chunk in result.get("metadata", {}).get("retrieved_chunks", []):
            sources.append(
                {
                    "filename": chunk.get("source", ""),
                    "title": chunk.get("heading", ""),
                    "score": chunk.get("score", 0),
                    "snippet": chunk.get("preview", ""),
                    "chunk_id": chunk.get("chunk_id", ""),
                }
            )

        _log_interaction(
            mode="chat",
            question=question,
            answer=result["answer"],
            extra={
                "confidence": round(result.get("confidence", 0), 4),
                "processing_time": elapsed,
                "top_k": top_k,
            },
        )

        return jsonify(
            {
                "answer": result["answer"],
                "sources": sources or result.get("sources", []),
                "confidence": result.get("confidence", 0),
                "processing_time": elapsed,
                "timestamp": datetime.now().isoformat(),
                "status": "success",
                "username": _current_user(),
                "metrics": {
                    "retrieval_time": result.get("retrieval_time"),
                    "generation_time": result.get("generation_time"),
                    "is_refusal": result.get("is_refusal", False),
                },
            }
        )
    except Exception as exc:
        logger.error("Chat error: %s", exc, exc_info=True)
        return (
            jsonify(
                {
                    "error": "An internal error occurred. Please try again.",
                    "status": "error",
                    "timestamp": datetime.now().isoformat(),
                }
            ),
            500,
        )


@app.route("/batch", methods=["POST"])
@login_required
def batch():
    """
    Batch CSV question answering.

    POST a multipart/form-data request with field ``file`` containing a CSV
    that has at least a ``question`` column (``question_id`` is optional).

    The file is read row-by-row — it never sits in RAM in full.
    Hard limits: MAX_UPLOAD_MB (default 5 MB), MAX_BATCH_ROWS (default 100).
    Rows beyond the limit are counted but not processed.
    """
    if "file" not in request.files:
        return (
            jsonify(
                {
                    "error": "No 'file' field found. Use multipart/form-data.",
                    "status": "error",
                }
            ),
            400,
        )

    f = request.files["file"]
    if not f.filename:
        return jsonify({"error": "No file selected.", "status": "error"}), 400
    if not f.filename.lower().endswith(".csv"):
        return jsonify({"error": "Only .csv files are accepted.", "status": "error"}), 400

    try:
        rag = get_rag()
    except RuntimeError as exc:
        return jsonify({"error": str(exc), "status": "error"}), 503

    results = []
    skipped = 0

    try:
        # TextIOWrapper streams the upload socket directly — no temp file in RAM
        stream = io.TextIOWrapper(f.stream, encoding="utf-8", errors="replace")
        reader = csv.DictReader(stream)

        if not reader.fieldnames or "question" not in reader.fieldnames:
            return (
                jsonify({"error": "CSV must contain a 'question' column.", "status": "error"}),
                400,
            )

        for i, row in enumerate(reader):
            if len(results) >= _MAX_BATCH_ROWS:
                skipped += 1
                continue  # keep counting but don't process

            question = (row.get("question") or "").strip()
            if not question:
                skipped += 1
                continue

            t0 = time.time()
            # top_k=3 during batch to reduce per-query memory pressure
            result = rag.query(question=question, top_k=3, return_metadata=False)
            elapsed = round(time.time() - t0, 3)

            results.append(
                {
                    "question_id": (row.get("question_id") or str(i + 1)).strip(),
                    "question": question,
                    "answer": result["answer"],
                    "confidence": round(result.get("confidence", 0), 4),
                    "sources": [s.get("filename", "") for s in result.get("sources", [])],
                    "processing_time": elapsed,
                }
            )

            # Hint the GC after each query so intermediate tensors/strings
            # are freed before the next query starts (helps on low-RAM hosts)
            gc.collect()

    except Exception as exc:
        logger.error("Batch error: %s", exc, exc_info=True)
        return jsonify({"error": f"Processing error: {exc}", "status": "error"}), 500
    finally:
        f.close()

    return jsonify(
        {
            "status": "success",
            "count": len(results),
            "skipped": skipped,
            "max_rows": _MAX_BATCH_ROWS,
            "results": results,
        }
    )


@app.route("/api/docs")
def api_docs():
    return jsonify(
        {
            "title": "Isekai Slow Life Fellow Power Advisor API",
            "version": "1.0.0",
            "endpoints": [
                {"path": "/", "method": "GET", "description": "Fellow Power Advisor chat interface"},
                {"path": "/ping", "method": "GET", "description": "Keep-warm / liveness probe"},
                {
                    "path": "/health",
                    "method": "GET",
                    "description": "Health check with system stats",
                },
                {
                    "path": "/chat",
                    "method": "POST",
                    "description": "Game strategy question → answer with citations",
                },
                {
                    "path": "/batch",
                    "method": "POST",
                    "description": (
                        f"CSV upload (≤{_MAX_UPLOAD_MB} MB, ≤{_MAX_BATCH_ROWS} rows)"
                        " → bulk answers"
                    ),
                },
                {"path": "/stats", "method": "GET", "description": "System statistics"},
            ],
        }
    )


@app.route("/stats")
def stats():
    try:
        rag = get_rag()
        return jsonify(
            {
                "status": "success",
                "stats": rag.get_stats(),
                "timestamp": datetime.now().isoformat(),
            }
        )
    except RuntimeError as exc:
        return jsonify({"status": "error", "error": str(exc)}), 503
    except Exception as exc:
        return jsonify({"status": "error", "error": str(exc)}), 500


@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "Not found", "status": "error"}), 404


@app.errorhandler(413)
def too_large(e):
    return (
        jsonify(
            {
                "error": f"Upload too large. Maximum is {_MAX_UPLOAD_MB} MB.",
                "status": "error",
            }
        ),
        413,
    )


@app.errorhandler(500)
def server_error(e):
    return jsonify({"error": "Internal server error", "status": "error"}), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
