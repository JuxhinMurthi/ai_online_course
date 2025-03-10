from dependency_injector import containers, providers

from src.adapters.database.postgres import PostgresDbService
from src.di.ai_container import AiPackageContainer
from src.di.course_container import CoursePackageContainer
from src.di.user_container import UserPackageContainer
from src.adapters.ai.openai_integration import OpenAIService


class ApplicationContainer(containers.DeclarativeContainer):
    """ Application container. """

    config = providers.Configuration()

    database = providers.Singleton(PostgresDbService)
    ai_service = providers.Singleton(OpenAIService)

    user_package = providers.Container(UserPackageContainer, database=database)
    course_package = providers.Container(CoursePackageContainer, database=database)
    ai_package = providers.Container(AiPackageContainer, database=database, ai_service=ai_service)