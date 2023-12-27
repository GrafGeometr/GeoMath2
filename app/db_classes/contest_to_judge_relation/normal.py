from app.imports import *

from app.db_classes.standard_model.normal import StandardModel
from .abstract import AbstractContestToJudgeRelation
from .null import NullContestToJudgeRelation
from .getter import ContestToJudgeRelationGetter


class ContestToJudgeRelation(StandardModel):
    # --> INITIALIZE
    __abstract__ = False
    __tablename__ = "contest_judge"

    null_cls_ = NullContestToJudgeRelation
    getter_cls_ = ContestToJudgeRelationGetter

    # --> RELATIONS
    contest_id_ = db.Column(db.Integer, db.ForeignKey("contest.id_"))
    user_id_ = db.Column(db.Integer, db.ForeignKey("user.id_"))

    # --> FUNCTIONS
    @property
    def contest_id(self) -> int:
        return self.contest_id_

    @contest_id.setter
    def contest_id(self, contest_id: int):
        self.contest_id_ = contest_id
        self.save()

    @property
    def user_id(self) -> int:
        return self.user_id_

    @user_id.setter
    def user_id(self, user_id: int):
        self.user_id_ = user_id
        self.save()

    @staticmethod
    def get_by_contest_and_user(contest, user):
        return ContestToJudgeRelation.get.by_contest(contest).by_user(user).first()
