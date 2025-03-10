from dataclasses import dataclass

from fastapi import HTTPException

from src.interfaces.database.postgres import PostgresService
from src.interfaces.use_case.use_case import UseCasePort
from src.models.models import Course
from src.web.schemas import CourseCreate

@dataclass
class CreateCourseUseCase(UseCasePort):
    """ Create course use case. """
    database: PostgresService

    def execute(self, data: CourseCreate, **kwargs):
        existing_course = self.database.filter(model=Course, model_field="course_title", value=data.course_title)

        if existing_course:
            raise HTTPException(status_code=409, detail=f"Course with title {data.course_title} already exists")

        course_object = self.database.create(model=Course, **data.model_dump())
        return course_object