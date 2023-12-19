from app.imports import *
from app.sqlalchemy_custom_types import *

from app.db_classes.standart_database_classes import *


class User_Chat(db.Model, StandartModel):
    # --> INITIALIZE
    __tablename__ = "user_chat"

    # --> RELATIONS
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    chat_id = db.Column(db.Integer, db.ForeignKey("chat.id"))
    messages = db.relationship("Message", backref="user_chat")

    # --> FUNCTIONS
    def is_owner(self):
        if self.chat.club is None:
            return True

        return self.user.get_club_relation(self.chat.club.id).role.isOwner()

    def is_participant(self):
        if self.chat.club is None:
            return False

        return self.user.get_club_relation(self.chat.club.id).role.isParticipant()

    def remove(self):
        for m in self.messages:
            m.remove()
        db.session.delete(self)
        db.session.commit()
