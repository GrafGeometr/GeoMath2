from app.imports import *
from app.sqlalchemy_custom_types import *

class Contest_Judge(db.Model):
    # --> INITIALIZE
    __tablename__ = "contest_judge"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    # --> RELATIONS
    contest_id = db.Column(db.Integer, db.ForeignKey("contest.id"))
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    # --> FUNCTIONS