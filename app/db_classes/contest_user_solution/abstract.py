from app.imports import *
from app.sqlalchemy_custom_types import *

from abc import abstractmethod
from app.db_classes.standard_model.normal import AbstractStandardModel


class AbstractContestUserSolution(AbstractStandardModel):
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
    def contest_to_user_relation_id(self) -> int:
        pass

    @contest_to_user_relation_id.setter
    @abstractmethod
    def contest_to_user_relation_id(self, contest_to_user_relation_id: int):
        pass

    @property
    @abstractmethod
    def contest_to_user_relation(self) -> "ContestToUserRelation":
        pass

    @contest_to_user_relation.setter
    @abstractmethod
    def contest_to_user_relation(
        self, contest_to_user_relation: "ContestToUserRelation"
    ):
        pass

    @property
    @abstractmethod
    def contest_to_problem_relation_id(self) -> int:
        pass

    @contest_to_problem_relation_id.setter
    @abstractmethod
    def contest_to_problem_relation_id(self, contest_to_problem_relation_id: int):
        pass

    @property
    @abstractmethod
    def contest_to_problem_relation(self) -> "ContestToProblemRelation":
        pass

    @contest_to_problem_relation.setter
    @abstractmethod
    def contest_to_problem_relation(
        self, contest_to_problem_relation: "ContestToProblemRelation"
    ):
        pass
