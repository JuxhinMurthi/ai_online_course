# import pytest
# from fastapi.testclient import TestClient
# from dependency_injector import providers
#
# from src.web.main import app  # import the FastAPI app
# from src.containers import ApplicationContainer  # our DI container
#
# # Define a fake in-memory database that mimics PostgresService
# class FakeDatabase:
#     def __init__(self):
#         self.data = {}
#         self.next_id = 1
#
#     def get(self, model, record_id: int):
#         return self.data.get(record_id)
#
#     def create(self, model, **data):
#         # Simulate assigning an auto-increment id
#         data["id"] = self.next_id
#         self.data[self.next_id] = data
#         self.next_id += 1
#         return data
#
#     def filter(self, model, model_field: str, value):
#         # Return the first match found for the given field
#         for record in self.data.values():
#             if record.get(model_field) == value:
#                 return record
#         return None
#
# # Fixture to override the container with our fake database
# @pytest.fixture(scope="module")
# def test_app():
#     # Create a fake database instance
#     fake_db = FakeDatabase()
#
#     # Override the database dependency in the ApplicationContainer's user package
#     container: ApplicationContainer = app.container  # container created in main.py
#     # Override the 'database' provider in the user package container
#     container.user_package.database.override(providers.Object(fake_db))
#
#     # Create a TestClient using the app with overridden dependencies
#     with TestClient(app) as client:
#         yield client
#
# # Helper function to build a user payload
# def get_user_payload(email="test@example.com", name="Test User"):
#     return {
#         "email": email,
#         "name": name
#     }
#
# # Test the create user endpoint (happy path)
# def test_create_user_success(test_app):
#     payload = get_user_payload()
#     response = test_app.post("/user", json=payload)
#     assert response.status_code == 200, response.text
#     data = response.json()
#     assert data["id"] is not None
#     assert data["email"] == payload["email"]
#     assert data["name"] == payload["name"]
#
# # Test the create user endpoint when a user already exists (conflict)
# def test_create_user_conflict(test_app):
#     payload = get_user_payload(email="conflict@example.com")
#     # Create a user for the first time
#     response = test_app.post("/user", json=payload)
#     assert response.status_code == 200, response.text
#
#     # Try to create a user with the same email
#     conflict_response = test_app.post("/user", json=payload)
#     assert conflict_response.status_code == 409, conflict_response.text
#     error_detail = conflict_response.json()["detail"]
#     assert "already exists" in error_detail
#
# # Test the get user endpoint for an existing user
# def test_get_user_success(test_app):
#     payload = get_user_payload(email="getuser@example.com")
#     # Create a user first
#     create_response = test_app.post("/user", json=payload)
#     assert create_response.status_code == 200, create_response.text
#     created_user = create_response.json()
#     user_id = created_user["id"]
#
#     # Retrieve the user by id
#     get_response = test_app.get(f"/user/{user_id}")
#     assert get_response.status_code == 200, get_response.text
#     retrieved_user = get_response.json()
#     assert retrieved_user["id"] == user_id
#     assert retrieved_user["email"] == payload["email"]
#
# # Test the get user endpoint for a non-existing user
# def test_get_user_not_found(test_app):
#     # Attempt to get a user with an id that does not exist
#     response = test_app.get("/user/9999")
#     assert response.status_code == 404, response.text
#     error_detail = response.json()["detail"]
#     assert error_detail == "User not found"
