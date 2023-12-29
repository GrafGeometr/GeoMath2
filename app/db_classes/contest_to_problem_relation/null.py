from typing import List

from app.imports import *
from app.sqlalchemy_custom_types import *


from app.db_classes.standard_model.null import NullStandardModel
from app.db_classes.contest_to_problem_relation.abstract import (
    AbstractContestToProblemRelation,
)


class NullContestToProblemRelation(NullStandardModel, AbstractContestToProblemRelation):
    # --> INITIALIZE
    __abstract__ = True

    # --> PROPERTIES
    @property
    def max_score(self) -> int:
        return 0

    @max_score.setter
    def max_score(self, max_score: int):
        pass

    @property
    def list_index(self) -> int:
        return 0  # TODO decide what to return here

    @list_index.setter
    def list_index(self, list_index: int):
        pass

    @property
    def contest_id(self) -> int:
        return -1

    @contest_id.setter
    def contest_id(self, contest_id: int):
        pass

    @property
    def problem_id(self) -> int:
        return -1

    @problem_id.setter
    def problem_id(self, problem_id: int):
        pass

    @property
    def contest_user_solutions(self) -> List["ContestUserSolution"]:
        return []

    @contest_user_solutions.setter
    def contest_user_solutions(
        self, contest_user_solutions: List["ContestUserSolution"]
    ):
        pass
