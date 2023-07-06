from app.imports import *
from app.sqlalchemy_custom_types import *

class Contest_User(db.Model):
    # --> INITIALIZE
    __tablename__ = "contest_user"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    start_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)
    virtual = db.Column(db.Boolean, default=False)

    # --> RELATIONS
    contest_id = db.Column(db.Integer, db.ForeignKey("contest.id"))
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    contest_user_solutions = db.relationship("Contest_User_Solution", backref="contest_user")
    
    # --> FUNCTIONS
    def is_started(self):
        return self.start_date <= current_time()

    def is_ended(self):
        return self.end_date <= current_time()


    def add(self):
        from app.dbc import Contest_User_Solution
        db.session.add(self)
        db.session.commit()
        for cp in self.contest.contest_problems:
            cus = Contest_User_Solution(contest_user_id=self.id, contest_problem_id=cp.id)
            cus.add()


    def remove(self):
        for cus in self.contest_user_solutions:
            db.session.delete(cus)
        db.session.delete(self)
        db.session.commit()

    def act_stop(self):
        if self.is_ended():
            pass
        elif self.is_started():
            self.end_date = current_time()
            db.session.commit()
        else:
            self.remove()