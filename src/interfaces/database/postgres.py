from abc import ABC, abstractmethod
from typing import Any, Type, TypeVar, Dict

from kombu.abstract import Object

T = TypeVar("T")


class PostgresDbConnector(ABC):
    """ Postgres database connector interface. """

    @abstractmethod
    def create_engine(self):
        raise NotImplementedError()

    @abstractmethod
    def _create_session_factory(self):
        raise NotImplementedError()

    @abstractmethod
    def session_maker(self):
        raise NotImplementedError()


class PostgresService(ABC):
    """ Postgres database service interface. """

    @abstractmethod
    def filter(self, model: Type[T], model_field: str, value: Any) -> Object:
        """ Filter records interface. """
        raise NotImplementedError()

    @abstractmethod
    def get(self, model: Type[T], record_id: Any) -> Object | None:
        """ Get records interface. """
        raise NotImplementedError()

    @abstractmethod
    def create(self, model: Type[T], **kwargs) -> Object | None:
        """ Create new records interface. """
        raise NotImplementedError()

    @abstractmethod
    def update(self, model: Type[T], record_id: int, **kwargs) -> Object | None:
        """ Update records interface. """
        raise NotImplementedError()

    @abstractmethod
    def bulk_update(self, model: Type[T], updates: list,  **kwargs) -> Object | None:
        """ Bulk update records interface. """
        raise NotImplementedError()

    @abstractmethod
    def obj_to_dict(self, obj: object) -> Dict[str, Any]:
        """ Convert object to dictionary interface. """
        raise NotImplementedError()