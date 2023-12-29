from app.imports import *
from app.sqlalchemy_custom_types import *


from app.db_classes.standard_model.null import NullStandardModel
from app.db_classes.contest_to_judge_relation.abstract import (
    AbstractContestToJudgeRelation,
)


class NullContestToJudgeRelation(NullStandardModel, AbstractContestToJudgeRelation):
    # --> INITIALIZE
    __abstract__ = True

    # --> PROPERTIES
    @property
    def contest_id(self) -> int:
        return -1

    @contest_id.setter
    def contest_id(self, contest_id: int):
        pass

    @property
    def user(self) -> "AbstractUser":
        from app.db_classes.user.null import NullUser

        return NullUser()

    @user.setter
    def user(self, user: "AbstractUser"):
        pass

    @property
    def user_id(self) -> int:
        return -1

    @user_id.setter
    def user_id(self, user_id: int):
        pass

    @property
    def contest(self) -> "AbstractContest":
        from app.db_classes.contest.null import NullContest

        return NullContest()

    @contest.setter
    def contest(self, contest: "AbstractContest"):
        pass
