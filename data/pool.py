import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy import orm
from data.user_pool import UserPool
from utils_and_functions.token_gen import generate_token
from data import db_session


class Pool(SqlAlchemyBase):
    __tablename__ = 'pools'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, unique=True, nullable=True)

    hashed_id = sqlalchemy.Column(sqlalchemy.String, unique=True, nullable=True)

    users_rels = orm.relationship("UserPool", back_populates="pool")


    def set_hashed_id(self, db_sess):
        while True:
            hashed_id = generate_token()
            if not db_sess.query(Pool).filter(Pool.hashed_id == hashed_id).first():
                self.hashed_id = hashed_id
                break
        
        self.hashed_id = hashed_id

    def get_users(self):
        db_sess = db_session.create_session()
        return db_sess.query(UserPool).filter(UserPool.pool_id == self.id).all()
    

print(2)
    