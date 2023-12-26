from app.imports import *

from app.db_classes.standard_model.normal import StandardModel
from app.db_classes.user_to_chat_relation.abstract import AbstractUserToChatRelation
from app.db_classes.user_to_club_relation.null import NullUserToClubRelation
from app.db_classes.user_to_chat_relation.getter import UserToChatRelationGetter


class UserToChatRelation(StandardModel, AbstractUserToChatRelation):
    # --> INITIALIZE
    __abstract__ = False
    __tablename__ = "user_chat"

    # --> RELATIONS
    user_id_ = db.Column(db.Integer, db.ForeignKey("user.id_"))
    chat_id_ = db.Column(db.Integer, db.ForeignKey("chat.id_"))
    messages_ = db.relationship(
        "Message", backref="user_chat_"
    )  # TODO check all backrefs

    null_cls_ = NullUserToClubRelation
    getter_cls_ = UserToChatRelationGetter

    # --> PROPERTIES
    @property
    def user_id(self):
        return self.user_id_

    @user_id.setter
    def user_id(self, value):
        self.user_id_ = value
        self.save()

    @property
    def chat_id(self):
        return self.chat_id_

    @chat_id.setter
    def chat_id(self, value):
        self.chat_id_ = value
        self.save()

    @property
    def messages(self):
        return self.messages_

    @messages.setter
    def messages(self, value):
        self.messages_ = value
        self.save()

    # --> METHODS
    def is_owner(self):
        if self.chat.club is None:
            return True

        return self.user.get_club_relation(self.chat.club.id).role.is_owner()

    def is_participant(self):
        if self.chat.club is None:
            return False

        return self.user.get_club_relation(self.chat.club.id).role.is_participant()

    def remove(self):
        for m in self.messages:
            m.remove()
        db.session.delete(self)
        db.session.commit()
