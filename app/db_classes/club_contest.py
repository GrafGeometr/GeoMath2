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