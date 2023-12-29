from app.imports import *
from app.sqlalchemy_custom_types import *

from abc import abstractmethod
from app.db_classes.standard_model.normal import AbstractStandardModel

class AbstractContestUserSolutionRelation(AbstractStandardModel):
    # --> INITIALIZE
    __abstract__ = True

    # --> PROPERTIES
    @property
    @abstractmethod
    def score(self) -> int:
        pass

    @score.setter
    @abstractmethod
    def score(self, score: int):
        pass

    @property
    @abstractmethod
    def content(self) -> str:
        pass

    @content.setter
    @abstractmethod
    def content(self, content: str):
        pass

    @property
    @abstractmethod
    def judge_comment(self) -> str:
        pass

    @judge_comment.setter
    @abstractmethod
    def judge_comment(self, judge_comment: str):
        pass

    @property
    @abstractmethod
    def contest_user_id(self) -> int:
        pass

    @contest_user_id.setter
    @abstractmethod
    def contest_user_id(self, contest_user_id: int):
        pass

    @property
    @abstractmethod
    def contest_problem_id(self) -> int:
        pass

    @contest_problem_id.setter
    @abstractmethod
    def contest_problem_id(self, contest_problem_id: int):
        pass

    @property
    @abstractmethod
    def contest_user_solution(self) -> "ContestUserSolution":
        pass

    @contest_user_solution.setter
    @abstractmethod
    def contest_user_solution(self, contest_user_solution: "ContestUserSolution"):
        pass