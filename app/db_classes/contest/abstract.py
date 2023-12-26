from app.imports import *
from app.sqlalchemy_custom_types import *

from abc import abstractmethod
from app.db_classes.standard_model.normal import AbstractStandardModel

class AbstractContest(AbstractStandardModel):
    # --> INITIALIZE
    __abstract__ = True
    description = db.Column(db.String)
    grade = db.Column(GradeClassType)
    start_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)
    is_public = db.Column(db.Boolean, default=False)
    rating = db.Column(db.String, default="public")  # 'public' | 'private'
    total_likes = db.Column(db.Integer, default=0)
    total_dislikes = db.Column(db.Integer, default=0)
    # --> RELATIONS
    contest_problems = db.relationship("Contest_Problem", backref="contest")
    contest_judges = db.relationship("Contest_Judge", backref="contest")
    contest_users = db.relationship("Contest_User", backref="contest")
    club_contests = db.relationship("Club_Contest", backref="contest")
    pool_id = db.Column(db.Integer, db.ForeignKey("pool.id_"))
    olimpiad_id = db.Column(db.Integer, db.ForeignKey("olimpiad.id_"))
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
    def contest_problems(self) -> list("ContestToProblemRelation"):
        pass

    @contest_problems.setter
    @abstractmethod
    def contest_problems(self, contest_problems: list["ContestToProblemRelation"]):
        pass

    @property
    @abstractmethod
    def contest_judges(self) -> list("ContestToJudgeRelation"):
        pass

    @contest_judges.setter
    @abstractmethod
    def contest_judges(self, contest_judges: list["ContestToJudgeRelation"]):
        pass

    @property
    @abstractmethod
    def contest_users(self) -> list("ContestToUserRelation"):
        pass

    @contest_users.setter
    @abstractmethod
    def contest_users(self, contest_users: list["ContestToUserRelation"]):
        pass

    @property
    @abstractmethod
    def club_contests(self) -> list["ClubToContestRelation"]:
        pass

    @club_contests.setter
    @abstractmethod
    def club_contests(self, club_contests: list["ClubToContestRelation"]):
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