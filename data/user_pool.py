import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy import Column, ForeignKey, Table, orm



class UserPool(SqlAlchemyBase):
    __tablename__ = 'user_pool'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)

    user_id = sqlalchemy.Column(sqlalchemy.Integer, ForeignKey("users.id"))
    user = orm.relationship("User", back_populates="pools_rels")

    pool_id = sqlalchemy.Column(sqlalchemy.Integer, ForeignKey("pools.id"))
    pool = orm.relationship("Pool", back_populates="users_rels")

    role = sqlalchemy.Column(sqlalchemy.String)

