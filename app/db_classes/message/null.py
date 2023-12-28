from typing import List

from app.imports import *

from abc import abstractmethod
from app.db_classes.standard_model.null import NullStandardModel
from app.db_classes.message.abstract import AbstractMessage


class NullMessage(NullStandardModel, AbstractMessage):
    # --> INITIALIZE
    __abstract__ = True

    # --> RELATIONS

    # --> PROPERTIES
    @property
    def content(self) -> str:
        return ""

    @content.setter
    def content(self, value: str):
        pass

    @property
    def date(self) -> "datetime.datetime":
        return datetime.datetime.min

    @date.setter
    def date(self, value: "datetime.datetime"):
        pass

    @property
    def user_to_chat_relation_id(self) -> int:
        return -1

    @user_to_chat_relation_id.setter
    def user_to_chat_relation_id(self, value: int):
        pass

    @property
    def user_to_chat_relation(self) -> "AbstractUserToChatRelation":
        from app.db_classes.user_to_chat_relation.null import NullUserToChatRelation

        return NullUserToChatRelation()

    @user_to_chat_relation.setter
    def user_to_chat_relation(self, value: "AbstractUserToChatRelation"):
        pass

    @property
    def user_to_message_relations(self) -> List["UserToMessageRelation"]:
        return []

    @user_to_message_relations.setter
    def user_to_message_relations(self, value: List["UserToMessageRelation"]):
        pass

    # --> METHODS
