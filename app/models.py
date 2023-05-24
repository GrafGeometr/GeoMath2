from .imports import *
from .utils_and_functions.token_gen import generate_token

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, unique=True, nullable=True)
    password = db.Column(db.String, nullable=True)
    created_date = db.Column(db.DateTime, default=datetime.datetime.now)
    emails = db.relationship("Email", backref="user")
    userpools = db.relationship("UserPool", backref="user")
    
    def set_password(self, password):
        self.password = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password, password)
    
    def get_verified_emails_count(self):
        return len([email for email in self.emails if email.verified])
    
    def get_pools(self):
        return UserPool.query.filter_by(user_id = self.id).all()

class Email(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=True)
    created_date = db.Column(db.DateTime, default=datetime.datetime.now)
    verified = db.Column(db.Boolean, default=False)
    token = db.Column(db.String, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))

class Pool(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, unique=True, nullable=True)
    hashed_id = db.Column(db.String, unique=True, nullable=True)
    userpools = db.relationship("UserPool", backref="pool")
    problems = db.relationship("Problem", backref="pool")

    def set_hashed_id(self):
        while True:
            hashed_id = generate_token()
            if not Pool.query.filter_by(hashed_id = hashed_id).first():
                self.hashed_id = hashed_id
                break
        
        self.hashed_id = hashed_id

    def get_users(self):
        return UserPool.query.filter_by(pool_id = self.id).all()
    
    def get_problems(self):
        return Problem.query.filter_by(pool_id = self.id).all()
    
class UserPool(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    pool_id = db.Column(db.Integer, db.ForeignKey("pool.id"))
    role = db.Column(db.String)

class Problem(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String)
    pool_id = db.Column(db.Integer, db.ForeignKey("pool.id"))
    statement = db.Column(db.String)
    solution = db.Column(db.String)