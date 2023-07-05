from app.imports import *
from app.sqlalchemy_custom_types import *

class User(UserMixin, db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, unique=True, nullable=True)
    password = db.Column(db.String, nullable=True)
    admin = db.Column(db.Boolean, default=False)
    created_date = db.Column(db.DateTime, default=current_time)
    profile_pic = db.Column(db.String(), nullable=True)
    emails = db.relationship("Email", backref="user")

    userpools = db.relationship("User_Pool", backref="user")
    contest_judges = db.relationship("Contest_Judge", backref="user")
    contest_users = db.relationship("Contest_User", backref="user")


    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def get_verified_emails_count(self):
        return len([email for email in self.emails if email.verified])

    def get_pools(self):
        from app.dbc import User_Pool
        return User_Pool.query.filter_by(user_id=self.id).all()

    def create_new_pool(self, name):
        from app.dbc import Pool, User_Pool
        pool = Pool(name=name)
        pool.set_hashed_id()
        db.session.add(pool)
        db.session.commit()

        relation = User_Pool(user_id=self.id, pool_id=pool.id, role=Owner)
        db.session.add(relation)
        db.session.commit()

        return pool.hashed_id

    def get_pool_relation(self, pool_id):
        from app.dbc import User_Pool
        relation = User_Pool.query.filter_by(user_id=self.id, pool_id=pool_id).first()
        return relation