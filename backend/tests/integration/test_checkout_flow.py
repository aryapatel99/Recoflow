import uuid
from decimal import Decimal

from fastapi.testclient import TestClient

from backend.app.main import app


client = TestClient(app)


def _user_headers():
    email = f"checkout_{uuid.uuid4().hex[:12]}@example.com"
    response = client.post(
        "/auth/register",
        json={
            "email": email,
            "password": "TestPassword123!",
            "full_name": "Checkout User",
        },
    )
    assert response.status_code == 201
    login = client.post(
        "/auth/login",
        json={"email": email, "password": "TestPassword123!"},
    )
    return {"Authorization": f"Bearer {login.json()['access_token']}"}


def test_checkout_calculates_total_and_is_idempotent():
    headers = _user_headers()
    product = client.get(
        "/api/v1/products", params={"page_size": 1}
    ).json()["items"][0]
    payload = {
        "items": [{"product_id": product["id"], "quantity": 2}],
        "delivery_address": {
            "full_name": "Checkout User",
            "line1": "1 Test Street",
            "city": "Pune",
            "state": "Maharashtra",
            "postal_code": "411001",
            "country": "India",
        },
        "shipping_method": "standard",
        "idempotency_key": f"checkout-{uuid.uuid4().hex}",
    }

    first = client.post("/api/v1/orders", json=payload, headers=headers)
    assert first.status_code == 201
    body = first.json()
    assert body["total_amount"] == str(Decimal(str(product["price"])) * 2)
    assert body["items"][0]["unit_price"] == product["price"]

    second = client.post("/api/v1/orders", json=payload, headers=headers)
    assert second.status_code == 201
    assert second.json()["id"] == body["id"]


def test_order_details_are_authorized():
    owner_headers = _user_headers()
    other_headers = _user_headers()
    product = client.get(
        "/api/v1/products", params={"page_size": 1}
    ).json()["items"][0]
    payload = {
        "items": [{"product_id": product["id"], "quantity": 1}],
        "delivery_address": {
            "full_name": "Owner",
            "line1": "1 Test Street",
            "city": "Pune",
            "state": "Maharashtra",
            "postal_code": "411001",
        },
        "shipping_method": "express",
        "idempotency_key": f"authorized-{uuid.uuid4().hex}",
    }
    order = client.post(
        "/api/v1/orders",
        json=payload,
        headers=owner_headers,
    ).json()

    response = client.get(
        f"/api/v1/orders/{order['id']}",
        headers=other_headers,
    )
    assert response.status_code == 404
