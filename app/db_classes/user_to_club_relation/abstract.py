from app.imports import *
from app.sqlalchemy_custom_types import *

from abc import abstractmethod
from app.db_classes.standard_model.normal import AbstractStandardModel


class AbstractUserToClubRelation(AbstractStandardModel):
    # --> INITIALIZE
    __abstract__ = True

    # --> RELATIONS

    # --> PROPERTIES
    @property
    @abstractmethod
    def role(self) -> "Role":
        pass

    @role.setter
    @abstractmethod
    def role(self, value: "Role"):
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
    def club_id(self) -> int:
        pass

    @club_id.setter
    @abstractmethod
    def club_id(self, value: int):
        pass

    # --> METHODS
