# Use a base Python image
FROM python:3.9-slim

# Set the working directory to /src
WORKDIR /app

# Install dependencies
COPY ../../../src/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code into the container
COPY ../../../src/ /app/src

# Install Celery
RUN pip install celery

# Run the Celery worker
CMD ["celery", "-A", "src.celery.celery_app", "worker", "--loglevel=info"]
