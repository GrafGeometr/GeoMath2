from app.imports import *

from abc import abstractmethod
from app.db_classes.standard_model.null import NullStandardModel
from app.db_classes.user_to_message_relation.abstract import (
    AbstractUserToMessageRelation,
)


class NullUserToMessageRelation(NullStandardModel, AbstractUserToMessageRelation):
    # --> INITIALIZE
    __abstract__ = True

    # --> RELATIONS

    # --> PROPERTIES
    @property
    @abstractmethod
    def read(self) -> bool:
        return True

    @read.setter
    @abstractmethod
    def read(self, value: bool):
        pass

    @property
    @abstractmethod
    def user_id(self) -> int:
        return -1

    @user_id.setter
    @abstractmethod
    def user_id(self, value: int):
        pass

    @property
    @abstractmethod
    def message_id(self) -> int:
        return -1

    @message_id.setter
    @abstractmethod
    def message_id(self, value: int):
        pass

    # --> METHODS
    @abstractmethod
    def is_read(self) -> bool:
        return self.read

    @abstractmethod
    def act_mark_as_read(self) -> "AbstractUserToMessageRelation":
        pass

    @abstractmethod
    def act_mark_as_unread(self) -> "AbstractUserToMessageRelation":
        pass
