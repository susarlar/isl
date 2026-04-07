"""
Production entry point — gunicorn server:app --preload

Model loads ONCE synchronously at startup in the gunicorn master process.
Workers inherit the loaded model via copy-on-write fork (--preload flag).
All endpoints always return JSON — never bare HTML.
"""
import csv
import gc
import io
import logging
import os
import sys
import time
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
os.environ.setdefault("APP_ENV", "production")

from flask import Flask, jsonify, render_template, request
from flask_cors import CORS

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

_MAX_UPLOAD_MB = int(os.environ.get("MAX_UPLOAD_MB", "5"))
_MAX_BATCH_ROWS = int(os.environ.get("MAX_BATCH_ROWS", "100"))

# ---------------------------------------------------------------------------
# Flask app
# ---------------------------------------------------------------------------

app = Flask(__name__, template_folder="templates", static_folder="static")
app.config["MAX_CONTENT_LENGTH"] = _MAX_UPLOAD_MB * 1024 * 1024  # hard limit before route
CORS(app)

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


@app.route("/")
def index():
    return render_template("index.html")


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

        return jsonify(
            {
                "answer": result["answer"],
                "sources": sources or result.get("sources", []),
                "confidence": result.get("confidence", 0),
                "processing_time": elapsed,
                "timestamp": datetime.now().isoformat(),
                "status": "success",
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
