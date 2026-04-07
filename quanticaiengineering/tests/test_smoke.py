"""
Smoke tests — fast checks that the application can be imported and basic
module structure is in place. These run in CI without any API keys or models.
"""

import importlib
import json
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

sys.path.insert(0, str(Path(__file__).parent.parent))
# APP_ENV=test is set in conftest.py


def test_config_imports():
    """Config module should import cleanly in test mode."""
    import config  # noqa: F401


def test_app_package_imports():
    """Core app sub-modules should be importable."""
    for mod in ["app", "app.evaluation", "app.prompts"]:
        importlib.import_module(mod)


def test_server_creates_flask_instance():
    """server.py must expose a Flask app object without loading the RAG system."""
    with patch("server.get_rag"):
        from server import app as flask_app

        assert flask_app is not None
        assert hasattr(flask_app, "route")


def test_evaluation_module_exports():
    """evaluation.py should export key symbols."""
    import app.evaluation as ev

    assert callable(ev.evaluate_groundedness)
    assert callable(ev.evaluate_citation_accuracy)
    assert callable(ev.evaluate_answer_relevance)
    assert callable(ev.compute_latency_stats)
    assert callable(ev.run_evaluation)
    assert callable(ev.save_results)
    assert ev.EvalQuestion is not None
    assert ev.EvalResult is not None
    assert ev.EvalSummary is not None


def test_test_dataset_script_has_questions():
    """create_test_dataset.py must contain at least 15 questions."""
    from scripts.create_test_dataset import QUESTIONS

    assert len(QUESTIONS) >= 15, f"Need at least 15 questions, got {len(QUESTIONS)}"


def test_all_questions_have_required_fields():
    from scripts.create_test_dataset import QUESTIONS

    for q in QUESTIONS:
        assert "question_id" in q
        assert "question" in q
        assert q["question"].strip()


def test_health_endpoint_smoke():
    """Health endpoint should return 200 with a mocked RAG."""
    with patch("server.get_rag") as mock_get:
        mock_rag = MagicMock()
        mock_get.return_value = mock_rag
        mock_rag.get_stats.return_value = {
            "model": "test-model",
            "vector_store": {"total_chunks": 100, "unique_sources": 5},
        }

        from server import app as flask_app

        flask_app.config["TESTING"] = True
        with flask_app.test_client() as client:
            resp = client.get("/health")
            assert resp.status_code == 200
            data = json.loads(resp.data)
            assert data["status"] == "healthy"
