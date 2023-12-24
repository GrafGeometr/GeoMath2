from app.imports import *

from abc import abstractmethod
from app.dbc import AbstractModelWithName


class AbstractTag(AbstractModelWithName):
    # --> INITIALIZE
    __abstract__ = True

    # --> RELATIONS

    # --> PROPERTIES
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

    @abstractmethod
    def get_hash(self) -> int:
        pass
