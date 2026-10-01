# RecoFlow API Design

## 1. Overview

RecoFlow exposes a REST API through FastAPI.

The API is responsible for:

- Authentication
- User identity
- Product catalog access
- Product catalog management
- User behavior event ingestion
- Session management
- Future recommendation serving
- Future recommendation feedback

The API follows a modular-monolith architecture.

```text
Client
  |
  v
FastAPI
  |
  +-- Authentication
  |
  +-- Product Catalog
  |
  +-- Event Ingestion
  |
  +-- Recommendations
  |
  v
PostgreSQL