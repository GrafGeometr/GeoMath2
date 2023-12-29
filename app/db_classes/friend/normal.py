from app.imports import *

from app.db_classes.standard_model.normal import StandardModel
from .abstract import AbstractFriend
from .null import NullFriend
from .getter import FriendGetter


class Friend(StandardModel):
    # --> INITIALIZE
    __tablename__ = "friend"

    friend_from = db.Column(db.Integer)
    friend_to = db.Column(db.Integer)
    accepted = db.Column(db.Boolean, default=False)

    # --> RELATIONS

    # --> FUNCTIONS
    def act_accept(self):
        self.accepted = True
        db.session.commit()
