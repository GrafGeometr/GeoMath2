from app.imports import *
from app.sqlalchemy_custom_types import *


class Friend(db.Model):
    # --> INITIALIZE
    __tablename__ = "friend"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    friend_from = db.Column(db.Integer)
    friend_to = db.Column(db.Integer)
    accepted = db.Column(db.Boolean, default=False)
    # --> RELATIONS

    # --> FUNCTIONS
    def add(self):
        db.session.add(self)
        db.session.commit()
        return self

    def remove(self):
        db.session.delete(self)
        db.session.commit()

    def act_accept(self):
        self.accepted = True
        db.session.commit()
