from app.imports import *

from abc import abstractmethod
from app.dbc import AbstractStandardModel


class AbstractUserToMessageRelation(AbstractStandardModel):
    # --> INITIALIZE
    __abstract__ = True

    # --> RELATIONS

    # --> PROPERTIES
    @property
    @abstractmethod
    def read(self) -> bool:
        pass

    @read.setter
    @abstractmethod
    def read(self, value: bool):
        pass

    @property
    @abstractmethod
    def user_id(self) -> int:
        pass

    @user_id.setter
    @abstractmethod
    def user_id(self, value: int):
        pass

    @property
    @abstractmethod
    def message_id(self) -> int:
        pass

    @message_id.setter
    @abstractmethod
    def message_id(self, value: int):
        pass

    # --> METHODS
    @abstractmethod
    def is_read(self) -> bool:
        pass

    @abstractmethod
    def act_mark_as_read(self) -> "AbstractUserToMessageRelation":
        pass

    @abstractmethod
    def act_mark_as_unread(self) -> "AbstractUserToMessageRelation":
        pass
