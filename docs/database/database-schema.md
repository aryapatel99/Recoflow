# RecoFlow Database Schema

## 1. Database Overview

RecoFlow uses PostgreSQL as its primary relational database.

The same PostgreSQL technology is used in:

- Local development
- Testing
- AWS deployment through Amazon RDS for PostgreSQL

The database stores application data, user behavior, product information, transactional data, and recommendation records.

---

## 2. Database Architecture

```text
FastAPI
   ↓
Service Layer
   ↓
Repository Layer
   ↓
PostgreSQL