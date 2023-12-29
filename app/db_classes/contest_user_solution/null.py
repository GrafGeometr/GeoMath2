from app.imports import *
from app.sqlalchemy_custom_types import *

from app.db_classes.standard_model.null import NullStandardModel
from app.db_classes.contest_user_solution.abstract import AbstractContestUserSolution


class NullContestUserSolution(NullStandardModel, AbstractContestUserSolution):
    # --> INITIALIZE
    __abstract__ = True

    # --> PROPERTIES
    @property
    def score(self) -> int:
        return 0

    @score.setter
    def score(self, score: int):
        pass

    @property
    def content(self) -> str:
        return ""

    @content.setter
    def content(self, content: str):
        pass

    @property
    def judge_comment(self) -> str:
        return ""

    @judge_comment.setter
    def judge_comment(self, judge_comment: str):
        pass

    @property
    def contest_to_user_relation_id(self) -> int:
        return -1

    @contest_to_user_relation_id.setter
    def contest_to_user_relation_id(self, contest_to_user_relation_id: int):
        pass

    @property
    def contest_to_user_relation(self) -> "ContestToUserRelation":
        from app.db_classes.contest_to_user_relation.null import (
            NullContestToUserRelation,
        )

        return NullContestToUserRelation()

    @contest_to_user_relation.setter
    def contest_to_user_relation(
        self, contest_to_user_relation: "ContestToUserRelation"
    ):
        pass

    @property
    def contest_to_problem_relation_id(self) -> int:
        return -1

    @contest_to_problem_relation_id.setter
    def contest_to_problem_relation_id(self, contest_to_problem_relation_id: int):
        pass

    @property
    def contest_to_problem_relation(self) -> "ContestToProblemRelation":
        from app.db_classes.contest_to_problem_relation.null import (
            NullContestToProblemRelation,
        )

        return NullContestToProblemRelation()

    @contest_to_problem_relation.setter
    def contest_to_problem_relation(
        self, contest_to_problem_relation: "ContestToProblemRelation"
    ):
        pass
