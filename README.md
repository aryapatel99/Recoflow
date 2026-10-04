# RecoFlow

Event-Driven Personalized Recommendation & Ranking Platform

## Project Overview

RecoFlow is a production-inspired e-commerce recommendation platform designed to demonstrate software engineering, backend engineering, machine learning, data engineering, and AWS ML engineering skills in one complete system.

The platform processes user behavior events, generates product recommendation candidates, ranks those candidates, evaluates recommendation quality, and continuously uses behavioral feedback to improve recommendations.

The project is designed as a modular monolith first and can later be deployed to AWS using managed services.

---

## Primary Objective

RecoFlow is designed to demonstrate:

- Python backend engineering
- REST API development
- PostgreSQL database engineering
- Secure authentication
- Event-driven application architecture
- Product catalog management
- User behavior tracking
- Recommendation systems
- Candidate generation
- Ranking
- Machine learning
- Offline recommendation evaluation
- Cold-start handling
- Recommendation feedback loops
- ML pipeline design
- AWS ML engineering
- MLOps fundamentals
- Production-oriented system design
- Testing and security

---

## Core Technology Stack

### Backend

- Python
- FastAPI
- SQLAlchemy
- PostgreSQL
- Pydantic
- JWT-based authentication

### Frontend

- Modern e-commerce-style web interface
- Responsive product browsing
- Product detail pages
- Search
- Cart
- Wishlist
- Personalized recommendations
- Authentication
- User activity

### Machine Learning

- Python
- NumPy
- Pandas
- Scikit-learn
- Recommendation algorithms
- Feature engineering
- Offline evaluation

### Cloud

- AWS
- Amazon RDS for PostgreSQL
- Amazon S3
- Amazon SageMaker
- Amazon CloudWatch
- AWS IAM

### Development

- Git
- GitHub
- VS Code
- Docker where useful
- Pytest

---

## Architecture Philosophy

RecoFlow follows a modular monolith architecture.

The project intentionally avoids unnecessary:

- Microservices
- Kafka
- Kubernetes
- Distributed infrastructure
- Deep learning
- LLM features

unless a later requirement clearly justifies them.

The priority is:

```text
Correctness
    ↓
Security
    ↓
Testability
    ↓
Maintainability
    ↓
Scalability
```

## Current local system

The application is a modular monolith:

- FastAPI serves authentication, products, events, behaviors, recommendations,
  evaluation, and orders.
- PostgreSQL stores users, catalog data, behavior events, recommendations,
  carts, wishlists, and orders.
- Next.js serves the storefront and forwards browser API calls through its
  same-origin backend proxy.
- Email ownership verification and real payment processing are intentionally
  not part of the current registration and checkout flows.

### Local setup

1. Copy `.env.example` to `.env` and set a strong `JWT_SECRET_KEY` and a
   PostgreSQL `DATABASE_URL`.
2. Apply migrations:

   ```powershell
   python -m alembic upgrade head
   ```

3. Start the API:

   ```powershell
   uvicorn backend.app.main:app --reload --port 8000
   ```

4. Start the storefront:

   ```powershell
   cd frontend
   npm install
   npm run dev
   ```

The API health check is `GET http://127.0.0.1:8000/health`. The frontend uses
`NEXT_PUBLIC_API_URL` for the server-side proxy target; keep it set to the
reachable backend URL in each environment. `CORS_ORIGINS` is a comma-separated
list of allowed direct-browser origins.

Run backend tests with `pytest -q` and build the frontend with
`cd frontend; npm run build`.

## Planned AWS deployment

AWS deployment is not currently performed by this repository. A minimal
deployment can keep the modular-monolith shape: FastAPI on ECS/Fargate or
Elastic Beanstalk, Next.js on a Node-capable service or static-capable
platform, PostgreSQL on RDS, and product images in S3 or an equivalent CDN.
Secrets should be supplied through AWS Secrets Manager or task environment
configuration, never committed to the repository. Run Alembic migrations as a
deployment step before switching traffic, configure health checks against
`/health`, and set production `DATABASE_URL`, `JWT_SECRET_KEY`,
`CORS_ORIGINS`, and `NEXT_PUBLIC_API_URL` explicitly.

See [docs/aws/aws-architecture.md](docs/aws/aws-architecture.md),
[docs/architecture/system-architecture.md](docs/architecture/system-architecture.md),
and [docs/database/database-schema.md](docs/database/database-schema.md) for
the current architecture and deployment plan.