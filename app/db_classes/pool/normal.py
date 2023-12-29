from typing import List

from app.imports import *
from app.sqlalchemy_custom_types import *

from app.db_classes.model_with_name.normal import ModelWithName
from app.db_classes.model_with_hashed_id.normal import ModelWithHashedId
from app.db_classes.pool.abstract import AbstractPool

from app.db_classes.pool.null import NullPool
from app.db_classes.pool.getter import PoolGetter

from app.db_classes.invite.null import NullInvite


class Pool(ModelWithHashedId, ModelWithName, AbstractPool):
    # --> INITIALIZE
    __abstract__ = False
    __tablename__ = "pool"

    null_cls_ = NullPool
    getter_cls_ = PoolGetter

    # --> RELATIONS
    user_to_pool_relations_ = db.relationship("UserToPoolRelation", backref="pool_")
    problems_ = db.relationship("Problem", backref="pool_")
    sheets_ = db.relationship("Sheet", backref="pool_")
    contests_ = db.relationship("Contest", backref="pool_")

    # --> PROPERTIES
    @property
    def user_to_pool_relations(self):
        return self.user_to_pool_relations_

    @user_to_pool_relations.setter
    def user_to_pool_relations(self, value):
        self.user_to_pool_relations_ = value
        self.save()

    @property
    def problems(self):
        return self.problems_

    @problems.setter
    def problems(self, value):
        self.problems_ = value
        self.save()

    @property
    def sheets(self):
        return self.sheets_

    @sheets.setter
    def sheets(self, value):
        self.sheets_ = value
        self.save()

    @property
    def contests(self):
        return self.contests_

    @contests.setter
    def contests(self, value):
        self.contests_ = value
        self.save()

    # --> METHODS
    def contains_user(self, user=current_user):
        return user in [up.user for up in self.user_pools]

    def is_my(self):
        return self.contains_user(current_user)

    def check_user_access(self, user=current_user) -> bool:
        from app.log import Exception_Access_Denied

        users = [up.user for up in self.user_to_pool_relations]
        access = user in users
        if not access:
            Exception_Access_Denied(self).flash()
        return access

    def check_user_owner(self, user=current_user) -> bool:
        from app.log import Exception_Access_Denied

        users = [up.user for up in self.user_pools if up.is_owner()]
        access = user in users
        if not access:
            Exception_Access_Denied(self).flash()
        return access

    def add_user(self, user=current_user, role=Participant):
        from app.db_classes.user_to_pool_relation.normal import UserToPoolRelation

        if self.contains_user(user):
            return self
        UserToPoolRelation(user_=user, pool_=self, role_=role).add()
        return self

    def remove_user(self, user=current_user):
        from app.db_classes.user_to_pool_relation.normal import UserToPoolRelation

        if not self.contains_user(user):
            return self
        UserToPoolRelation.get.by_pool(self).by_user(user).first().remove()
        return self

    def add_user_by_invite(self, user=current_user, invite=NullInvite()):
        if (
            invite.is_expired()
            or invite.get_parent() != self
            or self.contains_user(user)
        ):
            return self
        self.add_user(user)  # TODO : why don't we remove invite?
        return self

    def act_generate_new_invite_code(self):
        from app.db_classes.invite.normal import Invite

        Invite.act_refresh_all()
        invite = Invite(parent_type_=DbParent.from_type(Pool), parent_id_=self.id)
        invite.add()
        return invite

    def get_users(self):
        relations = self.user_to_pool_relations
        relations.sort(
            key=lambda up: (0, up.user.name)
            if up.role.is_owner()
            else (1, up.user.name)
            if up.role.is_participant()
            else (2, up.user.name)
        )
        return relations

    def get_owners(self):
        return [u_p_rel.user for u_p_rel in self.get_users() if u_p_rel.role.is_owner()]

    def count_owners(self):
        return len(self.get_owners())

    def get_participants(self) -> List["User"]:
        return [
            u_p_rel.user
            for u_p_rel in self.get_users()
            if u_p_rel.role.is_participant() or u_p_rel.role.is_owner()
        ]

    def count_participants(self):
        return len(self.get_participants())

    def get_problems(self):
        return self.problems

    def get_all_invites(self):
        from app.dbc import Invite

        return Invite.get_all_by_parent(self)

    def new_problem(self):
        from app.dbc import Problem

        problem = Problem(pool_id_=self.id).add()
        problem.name = f"Задача #{problem.id}"
        return problem

    def new_sheet(self):
        from app.dbc import Sheet

        sheet = Sheet(pool_id=self.id).add()
        sheet.name = f"Подборка #{sheet.id}"
        return sheet

    def new_contest(self):
        from app.dbc import Contest

        contest = Contest(
            description="", name="Название", pool_id=self.id, grade=Grade("")
        ).add()
        tm = current_time("minutes")
        contest.name = f"Контест #{contest.id}"
        contest.date = tm, tm
        return contest

    def remove(self):
        from app.dbc import UserToPoolRelation, Problem, Sheet, Contest

        for relation in UserToPoolRelation.get.by_pool(self).all():
            relation.remove()
        for problem in Problem.get.by_pool(self).all():
            problem.remove()
        for sheet in Sheet.get.by_pool(self).all():
            sheet.remove()
        for contest in Contest.get.by_pool(self).all():
            contest.remove()
        db.session.delete(self)
        db.session.commit()
