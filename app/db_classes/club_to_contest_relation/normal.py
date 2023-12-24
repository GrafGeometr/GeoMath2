from app.imports import *

from app.db_classes.standard_model.normal import StandardModel


class ClubToContestRelation(StandardModel):
    # --> INITIALIZE
    __tablename__ = "club_contest"

    # --> RELATIONS
    club_id = db.Column(db.Integer, db.ForeignKey("club.id_"))
    contest_id = db.Column(db.Integer, db.ForeignKey("contest.id_"))

    # --> FUNCTIONS
    def is_valid(self):
        from app.dbc import User_Club, User_Pool

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
            for uc in User_Club.query.filter_by(club=self.club).all()
            if uc.role.is_owner()
        ]
        contest_owners = [
            up.user
            for up in User_Pool.query.filter_by(pool=self.contest.pool).all()
            if up.role.is_owner()
        ]
        return any(clo in contest_owners for clo in club_owners)
