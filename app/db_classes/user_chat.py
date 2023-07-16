from app.imports import *
from app.sqlalchemy_custom_types import *


class User_Chat(db.Model):
    # --> INITIALIZE
    __tablename__ = "user_chat"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

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

    def add(self):
        db.session.add(self)
        db.session.commit()

    def remove(self):
        for m in self.messages:
            m.remove()
        db.session.delete(self)
        db.session.commit()
    