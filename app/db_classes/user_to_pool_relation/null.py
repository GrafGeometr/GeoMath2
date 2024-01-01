from app.sqlalchemy_custom_types import *

from app.db_classes.standard_model.null import NullStandardModel
from app.db_classes.user_to_pool_relation.abstract import AbstractUserToPoolRelation


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
    def user_id(self):
        return -1
    
    @user_id.setter
    def user_id(self, user_id):
        pass

    @property
    def user(self):
        from app.dbc import NullUser
        return NullUser()
    
    @user.setter
    def user(self, user):
        pass
    
    @property
    def pool_id(self):
        return -1
    
    @pool_id.setter
    def pool_id(self, pool_id):
        pass

    @property
    def pool(self):
        from app.dbc import NullPool
        return NullPool()
    
    @pool.setter
    def pool(self, pool):
        pass

    # --> METHODS
    def act_accept_invitation(self):
        pass
