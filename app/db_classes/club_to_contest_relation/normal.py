from app.imports import *
from app.sqlalchemy_custom_types import *

from app.db_classes.standard_model.normal import StandardModel
from .abstract import AbstractClubToContestRelation
from .null import NullClubToContestRelation
from .getter import ClubToContestRelationGetter


class ClubToContestRelation(StandardModel):
    # --> INITIALIZE
    __abstract__ = False
    __tablename__ = "club_to_contest_relation"

    null_cls_ = NullClubToContestRelation
    getter_cls_ = ClubToContestRelationGetter

    # --> RELATIONS
    club_id_ = db.Column(db.Integer, db.ForeignKey("club.id_"))
    contest_id_ = db.Column(db.Integer, db.ForeignKey("contest.id_"))

    # --> PROPERTIES
    @property
    def club_id(self) -> int:
        return self.club_id_

    @club_id.setter
    def club_id(self, club_id: int):
        self.club_id_ = club_id
        self.save()

    @property
    def contest_id(self) -> int:
        return self.contest_id_

    @contest_id.setter
    def contest_id(self, contest_id: int):
        self.contest_id_ = contest_id
        self.save()

    # --> FUNCTIONS
    def is_valid(self):
        from app.dbc import UserToClubRelation, UserToPoolRelation

        if (
                (self.contest is None)
                or (self.club is None)
                or (self.contest.pool is None)
                or self.contest.pool is None
        ):
            return False
        if self.contest.is_archived():
            return True
        club_owners = [
            uc.user
            for uc in UserToClubRelation.get.by_club(self.club).all()
            if uc.role.is_owner()
        ]
        contest_owners = [
            up.user
            for up in UserToPoolRelation.get.by_pool(self.contest.pool).all()
            if up.role.is_owner()
        ]
        return any(clo in contest_owners for clo in club_owners)
