FROM python:3.12-slim

# Set working directory
WORKDIR /app

COPY conf/docker/app/entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

# Install dependencies
COPY ../../../src/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code into the container
COPY ../../../src/ /app/src

# Expose the FastAPI app port
EXPOSE 8000

# Run the FastAPI app with Uvicorn
CMD ["uvicorn", "src.web.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

ENTRYPOINT ["/app/entrypoint.sh"]