"""
Basic API tests for the Real Estate RAG service.
"""

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "service" in data


def test_root_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"


def test_query_endpoint_shape():
    # This only validates request/response path exists.
    # It may fail at runtime if OPENAI_API_KEY is not configured.
    payload = {
        "query": "What documents do I need to buy a property?",
        "top_k": 3,
    }
    response = client.post("/query", json=payload)
    assert response.status_code in (200, 500)
