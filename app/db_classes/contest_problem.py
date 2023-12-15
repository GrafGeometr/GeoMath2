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
        from app.dbc import Contest_User_Solution
        db.session.add(self)
        db.session.commit()
        for cu in self.contest.contest_users:
            Contest_User_Solution(contest_user=cu, contest_problem=self).add()
        return self

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
        return self
    
    def is_accessible(self, user=current_user):
        print(self.is_valid(), self.problem, self.problem.is_statement_available(user))
        return self.is_valid() and self.problem is not None and self.problem.is_statement_available(user)

    def is_valid(self):
        if self.problem is None or self.contest is None:
            return False
        return self.problem.is_archived() or self.problem.pool.id == self.contest.pool.id

    def get_active_contest_user_solution(self, user=current_user):
        if user is None:
            return None
        from app.dbc import Contest_User, Contest_User_Solution
        contest_user = Contest_User.get_active_by_contest_and_user(self.contest, user)
        return Contest_User_Solution.get_by_contest_problem_and_contest_user(self, contest_user)

    @staticmethod
    def get_by_id(id):
        if id is None:
            return None
        return Contest_Problem.query.filter_by(id=id).first()

    @staticmethod
    def get_by_contest_and_problem(contest, problem):
        if contest is None or problem is None or contest.id is None or problem.id is None:
            return None
        return Contest_Problem.query.filter_by(problem_id=problem.id, contest_id=contest.id).first()
    
    @staticmethod
    def get_all_by_contest(contest):
        if contest is None:
            return []
        return Contest_Problem.query.filter_by(contest_id=contest.id).all()

    def save(self):
        db.session.commit()
        return self

    