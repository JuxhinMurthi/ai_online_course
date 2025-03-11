import pytest
from unittest.mock import MagicMock

from fastapi import HTTPException

from src.web.schemas import UserCreate, User
from src.use_cases.create_user_use_case import CreateUserUseCase
from src.use_cases.get_user_use_case import GetUserUseCase


@pytest.fixture
def new_user_data():
    """ New user object. """
    return UserCreate(name="New User", email="new@user.com")

@pytest.fixture
def existing_user():
    """ Existing user object. """
    return User(id=1, name="Existing", email="existing@user.com")

@pytest.fixture
def mock_database(existing_user):
    """ Mock database for fake interactions. """
    mock_db = MagicMock()
    mock_db.get.return_value = existing_user
    return mock_db


def test_get_user_use_case(existing_user, mock_database):
    """ Test successful get user use case. """
    use_case = GetUserUseCase(mock_database)
    user = use_case.execute(existing_user.id)
    assert user.id == existing_user.id


def test_create_user_use_case_success(new_user_data, mock_database):
    """ Test successful create user use case. """
    mock_database.filter.return_value = None  # No existing user
    mock_database.create.return_value = User(id=2, name=new_user_data.name, email=new_user_data.email)

    use_case = CreateUserUseCase(mock_database)
    user = use_case.execute(new_user_data)

    assert user.id == 2
    assert user.name == new_user_data.name
    assert user.email == new_user_data.email
    mock_database.create.assert_called_once()


def test_create_user_use_case_failure(existing_user, mock_database):
    """ Test failure when user already exists (HTTP 409). """
    mock_database.filter.return_value = existing_user

    use_case = CreateUserUseCase(mock_database)

    with pytest.raises(HTTPException) as exc_info:
        use_case.execute(UserCreate(name="Duplicate User", email=existing_user.email))

    assert exc_info.value.status_code == 409
    assert f"User with email {existing_user.email} already exists" in exc_info.value.detail
    mock_database.create.assert_not_called()
