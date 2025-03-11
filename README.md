# AI-Powered Online Course Summary Generator

## Project Overview
This project is a FastAPI-based service that helps course creators quickly generate summaries for their courses using AI. The service allows users to submit course descriptions, which are processed by OpenAI's GPT model to generate concise summaries.

### Features
✅ Store course descriptions and summaries in a PostgreSQL database  
✅ Use OpenAI to generate a short summary of a course description  
✅ Provide an API to fetch user and course details  
✅ Use Celery for async task processing  

## API Endpoints

### User Management
- `POST /users` → Create a new user
- `GET /users/{user_id}` → Fetch user details

### Course Management
- `POST /courses` → Submit a course description

### AI-Generated Summaries
- `POST /generate_summary/{course_id}` → Generate a summary for a course description using OpenAI
- `POST /generate_all_summaries` → Generate summaries for all pending courses asynchronously using Celery

## Project Setup

### Prerequisites
- Install **Docker** and **Docker Compose**
- Ensure **Python 3.9+** is installed

### Step 1: Clone the Repository
```sh
git clone <repository-url>
cd <project-directory>
```

### Step 2: Create a `.env` File
Create a `.env` file inside the `src/` directory with the following environment variables:

```ini
DATABASE_URL=postgresql://username:password@db:5432/db_name
REDIS_URL=redis://redis:6379/0
OPENAI_API_KEY=your_openai_api_key
```

### Step 3: Build and Run the Services with Docker
Run the following command from the root directory:
```sh
docker-compose -f conf/docker/docker-compose.yaml up --build -d
```
This will set up the PostgreSQL database, Redis, and the FastAPI service.

### Step 4: Verify the Setup
After the services start, check if the API is running by visiting:
```
http://localhost:8000/docs
```
This will open the interactive API documentation (Swagger UI).

## Testing
To run tests, use:
```sh
pytest tests/
```

## Notes
- This implementation does **not** include the bonus features such as rate limiting, authentication, or manual summary editing.
- Background processing for batch summarization is handled using Celery.

## Conclusion
This project demonstrates the integration of FastAPI, PostgreSQL, Celery, and OpenAI to automate course summary generation. Future improvements can include authentication, rate limiting, and user-driven summary modifications.

---
**Author:** Juxhin Murthi  
**License:** MIT

