from abc import ABC, abstractmethod, ABCMeta
from sqlalchemy.orm import declarative_base, DeclarativeMeta
from app.imports import *
from .getter import StandardModelGetter


class DeclarativeABCMeta(ABCMeta, DeclarativeMeta):
    pass


class AbstractStandardModel(db.Model):
    # --> INITIALIZE
    __abstract__ = True

    # --> PROPERTIES
    @classmethod
    @property
    @abstractmethod
    def get(cls) -> "StandardModelGetter":
        pass

    @property
    @abstractmethod
    def id(self) -> int:
        pass

    @id.setter
    @abstractmethod
    def id(self, value: int) -> None:
        pass

    # --> METHODS
    @abstractmethod
    def save(self) -> "AbstractStandardModel":
        pass

    @abstractmethod
    def add(self) -> "AbstractStandardModel":
        pass

    @abstractmethod
    def remove(self) -> None:
        pass

    @abstractmethod
    def is_null(self) -> bool:
        pass

    def is_not_null(self) -> bool:
        return not self.is_null()
