# Backend image

Build from the repository root so the Dockerfile can copy the Python package:

```powershell
docker build -f deployment/backend/Dockerfile -t recoflow-backend:local .
```

The image contains no secrets. Supply `DATABASE_URL`, `JWT_SECRET_KEY`,
`APP_ENV`, `DEBUG`, and `CORS_ORIGINS` through the ECS task definition, using
Secrets Manager for credentials.

Run migrations as a one-off ECS task with the same image and runtime
configuration:

```text
python -m alembic upgrade head
```

