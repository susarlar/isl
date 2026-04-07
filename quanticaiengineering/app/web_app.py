"""
Flask Web Application for Fellow Power Advisor System
============================================

Provides a web interface and API for querying company policies.

Endpoints:
- GET  /         - Web chat interface
- POST /chat     - API endpoint for questions (returns answers with citations)
- GET  /health   - Health check endpoint
- GET  /api/docs - API documentation
"""

import sys
import os
import time
from pathlib import Path
from typing import Dict, List
from datetime import datetime

from flask import Flask, request, jsonify, render_template, send_from_directory
from flask_cors import CORS

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.rag_system import IsekaiRAGSystem
from config import GROQ_MODEL, TOP_K_DOCUMENTS

import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__, template_folder="../templates", static_folder="../static")
CORS(app)  # Enable CORS for API access

# Initialize RAG system (lazy loading)
rag_system = None
initialization_error = None


def get_rag_system() -> IsekaiRAGSystem:
    """Get or initialize the RAG system."""
    global rag_system, initialization_error

    if rag_system is None and initialization_error is None:
        try:
            logger.info("Initializing RAG system...")
            rag_system = IsekaiRAGSystem()
            logger.info("✓ RAG system initialized successfully")
        except Exception as e:
            initialization_error = str(e)
            logger.error(f"Failed to initialize RAG system: {e}")
            raise

    if initialization_error:
        raise RuntimeError(f"RAG system initialization failed: {initialization_error}")

    return rag_system


# Routes
# ======


@app.route("/")
def index():
    """Render the chat interface."""
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    """
    Handle chat requests.

    Request JSON:
        {
            "question": "What is the remote work policy?",
            "top_k": 5,  # optional
            "stream": false  # optional
        }

    Response JSON:
        {
            "answer": "...",
            "sources": [
                {
                    "filename": "remote_work_policy.md",
                    "title": "Remote Work Policy",
                    "score": 0.95,
                    "snippet": "..."
                }
            ],
            "confidence": 0.92,
            "processing_time": 2.5,
            "timestamp": "2026-02-22T10:30:00"
        }
    """
    try:
        # Get RAG system
        rag = get_rag_system()

        # Parse request
        data = request.get_json()

        if not data or "question" not in data:
            return (
                jsonify(
                    {"error": "Missing required field: question", "status": "error"}
                ),
                400,
            )

        question = data["question"].strip()

        if not question:
            return (
                jsonify({"error": "Question cannot be empty", "status": "error"}),
                400,
            )

        # Get optional parameters
        top_k = data.get("top_k", TOP_K_DOCUMENTS)

        # Process query
        logger.info(f"Processing question: {question[:100]}...")
        start_time = time.time()

        result = rag.query(question=question, top_k=top_k, return_metadata=True)

        processing_time = time.time() - start_time

        # Extract snippets from retrieved chunks
        sources_with_snippets = []
        if "metadata" in result and "retrieved_chunks" in result["metadata"]:
            for chunk_info in result["metadata"]["retrieved_chunks"]:
                sources_with_snippets.append(
                    {
                        "filename": chunk_info["source"],
                        "title": chunk_info.get("heading", "N/A"),
                        "score": chunk_info["score"],
                        "snippet": chunk_info["preview"],
                        "chunk_id": chunk_info["chunk_id"],
                    }
                )

        # Prepare response
        response = {
            "answer": result["answer"],
            "sources": sources_with_snippets
            if sources_with_snippets
            else result["sources"],
            "confidence": result["confidence"],
            "processing_time": round(processing_time, 3),
            "timestamp": datetime.now().isoformat(),
            "status": "success",
            "metrics": {
                "retrieval_time": result["retrieval_time"],
                "generation_time": result["generation_time"],
                "total_time": result["total_time"],
                "is_valid": result["is_valid"],
                "is_refusal": result["is_refusal"],
            },
        }

        logger.info(f"✓ Processed question in {processing_time:.3f}s")

        return jsonify(response), 200

    except Exception as e:
        logger.error(f"Error processing chat request: {e}")
        return (
            jsonify(
                {
                    "error": str(e),
                    "status": "error",
                    "timestamp": datetime.now().isoformat(),
                }
            ),
            500,
        )


