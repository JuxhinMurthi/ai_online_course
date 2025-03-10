# tests/test_course_endpoints.py

import pytest
from fastapi.testclient import TestClient
from dependency_injector import providers

from src.web.main import app  # Import the FastAPI app
from src.web.schemas import CourseCreate


# Define a fake in-memory database that mimics the behavior of PostgresService
class FakeDatabase:
    def __init__(self):
        self.data = {}
        self.next_id = 1

    def get(self, model, record_id: int):
        return self.data.get(record_id)

    def create(self, model, **data):
        # Simulate an auto-increment primary key
        data["id"] = self.next_id
        self.data[self.next_id] = data
        self.next_id += 1
        return data

    def filter(self, model, model_field: str, value):
        # Return the first record that matches the given field value
        for record in self.data.values():
            if record.get(model_field) == value:
                return record
        return None


# Fixture to override the course container's database dependency with our fake database
@pytest.fixture(scope="module")
def test_app():
    fake_db = FakeDatabase()
    container = app.container  # The DI container initialized in main.py
    # Override the 'database' dependency in the course package container
    container.course_package.database.override(providers.Object(fake_db))

    with TestClient(app) as client:
        yield client


# Helper function to build a course payload; note that "user_id" is now included.
def get_course_payload(
    course_title="Introduction to Testing",
    course_description="Learn how to test FastAPI applications",
    user_id=1,
):
    return {
        "course_title": course_title,
        "course_description": course_description,
        "user_id": user_id,
    }


# Test the create course endpoint (happy path)
def test_create_course_success(test_app):
    payload = get_course_payload()
    response = test_app.post("/course", json=payload)
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["id"] is not None
    assert data["course_title"] == payload["course_title"]
    assert data["course_description"] == payload["course_description"]
    assert data["user_id"] == payload["user_id"]


# Test the create course endpoint when a course with the same title already exists (conflict)
def test_create_course_conflict(test_app):
    payload = get_course_payload(course_title="Duplicate Course")
    # First creation should succeed
    response = test_app.post("/course", json=payload)
    assert response.status_code == 200, response.text

    # Second creation with the same title should fail with a 409 error
    conflict_response = test_app.post("/course", json=payload)
    assert conflict_response.status_code == 409, conflict_response.text
    error_detail = conflict_response.json()["detail"]
    assert "already exists" in error_detail


# Test the get course endpoint for an existing course
def test_get_course_success(test_app):
    payload = get_course_payload(course_title="Fetchable Course")
    # Create a course first
    create_response = test_app.post("/course", json=payload)
    assert create_response.status_code == 200, create_response.text
    created_course = create_response.json()
    course_id = created_course["id"]

    # Retrieve the course by ID
    get_response = test_app.get(f"/course/{course_id}")
    assert get_response.status_code == 200, get_response.text
    retrieved_course = get_response.json()
    assert retrieved_course["id"] == course_id
    assert retrieved_course["course_title"] == payload["course_title"]
    assert retrieved_course["course_description"] == payload["course_description"]
    assert retrieved_course["user_id"] == payload["user_id"]


# Test the get course endpoint for a non-existing course
def test_get_course_not_found(test_app):
    # Attempt to fetch a course with an ID that does not exist
    response = test_app.get("/course/9999")
    assert response.status_code == 404, response.text
    error_detail = response.json()["detail"]
    assert error_detail == "Course not found"
