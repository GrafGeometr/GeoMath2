from app.imports import *

from abc import abstractmethod
from app.db_classes.standard_model.abstract import AbstractStandardModel


class AbstractTag(AbstractStandardModel):
    # --> INITIALIZE
    __abstract__ = True

    # --> RELATIONS

    # --> PROPERTIES
    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @name.setter
    @abstractmethod
    def name(self, name: str):
        pass

    @property
    @abstractmethod
    def hash(self) -> int:
        pass

    @hash.setter
    @abstractmethod
    def hash(self, value: int):
        pass

    # --> METHODS
    @staticmethod
    @abstractmethod
    def get_all_by_obj(obj) -> list["AbstractTag"]:
        pass
