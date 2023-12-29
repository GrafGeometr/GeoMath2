import datetime
from typing import List

from app.imports import *
from app.sqlalchemy_custom_types import *

from app.db_classes.standard_model.null import NullStandardModel
from app.db_classes.contest.abstract import AbstractContest


class NullContest(NullStandardModel, AbstractContest):
    # --> INITIALIZE
    __abstract__ = True

    # --> PROPERTIES
    @property
    def description(self) -> str:
        return ""

    @description.setter
    def description(self, description: str):
        pass

    @property
    def grade(self) -> GradeClassType:
        return None  # TODO : null class?

    @grade.setter
    def grade(self, grade: GradeClassType):
        pass

    @property
    def start_date(self) -> datetime.datetime:
        return datetime.datetime.min

    @start_date.setter
    def start_date(self, start_date: datetime.datetime):
        pass

    @property
    def end_date(self) -> datetime.datetime:
        return datetime.datetime.min

    @end_date.setter
    def end_date(self, end_date: datetime.datetime):
        pass

    @property
    def is_public(self) -> bool:
        return False  # TODO : decide what to return

    @is_public.setter
    def is_public(self, is_public: bool):
        pass

    @property
    def rating(self) -> str:
        return "private"

    @rating.setter
    def rating(self, rating: str):
        pass

    @property
    def total_likes(self) -> int:
        return 0

    @total_likes.setter
    def total_likes(self, total_likes: int):
        pass

    @property
    def total_dislikes(self) -> int:
        return 0

    @total_dislikes.setter
    def total_dislikes(self, total_dislikes: int):
        pass

    @property
    def contest_problems(self) -> List["ContestToProblemRelation"]:
        return []

    @contest_problems.setter
    def contest_problems(self, contest_problems: List["ContestToProblemRelation"]):
        pass

    @property
    def contest_judges(self) -> List["ContestToJudgeRelation"]:
        return []

    @contest_judges.setter
    def contest_judges(self, contest_judges: List["ContestToJudgeRelation"]):
        pass

    @property
    def contest_users(self) -> List["ContestToUserRelation"]:
        return []

    @contest_users.setter
    def contest_users(self, contest_users: List["ContestToUserRelation"]):
        pass

    @property
    def club_contests(self) -> List["ClubToContestRelation"]:
        return []

    @club_contests.setter
    def club_contests(self, club_contests: List["ClubToContestRelation"]):
        pass

    @property
    def pool_id(self) -> int:
        return -1

    @pool_id.setter
    def pool_id(self, pool_id: int):
        pass

    @property
    def pool(self) -> "AbstractPool":
        from app.db_classes.pool.null import NullPool

        return NullPool()

    @pool.setter
    def pool(self, pool: "AbstractPool"):
        pass

    @property
    def olimpiad_id(self) -> int:
        return -1

    @olimpiad_id.setter
    def olimpiad_id(self, olimpiad_id: int):
        pass

    @property
    def olimpiad(self) -> "AbstractOlimpiad":
        from app.db_classes.olimpiad.null import NullOlimpiad

        return NullOlimpiad()

    @olimpiad.setter
    def olimpiad(self, olimpiad: "AbstractOlimpiad"):
        pass
