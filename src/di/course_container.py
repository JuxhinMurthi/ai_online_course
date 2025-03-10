from dependency_injector import containers, providers

from src.use_cases.create_course_use_case import CreateCourseUseCase
from src.use_cases.get_course_use_case import GetCourseUseCase


class CourseUseCaseContainer(containers.DeclarativeContainer):
    """ Course use case container. """

    database = providers.Dependency()

    create_course_use_case = providers.Factory(CreateCourseUseCase, database=database)
    get_course_use_case = providers.Factory(GetCourseUseCase, database=database)


class CoursePackageContainer(containers.DeclarativeContainer):
    """ Course package container. """

    database = providers.Dependency()

    use_cases = providers.Container(
        CourseUseCaseContainer,
        database=database,
    )