import uuid

from fastapi.testclient import TestClient

from backend.app.main import app


client = TestClient(app)


def test_health_endpoint():
    response = client.get("/health")

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "ok"


def test_register_login_requires_email_verification():
    email = (
        f"test_{uuid.uuid4().hex[:12]}"
        "@recoflow.local"
    )

    response = client.post(
        "/auth/register",
        json={
            "email": email,
            "password": "TestPassword123!",
            "full_name": "RecoFlow Test User",
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["email"] == email
    assert data["email_verified"] is False
    assert data["verification_token"]


def test_protected_endpoint_requires_authentication():
    response = client.get(
        "/auth-test/protected"
    )

    assert response.status_code == 401