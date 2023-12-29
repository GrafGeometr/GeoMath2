from app.imports import *
from app.sqlalchemy_custom_types import *

from abc import abstractmethod
from app.db_classes.standard_model.normal import AbstractStandardModel


class AbstractContestToJudgeRelation(AbstractStandardModel):
    # --> INITIALIZE
    __abstract__ = True

    # --> PROPERTIES
    @property
    @abstractmethod
    def contest_id(self) -> int:
        pass

    @contest_id.setter
    @abstractmethod
    def contest_id(self, contest_id: int):
        pass

    @property
    @abstractmethod
    def user_id(self) -> int:
        pass

    @user_id.setter
    @abstractmethod
    def user_id(self, user_id: int):
        pass
