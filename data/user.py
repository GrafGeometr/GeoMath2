import datetime
from data.user_pool import UserPool
import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy import orm
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from data import db_session


class User(SqlAlchemyBase, UserMixin):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, unique=True, nullable=True)

    hashed_password = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    created_date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)

    emails = orm.relationship("Email", back_populates="user")

    pools_rels = orm.relationship("UserPool", back_populates="user")
    
    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)
    
    def get_verified_emails_count(self):
        return len([email for email in self.emails if email.verified])

    def get_pools(self):
        db_sess = db_session.create_session()
        return db_sess.query(UserPool).filter(UserPool.user_id == self.id).all()