from app.imports import *
from app.sqlalchemy_custom_types import *

from abc import abstractmethod
from app.db_classes.standard_model.normal import AbstractStandardModel


class AbstractChat(AbstractStandardModel):
    # --> INITIALIZE
    __abstract__ = True

    # --> PROPERTIES
    @property
    @abstractmethod
    def readonly(self) -> bool:
        pass

    @readonly.setter
    @abstractmethod
    def readonly(self, readonly: bool):
        pass

    @property
    @abstractmethod
    def user_chats(self) -> list["User_Chat"]:
        pass

    @user_chats.setter
    @abstractmethod
    def user_chats(self, user_chats: list["User_Chat"]):
        pass

    @property
    @abstractmethod
    def club_id(self, club_id: int):
        pass

    @club_id.setter
    @abstractmethod
    def club_id(self, club_id: int):
        pass





