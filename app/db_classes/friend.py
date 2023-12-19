from app.imports import *
from app.sqlalchemy_custom_types import *

from app.db_classes.standart_database_classes import *


class Friend(db.Model, StandartModel):
    # --> INITIALIZE
    __tablename__ = "friend"

    friend_from = db.Column(db.Integer)
    friend_to = db.Column(db.Integer)
    accepted = db.Column(db.Boolean, default=False)
    # --> RELATIONS

    # --> FUNCTIONS
    def act_accept(self):
        self.accepted = True
        db.session.commit()
