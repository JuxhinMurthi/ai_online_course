from dataclasses import dataclass

from src.interfaces.database.postgres import PostgresService
from src.interfaces.use_case.use_case import UseCasePort
from src.models.models import Course

@dataclass
class GetCourseUseCase(UseCasePort):
    """ Get course use case. """

    database: PostgresService

    def execute(self, record_id: int):
        course = self.database.get(model=Course, record_id=record_id)
        return course