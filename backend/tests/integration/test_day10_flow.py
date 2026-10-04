from fastapi.testclient import TestClient

from backend.app.main import app


client = TestClient(app)


def test_health():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_openapi_available():
    response = client.get("/openapi.json")

    assert response.status_code == 200

    data = response.json()

    assert "paths" in data


def test_recommendation_routes_registered():
    response = client.get("/openapi.json")

    paths = response.json()["paths"]

    assert "/api/v1/recommendations/hybrid" in paths
    assert "/api/v1/recommendations/collaborative" in paths
    assert "/api/v1/evaluation/recommendations" in paths