from app.imports import *
from app.sqlalchemy_custom_types import *


class User_Chat(db.Model):
    # --> INITIALIZE
    __tablename__ = "user_chat"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    role = db.Column(RoleType)

    # --> RELATIONS
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    chat_id = db.Column(db.Integer, db.ForeignKey("chat.id"))
    messages = db.relationship("Message", backref="user_chat")

    # --> FUNCTIONS
    def add(self):
        db.session.add(self)
        db.session.commit()

    def remove(self):
        for m in self.messages:
            m.remove()
        db.session.delete(self)
        db.session.commit()
    