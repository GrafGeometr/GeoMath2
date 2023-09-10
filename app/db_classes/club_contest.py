from app.imports import *
from app.sqlalchemy_custom_types import *


class Club_Contest(db.Model):
    # --> INITIALIZE
    __tablename__ = "club_contest"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    # --> RELATIONS
    club_id = db.Column(db.Integer, db.ForeignKey("club.id"))
    contest_id = db.Column(db.Integer, db.ForeignKey("contest.id"))

    # --> FUNCTIONS
    def add(self):
        db.session.add(self)
        db.session.commit()

    def remove(self):
        db.session.delete(self)
        db.session.commit()

    def is_valid(self):
        from app.dbc import User_Club, User_Pool
        if (self.contest is None) or (self.club is None) or (self.contest.pool is None) or self.contest.pool is None:
            return False
        if self.contest.is_archived():
            return True
        club_owners = [uc.user for uc in User_Club.query.filter_by(club=self.club).all() if uc.role.isOwner()]
        contest_owners = [up.user for up in User_Pool.query.filter_by(pool=self.contest.pool).all() if up.role.isOwner()]
        return any(clo in contest_owners for clo in club_owners)