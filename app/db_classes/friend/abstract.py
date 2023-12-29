from app.imports import *
from app.sqlalchemy_custom_types import *

from abc import abstractmethod
from app.db_classes.standard_model.normal import AbstractStandardModel


class AbstractFriend(AbstractStandardModel):
    # --> INITIALIZE
    __abstract__ = True

    # --> PROPERTIES
    @property
    @abstractmethod
    def friend_from(self) -> int:
        pass

    @friend_from.setter
    @abstractmethod
    def friend_from(self, friend_from: int):
        pass

    @property
    @abstractmethod
    def friend_to(self) -> int:
        pass

    @friend_to.setter
    @abstractmethod
    def friend_to(self, friend_to: int):
        pass

    @property
    @abstractmethod
    def accepted(self) -> bool:
        pass

    @accepted.setter
    @abstractmethod
    def accepted(self, accepted: bool):
        pass
