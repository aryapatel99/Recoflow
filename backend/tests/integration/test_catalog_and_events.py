from uuid import uuid4

from fastapi.testclient import TestClient

from backend.app.main import app


client = TestClient(app)


def test_health():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_products_endpoint():
    response = client.get(
        "/api/v1/products"
    )

    assert response.status_code == 200

    body = response.json()

    assert "items" in body
    assert "total" in body
    assert "page" in body
    assert "page_size" in body


def test_events_requires_authentication():
    response = client.post(
        "/api/v1/events",
        json={
            "event_id": f"test-{uuid4().hex}",
            "event_type": "product_view",
        },
    )

    assert response.status_code in {
        401,
        403,
    }