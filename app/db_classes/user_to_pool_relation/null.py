from app.sqlalchemy_custom_types import *

from app.dbc import NullStandardModel, AbstractUserToPoolRelation


class NullUserToPoolRelation(NullStandardModel, AbstractUserToPoolRelation):
    # --> INITIALIZE
    __abstract__ = True

    # --> PROPERTIES
    @property
    def role(self):
        return Null_Role

    @role.setter
    def role(self, value):
        pass

    @property
    def pool_id(self):
        return -1

    @property
    def user_id(self):
        return -1

    # --> METHODS

    @staticmethod
    def get_by_user_and_pool(user, pool):
        return NullUserToPoolRelation()

    @staticmethod
    def get_all_by_pool(pool):
        return []

    @staticmethod
    def get_all_by_user(user):
        return []

    def act_accept_invitation(self):
        pass
