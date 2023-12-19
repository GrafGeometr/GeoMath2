from app.imports import *
from app.sqlalchemy_custom_types import *

from app.db_classes.standart_database_classes import *

class User_Club(db.Model, StandartModel):
    # --> INITIALIZE
    __tablename__ = "user_club"

    role = db.Column(RoleType)

    # --> RELATIONS
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    club_id = db.Column(db.Integer, db.ForeignKey("club.id"))

    # --> FUNCTIONS
    