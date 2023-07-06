from app.imports import *
from app.sqlalchemy_custom_types import *


class Pool(db.Model):
    # --> INITIALIZE
    __tablename__ = "pool"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=True)
    hashed_id = db.Column(db.String, unique=True, nullable=True)

    # --> RELATIONS
    user_pools = db.relationship("User_Pool", backref="pool")
    problems = db.relationship("Problem", backref="pool")
    sheets = db.relationship("Sheet", backref="pool")
    contests = db.relationship("Contest", backref="pool")

    # --> FUNCTIONS
    def act_set_hashed_id(self):
        while True:
            hashed_id = generate_token(20)
            if not Pool.get_by_hashed_id(hashed_id):
                self.hashed_id = hashed_id
                break

        self.hashed_id = hashed_id
        return self.save()

    def get_users(self):
        from app.dbc import User_Pool

        userpools = User_Pool.get_all_by_pool(self)
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
        from app.dbc import Problem

        return Problem.get_all_by_pool(self)

    def new_problem(self):
        from app.dbc import Problem

        problem = Problem(statement="", solution="", pool_id=self.id).add()
        return problem.act_set_name(f"Задача #{problem.id}")
        

    def new_sheet(self):
        from app.dbc import Sheet

        sheet = Sheet(text="", pool_id=self.id).add()
        return sheet.act_set_name( f"Подборка #{sheet.id}").save()

    def new_contest(self):
        from app.dbc import Contest

        contest = Contest(description="", name="Название", pool_id=self.id).add()
        tm = current_time("minutes")
        return contest.act_set_name(f"Контест #{contest.id}").act_set_date(tm, tm)
        

    @staticmethod
    def get_by_id(id):
        if id is None:
            return None
        return Pool.query.filter_by(id=id).first()

    @staticmethod
    def get_by_hashed_id(hashed_id):
        if hashed_id is None:
            return None
        return Pool.query.filter_by(hashed_id=hashed_id).first()

    def add(self):
        db.session.add(self.act_set_hashed_id())
        return self.save()

    def save(self):
        db.session.commit()
        return self