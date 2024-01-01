from typing import List

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
    def club_id(self) -> int:
        pass

    @club_id.setter
    @abstractmethod
    def club_id(self, club_id: int):
        pass

    # --> METHODS
    @abstractmethod
    def contains_user(self, user=current_user) -> bool:
        pass

    @abstractmethod
    def all_messages(self) -> List["Message"]:
        pass

    @abstractmethod
    def unread_messages(self, user=current_user) -> List["Message"]:
        pass

    @abstractmethod
    def last_message_date(self) -> datetime.datetime:
        pass

    @abstractmethod
    def other_user(self, user=current_user) -> "AbstractUser":
        pass

    @abstractmethod
    def count_owners(self) -> int:
        pass

    @abstractmethod
    def count_participants(self) -> int:
        pass

    @abstractmethod
    def add_user(self, user=current_user) -> "AbstractChat":
        pass

    @abstractmethod
    def remove_user(self, user=current_user) -> "AbstractChat":
        pass

    @abstractmethod
    def is_my(self) -> bool:
        pass

    @abstractmethod
    def act_refresh_chat_invites(self) -> "AbstractChat":
        pass

    @abstractmethod
    def act_generate_new_invite_code(self) -> "AbstractChat":
        pass

    @abstractmethod
    def act_mark_all_as_read(self, user=current_user) -> "AbstractChat":
        pass
