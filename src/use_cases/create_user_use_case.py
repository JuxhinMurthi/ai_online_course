from dataclasses import dataclass

from fastapi import HTTPException

from src.interfaces.database.postgres import PostgresService
from src.interfaces.use_case.use_case import UseCasePort
from src.web.schemas import UserCreate

from src.models.models import User

@dataclass
class CreateUserUseCase(UseCasePort):
    """ Create user use case. """
    database: PostgresService

    def execute(self, data: UserCreate, **kwargs):
        existing_user = self.database.filter(model=User, model_field="email", value=data.email)

        if existing_user:
            raise HTTPException(status_code=409, detail=f"User with email {data.email} already exists")

        data = data.model_dump()
        data.update({"id": None})
        user = self.database.create(model=User, **data)
        return user
