from typing import List, Tuple

from app.imports import *
from app.sqlalchemy_custom_types import *

from abc import abstractmethod
from app.db_classes.standard_model.abstract import AbstractStandardModel


class AbstractContest(AbstractStandardModel):
    # --> INITIALIZE
    __abstract__ = True

    # --> PROPERTIES
    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @name.setter
    @abstractmethod
    def name(self, name: str):
        pass

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
    def pool(self) -> "AbstractPool":
        pass

    @pool.setter
    @abstractmethod
    def pool(self, pool: "AbstractPool"):
        pass

    @property
    @abstractmethod
    def olimpiad_id(self) -> int:
        pass

    @olimpiad_id.setter
    @abstractmethod
    def olimpiad_id(self, olimpiad_id: int):
        pass

    @property
    @abstractmethod
    def olimpiad(self) -> "AbstractOlimpiad":
        pass

    @olimpiad.setter
    @abstractmethod
    def olimpiad(self, olimpiad: "AbstractOlimpiad"):
        pass

    @property
    @abstractmethod
    def date(self) -> Tuple[datetime.datetime, datetime.datetime]:
        pass

    @date.setter
    @abstractmethod
    def date(self, date: Tuple[datetime.datetime, datetime.datetime]):
        pass

    # --> METHODS
    @abstractmethod
    def is_liked(self, user=current_user) -> bool:
        pass

    @abstractmethod
    def act_add_like(self, user=current_user) -> "AbstractContest":
        pass

    @abstractmethod
    def act_remove_like(self, user=current_user) -> "AbstractContest":
        pass

    @abstractmethod
    def is_rating_public(self) -> bool:
        pass

    @abstractmethod
    def is_rating_private(self) -> bool:
        pass

    @abstractmethod
    def is_archived(self) -> bool:
        pass

    @abstractmethod
    def is_description_available(self) -> bool:
        pass

    @abstractmethod
    def is_my(self, user=current_user) -> bool:
        pass

    @abstractmethod
    def is_started(self) -> bool:
        pass

    @abstractmethod
    def is_ended(self) -> bool:
        pass

    @abstractmethod
    def is_rating_available(self) -> bool:
        pass

    @abstractmethod
    def is_problem_submitted(self, problem) -> bool:
        pass

    @abstractmethod
    def is_tags_available(self) -> bool:
        pass

    @abstractmethod
    def get_all_likes(self) -> List["Like"]:
        pass

    @abstractmethod
    def get_all_good_likes(self) -> List["Like"]:
        pass

    @abstractmethod
    def get_all_bad_likes(self) -> List["Like"]:
        pass

    @abstractmethod
    def get_problems(self) -> List["Problem"]:
        pass

    @abstractmethod
    def get_judges(self) -> List["User"]:
        pass

    @abstractmethod
    def get_nonsecret_contest_problems(self) -> List["ContestToProblemRelation"]:
        pass

    @abstractmethod
    def get_nonsecret_problems(self) -> List["Problem"]:
        pass

    @abstractmethod
    def get_active_cu(self, user=current_user) -> "ContestToUserRelation":
        pass

    @abstractmethod
    def get_idx_by_contest_problem(self, contest_problem) -> int:
        pass

    @abstractmethod
    def get_cu_by_mode_and_part(
        self, mode="all", part="real", user=current_user, club=None
    ) -> "ContestToUserRelation":
        pass

    @abstractmethod
    def get_rating_table(self, all_cu):
        pass

    @abstractmethod
    def act_set_date(self, start_date, end_date) -> "AbstractContest":
        pass

    @abstractmethod
    def act_register(
        self, user=current_user, mode="all", start_date=None, end_date=None
    ) -> "AbstractContest":
        pass

    @abstractmethod
    def act_stop(self, user=current_user) -> "AbstractContest":
        pass

    @abstractmethod
    def act_add_judge(self, user) -> "AbstractContest":
        pass

    @abstractmethod
    def act_add_judge_by_name(self, name) -> "AbstractContest":
        pass

    @abstractmethod
    def act_remove_judge(self, user) -> "AbstractContest":
        pass

    @abstractmethod
    def act_remove_judge_by_name(self, name) -> "AbstractContest":
        pass

    @abstractmethod
    def act_set_judges(self, judges) -> "AbstractContest":
        pass

    @abstractmethod
    def act_remove_problem(self, problem) -> "AbstractContest":
        pass

    @abstractmethod
    def act_add_problem(self, problem) -> "AbstractContest":
        pass

    @abstractmethod
    def act_add_problem_by_hashed_id(self, hashed_id) -> "AbstractContest":
        pass

    @abstractmethod
    def act_set_problem_score(self, problem, score) -> "AbstractContest":
        pass

    @abstractmethod
    def act_set_problem_score_by_hashed_id(self, hashed_id, score) -> "AbstractContest":
        pass

    @abstractmethod
    def act_set_problems(self, hashes, scores) -> "AbstractContest":
        pass

    @abstractmethod
    def act_set_rating_public(self) -> "AbstractContest":
        pass

    @abstractmethod
    def act_set_rating_private(self) -> "AbstractContest":
        pass

    @abstractmethod
    def act_toggle_rating(self, mode) -> "AbstractContest":
        pass

    @abstractmethod
    def get_tags(self) -> List["Tag"]:
        pass

    @abstractmethod
    def get_tag_names(self) -> List[str]:
        pass

    @abstractmethod
    def is_have_tag(self, tag) -> bool:
        pass

    @abstractmethod
    def act_add_tag(self, tag) -> "AbstractContest":
        pass

    @abstractmethod
    def act_add_tags(self, tags) -> "AbstractContest":
        pass

    def act_add_tag_by_name(self, tag_name) -> "AbstractContest":
        pass

    @abstractmethod
    def act_remove_tag(self, tag) -> "AbstractContest":
        pass

    @abstractmethod
    def act_remove_tag_by_name(self, tag_name) -> "AbstractContest":
        pass

    @abstractmethod
    def act_set_tags(self, tags) -> "AbstractContest":
        pass
