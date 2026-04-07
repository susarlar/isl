"""
Pytest configuration and shared fixtures.

Sets APP_ENV=test so config.py skips GROQ_API_KEY validation and model
validation. Heavy components (embeddings, FAISS, Groq) are mocked.
"""

import os
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

# Must be set BEFORE importing config
os.environ["APP_ENV"] = "test"
os.environ.setdefault("GROQ_API_KEY", "test-key-not-real")

# Ensure project root is on the path
sys.path.insert(0, str(Path(__file__).parent.parent))


# ---------------------------------------------------------------------------
# Mock Chunk (mirrors app.chunking.Chunk without importing heavy deps)
# ---------------------------------------------------------------------------


class MockChunk:
    def __init__(
        self, content: str, source: str = "test_policy.md", heading: str = "Section"
    ):
        self.chunk_id = f"{source}_{abs(hash(content)) % 10000:04d}"
        self.content = content
        self.metadata = {
            "filename": source,
            "title": "Test Policy Document",
            "heading": heading,
        }


@pytest.fixture
def sample_chunks():
    return [
        MockChunk(
            "Employees are entitled to 20 days of paid time off per year.",
            "leave_and_time_off.md",
            "PTO Policy",
        ),
        MockChunk(
            "Remote work is available to employees after 6 months of service.",
            "remote_work_policy.md",
            "Eligibility",
        ),
        MockChunk(
            "Passwords must be at least 12 characters long and include uppercase, "
            "lowercase, numbers, and special characters.",
            "information_security_policy.md",
            "Password Requirements",
        ),
    ]


@pytest.fixture
def mock_rag_response():
    return {
        "answer": (
            "Employees receive 20 days of paid time off per year. "
            "[Source: leave_and_time_off.md]"
        ),
        "sources": [
            {
                "filename": "leave_and_time_off.md",
                "title": "Leave and Time Off",
                "score": 0.92,
                "chunk_id": "leave_chunk_001",
            }
        ],
        "confidence": 0.92,
        "retrieval_time": 0.1,
        "generation_time": 1.2,
        "total_time": 1.35,
        "is_valid": True,
        "is_refusal": False,
        "metadata": {
            "chunks_retrieved": 5,
            "top_k": 5,
            "model": "llama-3.3-70b-versatile",
            "reranking_enabled": False,
            "reranking_time": 0.0,
            "validation": {"is_valid": True, "is_refusal": False},
            "retrieved_chunks": [
                {
                    "chunk_id": "leave_chunk_001",
                    "score": 0.92,
                    "source": "leave_and_time_off.md",
                    "heading": "PTO Policy",
                    "preview": "Employees receive 20 days of paid time off per year.",
                }
            ],
        },
    }


@pytest.fixture
def flask_app():
    """Return the Flask test client with a mocked RAG system."""
    # Import app.web_app only inside the fixture so the mock is applied first
    with patch("server.get_rag") as mock_get_rag:
        mock_rag = MagicMock()
        mock_get_rag.return_value = mock_rag
        mock_rag.get_stats.return_value = {
            "model": "llama-3.3-70b-versatile",
            "top_k": 5,
            "reranking_enabled": False,
            "temperature": 0.1,
            "max_tokens": 1024,
            "vector_store": {"total_chunks": 659, "unique_sources": 12},
            "embedding_model": "sentence-transformers/all-MiniLM-L6-v2",
            "embedding_dimension": 384,
        }

        from server import app as flask_application

        flask_application.config["TESTING"] = True
        yield flask_application.test_client(), mock_rag
