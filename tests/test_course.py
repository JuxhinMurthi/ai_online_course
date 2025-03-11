from datetime import datetime

import pytest
from unittest.mock import MagicMock

from fastapi import HTTPException

from src.use_cases.create_course_use_case import CreateCourseUseCase
from src.use_cases.get_course_use_case import GetCourseUseCase
from src.web.schemas import CourseCreate, Course


@pytest.fixture
def new_course_data():
    """ New course object. """
    return CourseCreate(user_id=1, course_title="New Course", course_description="New course description")

@pytest.fixture
def existing_course():
    """ Existing course object. """
    return Course(id=1, user_id=1, course_title="Existing Course", course_description="Existing course description", status="Pending", created_at=datetime.now())

@pytest.fixture
def mock_database(existing_course):
    """ Mock database for fake interactions. """
    mock_db = MagicMock()
    mock_db.get.return_value = existing_course
    return mock_db


def test_get_course_use_case(existing_course, mock_database):
    """ Test successful get course use case. """
    use_case = GetCourseUseCase(mock_database)
    course = use_case.execute(existing_course.id)
    assert course.id == existing_course.id


def test_create_course_use_case_success(new_course_data, mock_database):
    """ Test successful create course use case. """
    mock_database.filter.return_value = None
    mock_database.create.return_value = Course(id=2, user_id=1, course_title=new_course_data.course_title, course_description=new_course_data.course_description, status="Pending", created_at=datetime.now())

    use_case = CreateCourseUseCase(mock_database)
    course = use_case.execute(new_course_data)

    assert course.id == 2
    assert course.user_id == course.user_id
    assert course.course_title == new_course_data.course_title
    assert course.course_description == new_course_data.course_description
    mock_database.create.assert_called_once()


def test_create_course_use_case_failure(existing_course, mock_database):
    """ Test failure when course already exists (HTTP 409). """
    mock_database.filter.return_value = existing_course

    use_case = CreateCourseUseCase(mock_database)

    with pytest.raises(HTTPException) as exc_info:
        use_case.execute(CourseCreate(user_id=1, course_title=existing_course.course_title, course_description="Another course description"))

    assert exc_info.value.status_code == 409
    assert f"Course with title {existing_course.course_title} already exists" in exc_info.value.detail
    mock_database.create.assert_not_called()
