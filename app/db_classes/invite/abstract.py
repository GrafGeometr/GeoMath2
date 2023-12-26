from app.imports import *
from app.sqlalchemy_custom_types import *

from abc import abstractmethod
from app.db_classes.standard_model.normal import AbstractStandardModel


class AbstractInvite(AbstractStandardModel):
    code = db.Column(db.String, unique=True, nullable=True)
    expired_at = db.Column(db.DateTime)
    parent_type = db.Column(DbParentType)
    # parent_type = db.Column(db.String)  # 'Pool', 'Club'
    parent_id = db.Column(db.Integer)

    
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
    def parent_type(self) -> str:
        pass

    @parent_type.setter
    @abstractmethod
    def parent_type(self, parent_type: "DbParentType"):
        pass

    @property
    @abstractmethod
    def parent_id(self) -> int:
        pass

    @parent_id.setter
    @abstractmethod
    def parent_id(self, parent_id: int):
        pass