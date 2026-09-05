# github-actions-demo-project

FastAPI CRUD demo template with async SQLAlchemy + PostgreSQL, HTTP Basic auth, and a clean `app/` package layout.

## Stack

- FastAPI (async), SQLAlchemy 2.0 (asyncpg), PostgreSQL 16
- HTTP Basic auth with bcrypt
- Pydantic v2 schemas, repository pattern

## Run locally

```bash
docker compose up -d          # Postgres on port 55432
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Open http://localhost:8000/docs — default login `admin:admin`.
