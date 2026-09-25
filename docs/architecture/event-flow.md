# RecoFlow Event Flow

## 1. Overview

RecoFlow uses an event-driven application flow to capture user behavior.

User actions are represented as structured events and stored for:

- Recommendation feedback
- Analytics
- Feature engineering
- Model training
- Behavioral analysis

The event system is implemented inside the modular monolith.

---

## 2. Event Lifecycle

```text
User Action
    ↓
Frontend
    ↓
FastAPI Event API
    ↓
Authentication
    ↓
Event Validation
    ↓
Event Service
    ↓
PostgreSQL
    ↓
Analytics / Feature Engineering
    ↓
Recommendation System