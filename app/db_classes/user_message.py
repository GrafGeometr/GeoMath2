from app.imports import *
from app.sqlalchemy_custom_types import *

from app.db_classes.standart_database_classes import StandartModel


class User_Message(db.Model, StandartModel):
    # --> INITIALIZE
    __tablename__ = "user_message"

    read = db.Column(db.Boolean)

    # --> RELATIONS
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    message_id = db.Column(db.Integer, db.ForeignKey("message.id"))

    # --> FUNCTIONS
    def is_read(self):
        return self.read

    def act_mark_as_read(self):
        self.read = True
        db.session.commit()

    def act_mark_as_unread(self):
        self.read = False
        db.session.commit()
