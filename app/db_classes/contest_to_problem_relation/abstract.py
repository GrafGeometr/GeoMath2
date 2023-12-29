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
    def problem_id(self) -> int:
        pass

    @problem_id.setter
    @abstractmethod
    def problem_id(self, problem_id: int):
        pass

    @property
    @abstractmethod
    def contest_user_solutions(self) -> list("ContestUserSolution"):
        pass

    @contest_user_solutions.setter
    @abstractmethod
    def contest_user_solutions(self, contest_user_solutions: list("ContestUserSolution")):
        pass