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
    def add(self):
        db.session.add(self)
        db.session.commit()

    def remove(self):
        for cus in self.contest_user_solutions:
            db.session.delete(cus)
        db.session.delete(self)
        db.session.commit()

    def act_set_max_score(self, score):
        try:
            score = int(score)
            if (score <= 0):
                score = None
        except:
            score = None
        if score is None:
            if self.max_score is None:
                self.max_score = 7
        else:
            self.max_score = score
        db.session.commit()

    