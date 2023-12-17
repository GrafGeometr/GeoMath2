from app.imports import *
from app.sqlalchemy_custom_types import *

from app.db_classes.standart_database_classes import *


class Contest_Judge(db.Model, StandartModel):
    # --> INITIALIZE
    __tablename__ = "contest_judge"

    # --> RELATIONS
    contest_id = db.Column(db.Integer, db.ForeignKey("contest.id"))
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    # --> FUNCTIONS
    @staticmethod
    def get_by_contest_and_user(contest, user):
        if contest is None or user is None or contest.id is None or user.id is None:
            return None
        return Contest_Judge.query.filter_by(
            contest_id=contest.id, user_id=user.id
        ).first()
