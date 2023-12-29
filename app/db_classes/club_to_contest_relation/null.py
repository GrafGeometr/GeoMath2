from app.imports import *
from app.sqlalchemy_custom_types import *

from app.db_classes.standard_model.null import NullStandardModel
from app.db_classes.club_to_contest_relation.abstract import (
    AbstractClubToContestRelation,
)


class NullClubToContestRelation(NullStandardModel, AbstractClubToContestRelation):
    # --> INITIALIZE
    __abstract__ = True

    # --> PROPERTIES
    @property
    def club_id(self) -> int:
        return -1

    @club_id.setter
    def club_id(self, club_id: int):
        pass

    @property
    def club(self) -> "AbstractClub":
        from app.db_classes.club.null import NullClub

        return NullClub()

    @club.setter
    def club(self, club: "AbstractClub"):
        pass

    @property
    def contest_id(self) -> int:
        return -1

    @contest_id.setter
    def contest_id(self, contest_id: int):
        pass

    @property
    def contest(self) -> "AbstractContest":
        from app.db_classes.contest.null import NullContest

        return NullContest()

    @contest.setter
    def contest(self, contest: "AbstractContest"):
        pass
