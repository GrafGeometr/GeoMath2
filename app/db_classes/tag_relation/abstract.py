from app.imports import *
from app.sqlalchemy_custom_types import *

from abc import abstractmethod
from app.dbc import AbstractStandardModel


class AbstractTagRelation(AbstractStandardModel):
    # --> INITIALIZE
    __abstract__ = True

    # --> RELATIONS

    # --> PROPERTIES
    @property
    @abstractmethod
    def tag_id(self) -> int:
        pass

    @tag_id.setter
    @abstractmethod
    def tag_id(self, value: int):
        pass

    @property
    @abstractmethod
    def parent_id(self) -> int:
        pass

    @parent_id.setter
    @abstractmethod
    def parent_id(self, value: int):
        pass

    @property
    @abstractmethod
    def parent_type(self) -> DbParent:
        pass

    @parent_type.setter
    @abstractmethod
    def parent_type(self, value: DbParent):
        pass

    @property
    @abstractmethod
    def other_data(self) -> dict:
        pass

    @other_data.setter
    @abstractmethod
    def other_data(self, value: dict):
        pass

    # --> METHODS
    @abstractmethod
    def get_parent(self):
        pass

    @staticmethod
    @abstractmethod
    def get_all_by_parent(parent) -> list["AbstractTagRelation"]:
        pass

    @staticmethod
    @abstractmethod
    def get_by_parent_and_tag(parent, tag) -> "AbstractTagRelation":
        pass
