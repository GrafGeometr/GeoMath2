import datetime

from app.imports import *
from app.sqlalchemy_custom_types import *

from app.db_classes.standard_model.normal import NullStandardModel
from app.db_classes.invite.abstract import AbstractInvite


class NullInvite(NullStandardModel, AbstractInvite):
    # --> INITIALIZE
    __abstract__ = True

    # --> PROPERTIES
    @property
    def code(self) -> str:
        return ""

    @code.setter
    def code(self, code: str):
        pass

    @property
    def expired_at(self) -> datetime:
        return datetime.datetime.min

    @expired_at.setter
    def expired_at(self, expired_at: datetime):
        pass

    @property
    def parent_type(self) -> "DbParent":
        return None

    @parent_type.setter
    def parent_type(self, parent_type: "DbParent"):
        pass

    @property
    def parent_id(self) -> int:
        return -1

    @parent_id.setter
    def parent_id(self, parent_id: int):
        pass

    # --> METHODS
    def is_expired(self) -> bool:
        return True

    def act_check_expired(self):
        pass

    @staticmethod
    def generate_code() -> str:
        pass  # TODO return empty string or a valid code?

    def act_set_expired_at(self):
        pass

    @staticmethod
    def act_refresh_all():
        pass

    def get_parent(self) -> "AbstractStandardModel":
        return None  # TODO : decide what to return

    def is_from_parent(self, obj: "AbstractStandardModel") -> bool:
        return False
