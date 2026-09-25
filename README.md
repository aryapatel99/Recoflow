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