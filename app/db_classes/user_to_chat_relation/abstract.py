from app.imports import *

from abc import abstractmethod
from app.dbc import AbstractStandardModel


class AbstractUserToChatRelation(AbstractStandardModel):
    # --> INITIALIZE
    __abstract__ = True

    # --> RELATIONS

    # --> PROPERTIES
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
    def chat_id(self) -> int:
        pass

    @chat_id.setter
    @abstractmethod
    def chat_id(self, value: int):
        pass

    @property
    @abstractmethod
    def messages(self) -> list["Message"]:
        pass

    @messages.setter
    @abstractmethod
    def messages(self, value: list["Message"]):
        pass

    # --> METHODS
    @abstractmethod
    def is_owner(self) -> bool:
        pass

    @abstractmethod
    def is_participant(self) -> bool:
        pass
