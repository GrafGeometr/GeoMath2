from app.imports import *
from app.sqlalchemy_custom_types import *

from app.dbc import StandardModel, AbstractUserToPoolRelation


class UserToPoolRelation(StandardModel, AbstractUserToPoolRelation):
    # --> INITIALIZE
    __abstract__ = False
    __tablename__ = "user_pool"

    role_ = db.Column(RoleType)

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
    def pool_id(self):
        return self.pool_id_

    @pool_id.setter
    def pool_id(self, value):
        self.pool_id_ = value
        self.save()

    # --> METHODS
    @staticmethod
    def get_by_user_and_pool(user, pool):
        return UserToPoolRelation.query.filter_by(user_id_=user.id, pool_id_=pool.id).first()

    @staticmethod
    def get_all_by_pool(pool):
        return UserToPoolRelation.query.filter_by(pool_id_=pool.id).all()

    @staticmethod
    def get_all_by_user(user):
        return UserToPoolRelation.query.filter_by(user_id_=user.id).all()

    def act_accept_invitation(self):
        self.role = Participant
        return self
