from app.imports import *
from app.sqlalchemy_custom_types import *


class User_Message(db.Model):
    # --> INITIALIZE
    __tablename__ = "user_message"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    read = db.Column(db.Boolean)

    # --> RELATIONS
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    message_id = db.Column(db.Integer, db.ForeignKey("message.id"))

    # --> FUNCTIONS
    def add(self):
        db.session.add(self)
        db.session.commit()
        return self
    
    def remove(self):
        db.session.delete(self)
        db.session.commit()

    def is_read(self):
        return self.read
    
    def act_mark_as_read(self):
        self.read = True
        db.session.commit()

    def act_mark_as_unread(self):
        self.read = False
        db.session.commit()