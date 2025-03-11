from datetime import datetime

import pytest
from unittest.mock import MagicMock, patch
from fastapi import HTTPException

from src.models.models import Course
from src.use_cases.generate_course_summary_use_case import GenerateCourseSummaryUseCase
from src.use_cases.generate_course_all_summary_use_case import GenerateAllCourseSummaryUseCase


@pytest.fixture
def existing_course():
    """Mock an existing course."""
    return Course(
        id=1,
        user_id=1,
        course_title="Test Course",
        course_description="This is a test description.",
        status="Pending"
    )


@pytest.fixture
def mock_database(existing_course):
    """Mock database service."""
    mock_db = MagicMock()
    mock_db.get.return_value = existing_course
    mock_db.update.return_value = Course(
        id=existing_course.id,
        user_id=existing_course.user_id,
        course_title=existing_course.course_title,
        course_description=existing_course.course_description,
        ai_summary="This is a generated summary.",
        status="Completed"
    )
    return mock_db


@pytest.fixture
def mock_ai_service():
    """Mock AI service to return a fake summary."""
    mock_ai = MagicMock()
    mock_ai.generate_summary.return_value = "This is a generated summary."
    return mock_ai


def test_generate_course_summary_success(mock_database, mock_ai_service, existing_course):
    """Test successful course summary generation."""
    use_case = GenerateCourseSummaryUseCase(mock_database, mock_ai_service)

    summary = use_case.execute(record_id=existing_course.id)

    assert summary == "This is a generated summary."

    # Validate method calls
    mock_database.get.assert_called_once_with(model=Course, record_id=existing_course.id)
    mock_ai_service.generate_summary.assert_called_once_with(course_description=existing_course.course_description)
    mock_database.update.assert_called_once_with(
        model=Course, record_id=existing_course.id, ai_summary="This is a generated summary.", status="Completed"
    )


def test_generate_course_summary_not_found(mock_database, mock_ai_service):
    """Test failure when course is not found."""
    mock_database.get.return_value = None

    use_case = GenerateCourseSummaryUseCase(mock_database, mock_ai_service)

    with pytest.raises(HTTPException) as exc_info:
        use_case.execute(record_id=999)

    assert exc_info.value.status_code == 404
    assert "No course found with id 999" in exc_info.value.detail
    mock_database.update.assert_not_called()

