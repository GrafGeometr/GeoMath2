from app.imports import *
from app.sqlalchemy_custom_types import *

class Pool(db.Model):
    __tablename__ = "pool"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=True)
    hashed_id = db.Column(db.String, unique=True, nullable=True)
    userpools = db.relationship("User_Pool", backref="pool")
    problems = db.relationship("Problem", backref="pool")
    sheets = db.relationship("Sheet", backref="pool")
    contests = db.relationship("Contest", backref="pool")

    # open_for_new_problems = db.Column(db.Boolean, default=False)

    def set_hashed_id(self):
        while True:
            hashed_id = generate_token(20)
            if not Problem.query.filter_by(hashed_id=hashed_id).first():
                self.hashed_id = hashed_id
                break

        self.hashed_id = hashed_id

    def get_users(self):
        userpools = User_Pool.query.filter_by(pool_id=self.id).all()
        userpools.sort(
            key=lambda up: (0, up.user.name)
            if up.role.isOwner()
            else (1, up.user.name)
            if up.role.isParticipant()
            else (2, up.user.name)
        )
        return userpools

    def count_owners(self):
        return len([user for user in self.get_users() if user.role.isOwner()])

    def count_participants(self):
        return len([user for user in self.get_users() if user.role.isParticipant()])

    def count_invited(self):
        return len([user for user in self.get_users() if user.role.isInvited()])

    def get_problems(self):
        return Problem.query.filter_by(pool_id=self.id).all()

    def new_problem(self):
        problem = Problem(statement="", solution="", pool_id=self.id)
        problem.set_hashed_id()
        db.session.add(problem)
        db.session.commit()
        problem.name = f"Задача #{problem.id}"
        db.session.commit()
        return problem

    def new_sheet(self):
        sheet = Sheet(text="", pool_id=self.id)
        db.session.add(sheet)
        db.session.commit()
        sheet.name = f"Подборка #{sheet.id}"
        db.session.commit()
        return sheet

    def new_contest(self):
        contest = Contest(description="", name="Название", pool_id=self.id)
        db.session.add(contest)
        db.session.commit()
        tm = current_time()
        contest.name = f"Контест #{contest.id}"
        contest.start_date = tm
        contest.end_date = tm
        db.session.commit()

        return contest