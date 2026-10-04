import uuid

from fastapi.testclient import TestClient

from backend.app.main import app
from backend.app.db.database import SessionLocal
from backend.app.models.user import User


client = TestClient(app)


def unique_email() -> str:
    return f"auth_{uuid.uuid4().hex[:12]}@example.com"


def register(email: str):
    return client.post(
        "/auth/register",
        json={
            "email": email,
            "password": "TestPassword123!",
            "full_name": "RecoFlow Test User",
        },
    )


def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_registration_creates_immediately_usable_account():
    email = unique_email()
    response = register(email)

    assert response.status_code == 201
    assert response.json()["email"] == email

    login = client.post(
        "/auth/login",
        json={"email": email, "password": "TestPassword123!"},
    )
    assert login.status_code == 200
    assert login.json()["access_token"]


def test_registration_rejects_invalid_email_format():
    response = client.post(
        "/auth/register",
        json={
            "email": "not-an-email",
            "password": "TestPassword123!",
            "full_name": "Invalid Email User",
        },
    )
    assert response.status_code == 422


def test_registration_rejects_duplicate_email():
    email = unique_email()
    assert register(email).status_code == 201
    assert register(email.upper()).status_code == 409


def test_registration_creates_active_account_state():
    email = unique_email()
    assert register(email).status_code == 201

    with SessionLocal() as db:
        user = db.query(User).filter(User.email == email).one()
        assert user.is_email_verified is True


def test_me_and_protected_endpoint_work_with_jwt():
    email = unique_email()
    assert register(email).status_code == 201
    login = client.post(
        "/auth/login",
        json={"email": email, "password": "TestPassword123!"},
    )
    headers = {"Authorization": f"Bearer {login.json()['access_token']}"}

    me = client.get("/auth/me", headers=headers)
    assert me.status_code == 200
    assert me.json()["email"] == email

    protected = client.get("/auth-test/protected", headers=headers)
    assert protected.status_code == 200


def test_protected_endpoint_requires_authentication():
    response = client.get("/auth-test/protected")
    assert response.status_code == 401
