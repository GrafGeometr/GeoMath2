from app.imports import *
from app.sqlalchemy_custom_types import *

from abc import abstractmethod
from app.db_classes.standard_model.normal import AbstractStandardModel


class AbstractInvite(AbstractStandardModel):
    # --> INITIALIZE
    __abstract__ = True

    # --> PROPERTIES
    @property
    @abstractmethod
    def code(self) -> str:
        pass

    @code.setter
    @abstractmethod
    def code(self, code: str):
        pass

    @property
    @abstractmethod
    def expired_at(self) -> datetime:
        pass

    @expired_at.setter
    @abstractmethod
    def expired_at(self, expired_at: datetime):
        pass

    @property
    @abstractmethod
    def parent_type(self) -> "DbParent":
        pass

    @parent_type.setter
    @abstractmethod
    def parent_type(self, parent_type: "DbParent"):
        pass

    @property
    @abstractmethod
    def parent_id(self) -> int:
        pass

    @parent_id.setter
    @abstractmethod
    def parent_id(self, parent_id: int):
        pass

    # --> METHODS
    @abstractmethod
    def is_expired(self) -> bool:
        pass

    @abstractmethod
    def act_check_expired(self):
        pass

    @staticmethod
    @abstractmethod
    def generate_code() -> str:
        pass

    @abstractmethod
    def act_set_expired_at(self):
        pass

    @staticmethod
    @abstractmethod
    def act_refresh_all():
        pass

    @abstractmethod
    def get_parent(self) -> "AbstractStandardModel":
        pass

    @abstractmethod
    def is_from_parent(self, obj: "AbstractStandardModel") -> bool:
        pass
