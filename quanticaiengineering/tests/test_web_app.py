"""
Tests for the Flask web application endpoints.

All tests use a mocked RAG system - no API key or vector DB required.
"""

import json


def test_health_endpoint(flask_app):
    client, mock_rag = flask_app
    resp = client.get("/health")
    assert resp.status_code == 200
    data = json.loads(resp.data)
    assert data["status"] == "healthy"
    assert "model" in data
    assert "vector_store" in data


def test_api_docs_endpoint(flask_app):
    client, _ = flask_app
    resp = client.get("/api/docs")
    assert resp.status_code == 200
    data = json.loads(resp.data)
    assert "endpoints" in data
    assert data["version"] == "1.0.0"


def test_stats_endpoint(flask_app):
    client, _ = flask_app
    resp = client.get("/stats")
    assert resp.status_code == 200
    data = json.loads(resp.data)
    assert data["status"] == "success"
    assert "stats" in data


def test_chat_missing_question(flask_app):
    client, _ = flask_app
    resp = client.post(
        "/chat",
        data=json.dumps({}),
        content_type="application/json",
    )
    assert resp.status_code == 400
    data = json.loads(resp.data)
    assert data["status"] == "error"


def test_chat_empty_question(flask_app):
    client, _ = flask_app
    resp = client.post(
        "/chat",
        data=json.dumps({"question": "   "}),
        content_type="application/json",
    )
    assert resp.status_code == 400


def test_chat_success(flask_app, mock_rag_response):
    client, mock_rag = flask_app
    mock_rag.query.return_value = mock_rag_response

    resp = client.post(
        "/chat",
        data=json.dumps({"question": "How many PTO days do I get?"}),
        content_type="application/json",
    )
    assert resp.status_code == 200
    data = json.loads(resp.data)
    assert data["status"] == "success"
    assert "answer" in data
    assert "sources" in data
    assert "confidence" in data
    assert "processing_time" in data


def test_chat_with_top_k(flask_app, mock_rag_response):
    client, mock_rag = flask_app
    mock_rag.query.return_value = mock_rag_response

    resp = client.post(
        "/chat",
        data=json.dumps({"question": "Remote work policy?", "top_k": 3}),
        content_type="application/json",
    )
    assert resp.status_code == 200
    # Verify top_k was passed to query
    call_kwargs = mock_rag.query.call_args
    assert call_kwargs.kwargs.get("top_k") == 3 or call_kwargs.args[1] == 3


def test_index_route(flask_app):
    client, _ = flask_app
    resp = client.get("/")
    assert resp.status_code == 200


def test_404_returns_json(flask_app):
    client, _ = flask_app
    resp = client.get("/nonexistent-route")
    assert resp.status_code == 404
    data = json.loads(resp.data)
    assert data["status"] == "error"


def test_ping_endpoint(flask_app):
    client, _ = flask_app
    resp = client.get("/ping")
    assert resp.status_code == 200
    data = json.loads(resp.data)
    assert data["status"] == "ok"
    assert "ts" in data


def test_batch_no_file(flask_app):
    client, _ = flask_app
    resp = client.post("/batch")
    assert resp.status_code == 400
    data = json.loads(resp.data)
    assert data["status"] == "error"


def test_batch_wrong_extension(flask_app):
    import io as _io

    client, _ = flask_app
    data = {"file": (_io.BytesIO(b"question\nWhat is PTO?"), "questions.txt")}
    resp = client.post("/batch", data=data, content_type="multipart/form-data")
    assert resp.status_code == 400
    body = json.loads(resp.data)
    assert body["status"] == "error"


def test_batch_missing_question_column(flask_app):
    import io as _io

    client, _ = flask_app
    csv_bytes = b"id,text\n1,hello\n"
    data = {"file": (_io.BytesIO(csv_bytes), "questions.csv")}
    resp = client.post("/batch", data=data, content_type="multipart/form-data")
    assert resp.status_code == 400
    body = json.loads(resp.data)
    assert body["status"] == "error"


def test_batch_success(flask_app, mock_rag_response):
    import io as _io

    client, mock_rag = flask_app
    mock_rag.query.return_value = mock_rag_response

    csv_bytes = b"question_id,question\n1,How many PTO days?\n2,Remote work policy?\n"
    data = {"file": (_io.BytesIO(csv_bytes), "questions.csv")}
    resp = client.post("/batch", data=data, content_type="multipart/form-data")
    assert resp.status_code == 200
    body = json.loads(resp.data)
    assert body["status"] == "success"
    assert body["count"] == 2
    assert len(body["results"]) == 2
    first = body["results"][0]
    assert "answer" in first
    assert "confidence" in first
    assert "sources" in first
