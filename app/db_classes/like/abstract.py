from app.imports import *

from app.sqlalchemy_custom_types import *

from abc import abstractmethod
from app.db_classes.standard_model.abstract import AbstractStandardModel


class AbstractLike(AbstractStandardModel):
    # --> INITIALIZE
    __abstract__ = True

    # --> RELATIONS

    # --> PROPERTIES
    @property
    @abstractmethod
    def parent_type(self) -> "DbParentType":
        pass

    @parent_type.setter
    @abstractmethod
    def parent_type(self, value: "DbParentType"):
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
    def good(self) -> bool:
        pass

    @good.setter
    @abstractmethod
    def good(self, value: bool):
        pass

    @property
    @abstractmethod
    def bad(self) -> bool:
        pass

    @bad.setter
    @abstractmethod
    def bad(self, value: bool):
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
    def user(self) -> "User":
        pass

    @user.setter
    @abstractmethod
    def user(self, value: "User"):
        pass

    # --> METHODS
    @abstractmethod
    def get_parent(self) -> "AbstractStandardModel":
        pass

    @staticmethod
    @abstractmethod
    def exists(parent, user=current_user) -> bool:
        pass

    @staticmethod
    @abstractmethod
    def act_add_like_to_parent(parent, user=current_user, good=True):
        pass

    @staticmethod
    @abstractmethod
    def act_remove_like_from_parent(parent, user=current_user):
        pass
