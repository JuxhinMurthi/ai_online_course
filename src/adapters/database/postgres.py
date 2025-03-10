import os
from typing import Callable, Any, Type, TypeVar, Dict
from kombu.abstract import Object
from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import sessionmaker, Session, Query

from src.interfaces.database.postgres import PostgresDbConnector, PostgresService


T = TypeVar("T")

class PostgresDbConnect(PostgresDbConnector):
    """ Postgres database connector. """

    _engine: Engine = None
    _session_factory: Callable = None

    def __init__(self):
        self._config = os.getenv("DATABASE_URL")
        self.engine = self.create_engine()
        self._create_session_factory()

    def session_maker(self) -> Session:
        """ Create a session. """

        return self._session_factory()

    def create_engine(self):
        """ Create an engine. """

        if not self._engine:
            self._engine = create_engine(self._config)
        return self._engine

    def _create_session_factory(self):
        """ Create a session factory. """

        if not self._session_factory:
            self._session_factory = sessionmaker(bind=self._engine)
        return self._session_factory()


class PostgresDbService(PostgresService):
    """ Postgres database service. """

    def __init__(self):
        self._postgres_db_connect: PostgresDbConnect = PostgresDbConnect()
        self._session = self._postgres_db_connect.session_maker()

    def filter(self, model: Type[T], model_field: str, value: Any) -> Query[T]:
        """ Filter records. """

        query = self._session.query(model).filter(getattr(model, model_field) == value).all()
        return query

    def get(self, model: Type[T], record_id: Any) -> Query[T] | None:
        """ Get records. """

        query = self._session.query(model).get(record_id)
        return query

    def create(self, model: Type[T], **kwargs) -> object:
        """ Create new records. """

        with self._session as session:
            new_object = model(**kwargs)
            session.add(new_object)
            session.commit()
            session.refresh(new_object)
            return new_object

    def update(self, model: Type[T], record_id: int, **kwargs) -> object:
        """ Update records. """

        with self._session as session:
            obj = self._session.query(model).get(record_id)

            if not obj:
                raise ValueError(f"{model.__name__} with id {record_id} not found")

            for key, value in kwargs.items():
                if hasattr(obj, key):
                    setattr(obj, key, value)
                else:
                    raise ValueError(f"{model.__name__} has no attribute '{key}'")

            session.commit()
            session.refresh(obj)
            return obj

    def bulk_update(self, model: Type[T], updates: list,  **kwargs) -> Object | None:
        """ Bulk update records. """

        with self._session as session:
            session.bulk_update_mappings(model, updates)
            session.commit()

    def obj_to_dict(self, obj: object) -> Dict[str, Any]:
        """ Convert a model instance to a dictionary. """

        return {column.name: getattr(obj, column.name) for column in obj.__table__.columns}




