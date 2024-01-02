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
    def contest(self):
        from app.db_classes.contest.null import NullContest

        return NullContest()

    @contest.setter
    def contest(self, contest):
        pass

    @property
    def problem_id(self) -> int:
        return -1

    @problem_id.setter
    def problem_id(self, problem_id: int):
        pass

    @property
    def problem(self):
        from app.db_classes.problem.null import NullProblem

        return NullProblem()

    @problem.setter
    def problem(self, problem):
        pass

    @property
    def contest_user_solutions(self) -> List["ContestUserSolution"]:
        return []

    @contest_user_solutions.setter
    def contest_user_solutions(
        self, contest_user_solutions: List["ContestUserSolution"]
    ):
        pass

    # --> METHODS

    def act_set_list_index(self, list_index: int) -> "AbstractContestToProblemRelation":
        pass

    def act_set_max_score(self, max_score: int) -> "AbstractContestToProblemRelation":
        pass

    def is_accessible(self, user=current_user) -> bool:
        return False

    def is_valid(self) -> bool:
        return False

    def get_active_contest_user_solution(
        self, user=current_user
    ) -> "AbstractContestUserSolution":
        from app.db_classes.contest_user_solution.null import NullContestUserSolution

        return NullContestUserSolution()
