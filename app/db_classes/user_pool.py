from app.imports import *
from app.sqlalchemy_custom_types import *

class User_Pool(db.Model):
    # --> INITIALIZE
    __tablename__ = "user_pool"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    pool_id = db.Column(db.Integer, db.ForeignKey("pool.id"))
    role = db.Column(RoleType)

    # --> RELATIONS

    # --> FUNCTIONS
    @staticmethod
    def get_by_id(id):
        return User_Pool.query.filter_by(id=id).first()
    
    @staticmethod
    def get_by_user_and_pool(user, pool):
        if user is None or pool is None:
            return None
        return User_Pool.query.filter_by(user_id=user.id, pool_id=pool.id).first()