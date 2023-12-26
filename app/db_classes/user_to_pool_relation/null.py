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
    def act_accept_invitation(self):
        pass
