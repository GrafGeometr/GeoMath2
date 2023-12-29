from app.imports import *
from app.sqlalchemy_custom_types import *

from abc import abstractmethod
from app.db_classes.standard_model.normal import AbstractStandardModel


class AbstractEmail(AbstractStandardModel):
    # --> INITIALIZE
    __abstract__ = True

    # --> PROPERTIES
    @property
    @abstractmethod
    def created_date(self) -> datetime.datetime:
        pass

    @created_date.setter
    @abstractmethod
    def created_date(self, created_date: datetime.datetime):
        pass

    @property
    @abstractmethod
    def verified(self) -> bool:
        pass

    @verified.setter
    @abstractmethod
    def verified(self, verified: bool):
        pass

    @property
    @abstractmethod
    def token(self) -> str:
        pass

    @token.setter
    @abstractmethod
    def token(self, token: str):
        pass

    @property
    @abstractmethod
    def user_id(self) -> int:
        pass

    @user_id.setter
    @abstractmethod
    def user_id(self, user_id: int):
        pass

    @property
    @abstractmethod
    def user(self) -> "User":
        pass

    @user.setter
    @abstractmethod
    def user(self, user: "User"):
        pass
