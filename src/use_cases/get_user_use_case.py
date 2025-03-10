from src.interfaces.database.postgres import PostgresDbConnector, PostgresService
from src.interfaces.use_case.use_case import UseCasePort
from src.models.models import User
from dataclasses import dataclass

@dataclass
class GetUserUseCase(UseCasePort):
    """ Get user use case. """

    database: PostgresService

    def execute(self, record_id: int):
        user = self.database.get(model=User, record_id=record_id)
        return user