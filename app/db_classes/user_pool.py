from app.imports import *
from app.sqlalchemy_custom_types import *

from app.db_classes.standart_database_classes import *

class User_Pool(db.Model, StandartModel):
    # --> INITIALIZE
    __tablename__ = "user_pool"

    role = db.Column(RoleType)

    # --> RELATIONS
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    pool_id = db.Column(db.Integer, db.ForeignKey("pool.id"))

    # --> FUNCTIONS
    def is_owner(self) -> bool:
        return self.role == Owner

    @staticmethod
    def get_by_user_and_pool(user, pool):
        if user is None or pool is None:
            return None
        return User_Pool.query.filter_by(user_id=user.id, pool_id=pool.id).first()
    
    @staticmethod
    def get_all_by_pool(pool):
        if pool is None:
            return []
        return User_Pool.query.filter_by(pool_id=pool.id).all()
    
    @staticmethod
    def get_all_by_user(user):
        if user is None:
            return []
        return User_Pool.query.filter_by(user_id=user.id).all()
    
    def act_accept_invitation(self):
        self.role = Participant
        db.session.commit()
        return self

