from app.imports import *
from app.sqlalchemy_custom_types import *

class Contest_Problem(db.Model):
    # --> INITIALIZE
    __tablename__ = "contest_problem"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    max_score = db.Column(db.Integer, default=7)

    # --> RELATIONS
    contest_id = db.Column(db.Integer, db.ForeignKey("contest.id"))
    problem_id = db.Column(db.Integer, db.ForeignKey("problem.id"))
    contest_user_solutions = db.relationship("Contest_User_Solution", backref="contest_problem")

    # --> FUNCTIONS
    