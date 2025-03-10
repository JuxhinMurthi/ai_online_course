from dataclasses import dataclass

from fastapi import HTTPException

from src.interfaces.database.postgres import PostgresService
from src.interfaces.use_case.use_case import UseCasePort
from src.adapters.ai.openai_integration import OpenAIService
from src.models.models import Course


@dataclass
class GenerateCourseSummaryUseCase(UseCasePort):
    """ Generates a course summary using OpenAI use case. """

    database: PostgresService
    ai_service: OpenAIService

    def execute(self, record_id: int):
        existing_course: Course = self.database.get(model=Course, record_id=record_id)

        if not existing_course:
            raise HTTPException(status_code=404, detail=f"No course found with id {record_id}")

        ai_summary = self.ai_service.generate_summary(course_description=existing_course.course_description)
        updated_course: Course = self.database.update(model=Course, record_id=record_id, ai_summary=ai_summary, status="Completed")

        return updated_course.ai_summary

