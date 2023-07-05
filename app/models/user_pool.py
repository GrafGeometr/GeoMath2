from app.imports import *
from app.sqlalchemy_custom_types import *

class User_Pool(db.Model):
    __tablename__ = "user_pool"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    pool_id = db.Column(db.Integer, db.ForeignKey("pool.id"))
    role = db.Column(RoleType)