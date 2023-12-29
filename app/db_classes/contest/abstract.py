from typing import List

from app.imports import *
from app.sqlalchemy_custom_types import *

from abc import abstractmethod
from app.db_classes.standard_model.normal import AbstractStandardModel


class AbstractContest(AbstractStandardModel):
    # --> INITIALIZE
    __abstract__ = True

    # --> PROPERTIES
    @property
    @abstractmethod
    def description(self) -> str:
        pass

    @description.setter
    @abstractmethod
    def description(self, description: str):
        pass

    @property
    @abstractmethod
    def grade(self) -> GradeClassType:
        pass

    @grade.setter
    @abstractmethod
    def grade(self, grade: GradeClassType):
        pass

    @property
    @abstractmethod
    def start_date(self) -> datetime.datetime:
        pass

    @start_date.setter
    @abstractmethod
    def start_date(self, start_date: datetime.datetime):
        pass

    @property
    @abstractmethod
    def end_date(self) -> datetime.datetime:
        pass

    @end_date.setter
    @abstractmethod
    def end_date(self, end_date: datetime.datetime):
        pass

    @property
    @abstractmethod
    def is_public(self) -> bool:
        pass

    @is_public.setter
    @abstractmethod
    def is_public(self, is_public: bool):
        pass

    @property
    @abstractmethod
    def rating(self) -> str:
        pass

    @rating.setter
    @abstractmethod
    def rating(self, rating: str):
        pass

    @property
    @abstractmethod
    def total_likes(self) -> int:
        pass

    @total_likes.setter
    @abstractmethod
    def total_likes(self, total_likes: int):
        pass

    @property
    @abstractmethod
    def total_dislikes(self) -> int:
        pass

    @total_dislikes.setter
    @abstractmethod
    def total_dislikes(self, total_dislikes: int):
        pass

    @property
    @abstractmethod
    def contest_problems(self) -> List["ContestToProblemRelation"]:
        pass

    @contest_problems.setter
    @abstractmethod
    def contest_problems(self, contest_problems: List["ContestToProblemRelation"]):
        pass

    @property
    @abstractmethod
    def contest_judges(self) -> List["ContestToJudgeRelation"]:
        pass

    @contest_judges.setter
    @abstractmethod
    def contest_judges(self, contest_judges: List["ContestToJudgeRelation"]):
        pass

    @property
    @abstractmethod
    def contest_users(self) -> List["ContestToUserRelation"]:
        pass

    @contest_users.setter
    @abstractmethod
    def contest_users(self, contest_users: List["ContestToUserRelation"]):
        pass

    @property
    @abstractmethod
    def club_contests(self) -> List["ClubToContestRelation"]:
        pass

    @club_contests.setter
    @abstractmethod
    def club_contests(self, club_contests: List["ClubToContestRelation"]):
        pass

    @property
    @abstractmethod
    def pool_id(self) -> int:
        pass

    @pool_id.setter
    @abstractmethod
    def pool_id(self, pool_id: int):
        pass

    @property
    @abstractmethod
    def olimpiad_id(self) -> int:
        pass

    @olimpiad_id.setter
    @abstractmethod
    def olimpiad_id(self, olimpiad_id: int):
        pass
