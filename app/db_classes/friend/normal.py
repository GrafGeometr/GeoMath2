from app.imports import *

from app.db_classes.standard_model.normal import StandardModel
from .abstract import AbstractFriend
from .null import NullFriend
from .getter import FriendGetter


class Friend(StandardModel, AbstractFriend):
    # --> INITIALIZE
    __abstract__ = False
    __tablename__ = "friend"

    friend_from_id_ = db.Column(db.Integer)
    friend_to_id_ = db.Column(db.Integer)
    accepted_ = db.Column(db.Boolean, default=False)

    null_cls_ = NullFriend
    getter_cls_ = FriendGetter

    # --> RELATIONS

    # --> FUNCTIONS
    def act_accept(self):
        self.accepted = True
        db.session.commit()
