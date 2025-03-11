#!/usr/bin/env bash
set -e

# Optional: wait for Postgres to be ready here if needed
# For example, using a small while-loop or "wait-for-it.sh"

cd /app/src

# Run Alembic migrations (points to src/alembic.ini)
alembic -c alembic.ini upgrade head

cd ..
# Finally, start Uvicorn
exec uvicorn src.web.main:app --host 0.0.0.0 --port 8000 --reload