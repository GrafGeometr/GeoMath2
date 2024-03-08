from app.imports import *
from app.sqlalchemy_custom_types import *


class Message(db.Model):
    # --> INITIALIZE
    __tablename__ = "message"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.String)
    date = db.Column(db.DateTime)

    # --> RELATIONS
    user_chat_id = db.Column(db.Integer, db.ForeignKey("user_chat.id"))
    user_messages = db.relationship("User_Message", backref="message")

    # --> FUNCTIONS
    def add(self):
        from app.dbc import User_Message

        db.session.add(self)
        db.session.commit()
        self.date = current_time()
        db.session.commit()
        self.content = self.content.replace("\n", "\\n")
        db.session.commit()
        for uc in self.user_chat.chat.user_chats:
            um = User_Message(message=self, user=uc.user, read=False)
            um.add()
        my_um = User_Message.query.filter_by(message=self, user=current_user).first()
        if my_um is not None:
            my_um.act_mark_as_read()
        return self

    def remove(self):
        for um in self.user_messages:
            um.remove()
        db.session.delete(self)
        db.session.commit()
