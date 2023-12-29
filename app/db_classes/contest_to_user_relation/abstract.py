from typing import List

from app.imports import *
from app.sqlalchemy_custom_types import *

from abc import abstractmethod
from app.db_classes.standard_model.normal import AbstractStandardModel


class AbstractContestToUserRelation(AbstractStandardModel):
    # --> INITIALIZE
    __abstract__ = True

    # --> PROPERTIES
    @property
    @abstractmethod
    def start_date(self) -> datetime.datetime:
        pass

    @start_date.setter
    @abstractmethod
    def start_date(self, start_date: datetime.datetime):
        pass

    @property
    @abstractmethod
    def end_date(self) -> datetime.datetime:
        pass

    @end_date.setter
    @abstractmethod
    def end_date(self, end_date: datetime.datetime):
        pass

    @property
    @abstractmethod
    def virtual(self) -> bool:
        pass

    @virtual.setter
    @abstractmethod
    def virtual(self, virtual: bool):
        pass

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

    @property
    @abstractmethod
    def contest_user_solutions(self) -> List["ContestUserSolution"]:
        pass

    @contest_user_solutions.setter
    @abstractmethod
    def contest_user_solutions(
        self, contest_user_solutions: List["ContestUserSolution"]
    ):
        pass
