import datetime
from typing import List

from app.imports import *
from app.sqlalchemy_custom_types import *

from app.db_classes.standard_model.null import NullStandardModel
from app.db_classes.contest_to_user_relation.abstract import (
    AbstractContestToUserRelation,
)


class NullContestToUserRelation(NullStandardModel, AbstractContestToUserRelation):
    # --> INITIALIZE
    __abstract__ = True

    # --> PROPERTIES
    @property
    def start_date(self) -> datetime.datetime:
        return datetime.datetime.min

    @start_date.setter
    def start_date(self, start_date: datetime.datetime):
        pass

    @property
    def end_date(self) -> datetime.datetime:
        return datetime.datetime.min

    @end_date.setter
    def end_date(self, end_date: datetime.datetime):
        pass

    @property
    def virtual(self) -> bool:
        pass  # TODO : decide if user is not participant of the contest, should it be virtual?

    @virtual.setter
    def virtual(self, virtual: bool):
        pass

    @property
    def contest_id(self) -> int:
        return -1

    @contest_id.setter
    def contest_id(self, contest_id: int):
        pass

    @property
    def contest(self) -> "AbstractContest":
        from app.db_classes.contest.null import NullContest

        return NullContest()

    @contest.setter
    def contest(self, contest: "AbstractContest"):
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

    @user.setter
    def user(self, user: "AbstractUser"):
        pass

    @property
    def contest_user_solutions(self) -> List["ContestUserSolution"]:
        pass

    @contest_user_solutions.setter
    def contest_user_solutions(
        self, contest_user_solutions: List["ContestUserSolution"]
    ):
        pass
