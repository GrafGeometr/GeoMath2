from app.imports import *
from app.sqlalchemy_custom_types import *

from app.db_classes.standart_database_classes import *


class Pool(db.Model, ModelWithHashedId, ModelWithName):
    # --> INITIALIZE
    __tablename__ = "pool"

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
    
    def check_user_access(self, current_user) -> bool:
        from app.log import Exception_Access_Denied
        users = [up.user for up in self.user_pools]
        access = current_user in users
        if (not access):
            Exception_Access_Denied(self).flash()
        return access
    
    def get_name(self) -> str:
        return self.name
    
    @staticmethod
    def get_by_hashed_id(hashed_id: string) -> "Pool":
        from app.dbc import Pool_Null
        pool = Pool.query.filter_by(hashed_id=hashed_id).first()
        if pool is None:
            pool = Pool_Null()
        return pool

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

    def get_owners(self):
        return [up.user for up in self.get_users() if up.role.isOwner()]

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
        return sheet.act_set_name(f"Подборка #{sheet.id}").save()

    def new_contest(self):
        from app.dbc import Contest

        contest = Contest(description="", name="Название", pool_id=self.id, grade=Grade("")).add()
        tm = current_time("minutes")
        return contest.act_set_name(f"Контест #{contest.id}").act_set_date(tm, tm)

    def remove(self):
        from app.dbc import User_Pool, Problem, Sheet, Contest

        for relation in User_Pool.query.filter_by(pool_id=self.id).all():
            relation.remove()
        for problem in Problem.query.filter_by(pool_id=self.id).all():
            problem.remove()
        for sheet in Sheet.query.filter_by(pool_id=self.id).all():
            sheet.remove()
        for contest in Contest.query.filter_by(pool_id=self.id).all():
            contest.remove()
        db.session.delete(self)
        db.session.commit()
