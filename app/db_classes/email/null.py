import datetime

from app.imports import *
from app.sqlalchemy_custom_types import *

from app.db_classes.standard_model.null import NullStandardModel
from app.db_classes.email.abstract import AbstractEmail


class NullEmail(NullStandardModel, AbstractEmail):
    # --> INITIALIZE
    __abstract__ = True

    # --> PROPERTIES
    @property
    def created_date(self) -> datetime.datetime:
        return datetime.datetime.min

    @created_date.setter
    def created_date(self, created_date: datetime.datetime):
        pass

    @property
    def verified(self) -> bool:
        return False

    @verified.setter
    def verified(self, verified: bool):
        pass

    @property
    def token(self) -> str:
        return ""

    @token.setter
    def token(self, token: str):
        pass

    @property
    def user_id(self) -> int:
        return -1

    @user_id.setter
    def user_id(self, user_id: int):
        pass

    @property
    def user(self) -> "AbstractUser":
        from app.db_classes.user.null import NullUser

        return NullUser()

    @property
    def name(self) -> str:
        return ""
    
    @name.setter
    def name(self, name: str):
        pass
