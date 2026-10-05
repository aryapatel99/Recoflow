# Alembic migrations

The repository currently has one Alembic head. Verify it before deployment:

```powershell
python -m alembic current
python -m alembic heads
python -m alembic check
```

Run migrations against RDS from a controlled one-off ECS task:

```text
python -m alembic upgrade head
```

Take an RDS snapshot before applying a production migration. Never edit an
already-applied migration; create a new revision for schema changes.

