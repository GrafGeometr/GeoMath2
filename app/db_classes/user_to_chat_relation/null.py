from app.imports import *

from app.db_classes.user_to_chat_relation.abstract import AbstractUserToChatRelation
from app.db_classes.standard_model.null import NullStandardModel


class NullUserToChatRelation(NullStandardModel, AbstractUserToChatRelation):
    # --> INITIALIZE
    __abstract__ = True

    # --> RELATIONS

    # --> PROPERTIES
    @property
    def user_id(self) -> int:
        return -1

    @user_id.setter
    def user_id(self, value: int):
        pass

    @property
    def chat_id(self) -> int:
        return -1

    @chat_id.setter
    def chat_id(self, value: int):
        pass

    @property
    def messages(self) -> list["Message"]:
        return []

    @messages.setter
    def messages(self, value: list["Message"]):
        pass

    # --> METHODS
    def is_owner(self) -> bool:
        return False

    def is_participant(self) -> bool:
        return False
