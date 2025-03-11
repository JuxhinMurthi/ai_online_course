#!/usr/bin/env bash
set -e

# Optional: wait for Postgres to be ready
# If you prefer to rely on docker-compose's depends_on, you can remove this or
# add your own logic using wait-for-it or a similar script.

# Run Alembic migrations
#alembic -c /app/src/alembic.ini upgrade head

# Finally, start Uvicorn
exec uvicorn src.web.main:app --host 0.0.0.0 --port 8000 --reload