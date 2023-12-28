from typing import List

from app.imports import *

from app.db_classes.standard_model.normal import StandardModel
from app.db_classes.message.abstract import AbstractMessage
from app.db_classes.message.null import NullMessage
from app.db_classes.message.getter import MessageGetter


class Message(StandardModel, AbstractMessage):
    # --> INITIALIZE
    __abstract__ = False
    __tablename__ = "message"

    content_ = db.Column(db.String)
    date_ = db.Column(db.DateTime)

    null_cls_ = NullMessage
    getter_cls_ = MessageGetter

    # --> RELATIONS
    user_to_chat_relation_id_ = db.Column(db.Integer, db.ForeignKey("user_chat.id_"))
    user__to_message_relations_ = db.relationship(
        "UserToMessageRelation", backref="message_"
    )

    # --> PROPERTIES
    @property
    def content(self) -> str:
        return self.content_

    @content.setter
    def content(self, value: str):
        self.content_ = value
        self.save()

    @property
    def date(self) -> "datetime.datetime":
        return self.date_

    @date.setter
    def date(self, value: "datetime.datetime"):
        self.date_ = value
        self.save()

    @property
    def user_to_chat_relation_id(self) -> int:
        return self.user_to_chat_relation_id_

    @user_to_chat_relation_id.setter
    def user_to_chat_relation_id(self, value: int):
        self.user_to_chat_relation_id_ = value
        self.save()

    @property
    def user_to_chat_relation(self) -> "AbstractUserToChatRelation":
        return self.user_to_chat_relation_

    @user_to_chat_relation.setter
    def user_to_chat_relation(self, value: "AbstractUserToChatRelation"):
        self.user_to_chat_relation_ = value
        self.save()

    @property
    def user_to_message_relations(self) -> List["UserToMessageRelation"]:
        return self.user_messages_

    @user_to_message_relations.setter
    def user_to_message_relations(self, value: List["UserToMessageRelation"]):
        self.user__to_message_relations_ = value
        self.save()

    # --> FUNCTIONS
    def add(self):
        from app.db_classes.user_to_message_relation.normal import UserToMessageRelation

        db.session.add(self)
        db.session.commit()
        self.date = current_time()
        self.content = self.content.replace("\n", "\\n")
        for uc in self.user_chat.chat.user_chats:
            UserToMessageRelation(message_=self, user_=uc.user, read_=False).add()

        UserToMessageRelation.get.by_message(self).by_user(
            current_user
        ).first().act_mark_as_read()

        return self

    def remove(self):
        for um in self.user_messages:
            um.remove()
        db.session.delete(self)
        db.session.commit()
