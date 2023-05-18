import datetime
import math
import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy import orm


class Email(SqlAlchemyBase):
    __tablename__ = 'emails'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    created_date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)

    verified = sqlalchemy.Column(sqlalchemy.Boolean, default=False)

    token = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))
    user = orm.relationship("User")
