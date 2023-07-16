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
    def is_contains_user(self, user=current_user):
        return user in [up.user for up in self.user_pools]

    def is_my(self):
        return self.is_contains_user(current_user)
    
    def act_set_hashed_id(self):
        while True:
            hashed_id = generate_token(20)
            if not Pool.get_by_hashed_id(hashed_id):
                self.hashed_id = hashed_id
                break

        self.hashed_id = hashed_id
        return self.save()
    
    def act_add_user(self, user=current_user, role=Participant):
        from app.dbc import User_Pool
        if user is None:
            return
        if self.is_contains_user(user):
            return
        up = User_Pool(user=user, pool=self, role=role)
        up.add()
        return self
    
    def act_remove_user(self, user=current_user):
        from app.dbc import User_Pool
        if user is None:
            return
        if not self.is_contains_user(user):
            return
        up = User_Pool.query.filter_by(user=user, pool=self).first()
        up.remove()
        return self
    
    def act_add_user_by_invite(self, user=current_user, invite=None):
        if (invite is None) or (invite.is_expired()) or (invite.get_parent() != self):
            return
        if self.is_contains_user(user):
            return
        self.act_add_user(user)
        return self
    
    def act_generate_new_invite_code(self):
        from app.dbc import Invite
        Invite.act_refresh_all()
        invite = Invite(parent_type=DbParent.fromType(Pool), parent_id=self.id)
        invite.add()
        return invite

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

    def get_problems(self):
        from app.dbc import Problem

        return Problem.get_all_by_pool(self)
    
    def get_all_invites(self):
        from app.dbc import Invite
        return Invite.get_all_by_parent(self)
                

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