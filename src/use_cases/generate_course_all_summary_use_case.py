from dataclasses import dataclass

from fastapi import HTTPException

from src.adapters.ai.openai_integration import OpenAIService
from src.interfaces.database.postgres import PostgresService
from src.interfaces.use_case.use_case import UseCasePort
from src.models.models import Course
from src.utils.celery.tasks import generate_all_course_summaries

@dataclass
class GenerateAllCourseSummaryUseCase(UseCasePort):
    """ Generate all course summaries use case. """
    database: PostgresService
    ai_service: OpenAIService

    def execute(self, all_courses: bool):
        all_courses = self.database.filter(model=Course, model_field="status", value="Pending")
        result = [self.database.obj_to_dict(item) for item in all_courses]

        if not all_courses:
            raise HTTPException(status_code=404, detail="No courses found with status 'Pending'")

        task = generate_all_course_summaries.apply_async(args=[result])

        return {
            "message": "Course summary generation started successfully.",
            "task_id": task.id,
            "status": "Processing"
        }
            

