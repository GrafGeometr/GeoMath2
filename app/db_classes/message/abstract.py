from typing import List

from app.imports import *

from abc import abstractmethod
from app.db_classes.standard_model.abstract import AbstractStandardModel


class AbstractMessage(AbstractStandardModel):
    # --> INITIALIZE
    __abstract__ = True

    # --> RELATIONS

    # --> PROPERTIES
    @property
    @abstractmethod
    def content(self) -> str:
        pass

    @content.setter
    @abstractmethod
    def content(self, value: str):
        pass

    @property
    @abstractmethod
    def date(self) -> "datetime.datetime":
        pass

    @date.setter
    @abstractmethod
    def date(self, value: "datetime.datetime"):
        pass

    @property
    @abstractmethod
    def user_to_chat_relation_id(self) -> int:
        pass

    @user_to_chat_relation_id.setter
    @abstractmethod
    def user_to_chat_relation_id(self, value: int):
        pass

    @property
    @abstractmethod
    def user_to_chat_relation(self) -> "AbstractUserToChatRelation":
        pass

    @user_to_chat_relation.setter
    @abstractmethod
    def user_to_chat_relation(self, value: "AbstractUserToChatRelation"):
        pass

    @property
    @abstractmethod
    def user_to_message_relations(self) -> List["UserToMessageRelation"]:
        pass

    @user_to_message_relations.setter
    @abstractmethod
    def user_to_message_relations(self, value: List["UserToMessageRelation"]):
        pass

    # --> METHODS
