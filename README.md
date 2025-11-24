FastAPI Electoral Project - v2

Structure includes core (Postgres) and module elecciones_organizacion split into:
 - geografia_electoral
 - organizacion_electoral

Run instructions:
 - Configure .env with DATABASE_URL pointing to a Postgres instance
 - Install deps: pip install -r requirements/base.txt
 - Generate Alembic env and run migrations (alembic upgrade head)
 - Start: uvicorn app.main:app --reload
