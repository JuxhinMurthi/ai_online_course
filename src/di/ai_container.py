from dependency_injector import containers, providers

from src.use_cases.generate_course_all_summary_use_case import GenerateAllCourseSummaryUseCase
from src.use_cases.generate_course_summary_use_case import GenerateCourseSummaryUseCase


class AiUseCaseContainer(containers.DeclarativeContainer):
    """ AI use case container. """

    database = providers.Dependency()
    ai_service = providers.Dependency()

    generate_course_summary_use_case = providers.Factory(GenerateCourseSummaryUseCase, database=database, ai_service=ai_service)
    generate_course_all_summary_use_case = providers.Factory(GenerateAllCourseSummaryUseCase, database=database, ai_service=ai_service)


class AiPackageContainer(containers.DeclarativeContainer):
    """ AI package container. """

    database = providers.Dependency()
    ai_service = providers.Dependency()

    use_cases = providers.Container(
        AiUseCaseContainer,
        database=database,
        ai_service=ai_service,
    )