@app.route("/health", methods=["GET"])
def health():
    """
    Health check endpoint.

    Returns:
        JSON with system status
    """
    try:
        # Try to get RAG system
        rag = get_rag_system()

        # Get system stats
        stats = rag.get_stats()

        return (
            jsonify(
                {
                    "status": "healthy",
                    "timestamp": datetime.now().isoformat(),
                    "model": stats["model"],
                    "vector_store": {
                        "total_chunks": stats["vector_store"]["total_chunks"],
                        "unique_sources": stats["vector_store"]["unique_sources"],
                    },
                    "uptime": "running",
                    "version": "0.1.0",
                }
            ),
            200,
        )

    except Exception as e:
        return (
            jsonify(
                {
                    "status": "unhealthy",
                    "error": str(e),
                    "timestamp": datetime.now().isoformat(),
                }
            ),
            503,
        )


@app.route("/api/docs", methods=["GET"])
def api_docs():
    """API documentation."""
    docs = {
        "title": "Isekai Slow Life Fellow Power Advisor Fellow Power Advisor API",
        "version": "0.1.0",
        "description": "API for Isekai Slow Life game strategy optimization",
        "endpoints": [
            {"path": "/", "method": "GET", "description": "Web chat interface"},
            {
                "path": "/chat",
                "method": "POST",
                "description": "Ask a game strategy question and get an answer with citations",
                "request_body": {
                    "question": "string (required)",
                    "top_k": "integer (optional, default: 5)",
                },
                "response": {
                    "answer": "string",
                    "sources": "array of source objects with snippets",
                    "confidence": "float",
                    "processing_time": "float",
                    "timestamp": "ISO datetime string",
                },
            },
            {
                "path": "/health",
                "method": "GET",
                "description": "Health check endpoint",
                "response": {
                    "status": "healthy | unhealthy",
                    "timestamp": "ISO datetime string",
                    "model": "string",
                    "vector_store": "object",
                },
            },
        ],
        "examples": {
            "chat_request": {"question": "How should I allocate Skill Pearls?", "top_k": 5}
        },
    }

    return jsonify(docs), 200


@app.route("/stats", methods=["GET"])
def stats():
    """Get system statistics."""
    try:
        rag = get_rag_system()
        stats = rag.get_stats()

        return (
            jsonify(
                {
                    "status": "success",
                    "stats": stats,
                    "timestamp": datetime.now().isoformat(),
                }
            ),
            200,
        )

    except Exception as e:
        return (
            jsonify(
                {
                    "status": "error",
                    "error": str(e),
                    "timestamp": datetime.now().isoformat(),
                }
            ),
            500,
        )


# Error handlers
# ==============


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return (
        jsonify(
            {
                "error": "Endpoint not found",
                "status": "error",
                "timestamp": datetime.now().isoformat(),
            }
        ),
        404,
    )


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    return (
        jsonify(
            {
                "error": "Internal server error",
                "status": "error",
                "timestamp": datetime.now().isoformat(),
            }
        ),
        500,
    )


# Main
# ====

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Run the Fellow Power Advisor web application")
    parser.add_argument("--host", default="0.0.0.0", help="Host to bind to")
    parser.add_argument("--port", type=int, default=5000, help="Port to bind to")
    parser.add_argument("--debug", action="store_true", help="Enable debug mode")

    args = parser.parse_args()

    print()
    print("=" * 70)
    print("Isekai Slow Life Fellow Power Advisor - Fellow Power Advisor Web Application")
    print("=" * 70)
    print()
    print(f"Starting server on http://{args.host}:{args.port}")
    print()
    print("Endpoints:")
    print(f"  Web UI:        http://{args.host}:{args.port}/")
    print(f"  Chat API:      http://{args.host}:{args.port}/chat")
    print(f"  Health Check:  http://{args.host}:{args.port}/health")
    print(f"  API Docs:      http://{args.host}:{args.port}/api/docs")
    print(f"  Statistics:    http://{args.host}:{args.port}/stats")
    print()
    print("Press Ctrl+C to stop the server")
    print("=" * 70)
    print()

    app.run(host=args.host, port=args.port, debug=args.debug)
