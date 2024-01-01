from app.imports import *
from app.sqlalchemy_custom_types import *

from app.db_classes.standard_model.normal import StandardModel
from app.db_classes.user_to_pool_relation.abstract import AbstractUserToPoolRelation
from app.db_classes.user_to_pool_relation.getter import UserToPoolRelationGetter
from app.db_classes.user_to_pool_relation.null import NullUserToPoolRelation


class UserToPoolRelation(StandardModel, AbstractUserToPoolRelation):
    # --> INITIALIZE
    __abstract__ = False
    __tablename__ = "user_to_pool_relation"

    role_ = db.Column(RoleType)

    null_cls_ = NullUserToPoolRelation
    getter_cls_ = UserToPoolRelationGetter

    # --> RELATIONS
    user_id_ = db.Column(db.Integer, db.ForeignKey("user.id_"))
    pool_id_ = db.Column(db.Integer, db.ForeignKey("pool.id_"))

    # --> PROPERTIES
    @property
    def role(self):
        return self.role_

    @role.setter
    def role(self, value):
        self.role_ = value
        self.save()

    @property
    def user_id(self):
        return self.user_id_

    @user_id.setter
    def user_id(self, value):
        self.user_id_ = value
        self.save()

    @property
    def user(self):
        return self.user_
    
    @user.setter
    def user(self, user):
        self.user_ = user
        self.save()

    @property
    def pool_id(self):
        return self.pool_id_

    @pool_id.setter
    def pool_id(self, value):
        self.pool_id_ = value
        self.save()

    @property
    def pool(self):
        return self.pool_
    
    @pool.setter
    def pool(self, pool):
        self.pool_ = pool
        self.save()

    # --> METHODS
    def act_accept_invitation(self):
        self.role = Participant
        return self
