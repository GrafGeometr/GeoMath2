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
    
    def add(self):
        db.session.add(self)
        db.session.commit()
        return self
    
    def remove(self):
        db.session.delete(self)
        db.session.commit()
    
    def save(self):
        db.session.commit()
        return self