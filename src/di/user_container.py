from dependency_injector import containers, providers

from src.use_cases.create_user_use_case import CreateUserUseCase
from src.use_cases.get_user_use_case import GetUserUseCase


class UserUseCaseContainer(containers.DeclarativeContainer):
    """ User use case container. """

    database = providers.Dependency()

    get_user_usecase = providers.Factory(GetUserUseCase, database=database)
    create_user_use_case = providers.Factory(CreateUserUseCase, database=database)


class UserPackageContainer(containers.DeclarativeContainer):
    """ User package container. """

    database = providers.Dependency()

    use_cases = providers.Container(
        UserUseCaseContainer,
        database=database,
    )
