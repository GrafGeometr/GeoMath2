from app.imports import *
from app.sqlalchemy_custom_types import *

class Contest_Problem(db.Model):
    __tablename__ = "contest_problem"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    contest_id = db.Column(db.Integer, db.ForeignKey("contest.id"))
    problem_id = db.Column(db.Integer, db.ForeignKey("problem.id"))
    max_score = db.Column(db.Integer, default=7)