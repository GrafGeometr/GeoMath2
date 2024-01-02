from typing import List

from app.imports import *
from app.sqlalchemy_custom_types import *

from abc import abstractmethod
from app.db_classes.standard_model.normal import AbstractStandardModel


class AbstractContestToProblemRelation(AbstractStandardModel):
    # --> INITIALIZE
    __abstract__ = True

    # --> PROPERTIES
    @property
    @abstractmethod
    def max_score(self) -> int:
        pass

    @max_score.setter
    @abstractmethod
    def max_score(self, max_score: int):
        pass

    @property
    @abstractmethod
    def list_index(self) -> int:
        pass

    @list_index.setter
    @abstractmethod
    def list_index(self, list_index: int):
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
    def contest(self) -> "AbstractContest":
        pass

    @contest.setter
    @abstractmethod
    def contest(self, contest: "AbstractContest"):
        pass

    @property
    @abstractmethod
    def problem_id(self) -> int:
        pass

    @problem_id.setter
    @abstractmethod
    def problem_id(self, problem_id: int):
        pass

    @property
    @abstractmethod
    def problem(self) -> "AbstractProblem":
        pass

    @problem.setter
    @abstractmethod
    def problem(self, problem: "AbstractProblem"):
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

    # --> METHODS

    @abstractmethod
    def act_set_list_index(self, list_index: int) -> "AbstractContestToProblemRelation":
        pass

    @abstractmethod
    def act_set_max_score(self, max_score: int) -> "AbstractContestToProblemRelation":
        pass

    @abstractmethod
    def is_accessible(self, user=current_user) -> bool:
        pass

    @abstractmethod
    def is_valid(self) -> bool:
        pass

    @abstractmethod
    def get_active_contest_user_solution(
        self, user=current_user
    ) -> "AbstractContestUserSolution":
        pass
