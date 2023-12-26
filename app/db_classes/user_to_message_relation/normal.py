from app.imports import *

from app.db_classes.standard_model.normal import StandardModel
from app.db_classes.user_to_message_relation.abstract import (
    AbstractUserToMessageRelation,
)
from app.db_classes.user_to_message_relation.null import NullUserToMessageRelation
from app.db_classes.user_to_message_relation.getter import UserToMessageRelationGetter


class UserToMessageRelation(StandardModel, AbstractUserToMessageRelation):
    # --> INITIALIZE
    __tablename__ = "user_message"

    read_ = db.Column(db.Boolean)

    # --> RELATIONS
    user_id_ = db.Column(db.Integer, db.ForeignKey("user.id_"))
    message_id_ = db.Column(db.Integer, db.ForeignKey("message.id_"))

    null_cls_ = NullUserToMessageRelation
    getter_cls_ = UserToMessageRelationGetter

    # --> PROPERTIES
    @property
    def read(self):
        return self.read_

    @read.setter
    def read(self, value):
        self.read_ = value
        self.save()

    @property
    def user_id(self):
        return self.user_id_

    @user_id.setter
    def user_id(self, value):
        self.user_id_ = value
        self.save()

    @property
    def message_id(self):
        return self.message_id_

    @message_id.setter
    def message_id(self, value):
        self.message_id_ = value
        self.save()

    # --> METHODS
    def is_read(self):
        return self.read

    def act_mark_as_read(self):
        self.read = True
        return self

    def act_mark_as_unread(self):
        self.read = False
        return self
