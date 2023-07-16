from app.imports import *
from app.sqlalchemy_custom_types import *


class User_Club(db.Model):
    # --> INITIALIZE
    __tablename__ = "user_club"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    role = db.Column(RoleType)

    # --> RELATIONS
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    club_id = db.Column(db.Integer, db.ForeignKey("club.id"))

    # --> FUNCTIONS
    def add(self):
        db.session.add(self)
        db.session.commit()

    def remove(self):
        db.session.delete(self)
        db.session.commit()
    