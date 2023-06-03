from .imports import *
from .sqlalchemy_custom_types import *
from .utils_and_functions.token_gen import generate_token

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, unique=True, nullable=True)
    password = db.Column(db.String, nullable=True)
    admin = db.Column(db.Boolean, default=False)
    created_date = db.Column(db.DateTime, default=datetime.datetime.now)
    emails = db.relationship("Email", backref="user")

    userpools = db.relationship("UserPool", backref="user")
    archs = db.relationship("Arch", backref="user")
    
    def set_password(self, password):
        self.password = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password, password)
    
    def get_verified_emails_count(self):
        return len([email for email in self.emails if email.verified])
    
    def get_pools(self):
        return UserPool.query.filter_by(user_id = self.id).all()
    
    def create_new_pool(self, name):
        pool = Pool(name=name)
        pool.set_hashed_id()
        db.session.add(pool)
        db.session.commit()

        relation = UserPool(user_id=self.id, pool_id=pool.id, role=Owner)
        db.session.add(relation)
        db.session.commit()

        return pool.hashed_id
    
    def get_pool_relation(self, pool_id):
        relation = UserPool.query.filter_by(user_id = self.id, pool_id = pool_id).first()
        return relation


class AdminPassword(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    password = db.Column(db.String, nullable=True, default=generate_password_hash("qwerty"))

class Email(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=True)
    created_date = db.Column(db.DateTime, default=datetime.datetime.now)
    verified = db.Column(db.Boolean, default=False)
    token = db.Column(db.String, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))

class Pool(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=True)
    hashed_id = db.Column(db.String, unique=True, nullable=True)
    userpools = db.relationship("UserPool", backref="pool")
    problems = db.relationship("Problem", backref="pool")

    def set_hashed_id(self):
        while True:
            hashed_id = generate_token(20)
            if not Pool.query.filter_by(hashed_id = hashed_id).first():
                self.hashed_id = hashed_id
                break
        
        self.hashed_id = hashed_id

    def get_users(self):
        userpools = UserPool.query.filter_by(pool_id = self.id).all()
        userpools.sort(key = lambda up: (0, up.user.name) if up.role.isOwner() else (1, up.user.name) if up.role.isParticipant() else (2, up.user.name))
        return userpools
    
    def get_problems(self):
        return Problem.query.filter_by(pool_id = self.id).all()
    
    def new_problem(self):
        problem = Problem(statement="Условие", solution="Решение", pool_id=self.id)
        db.session.add(problem)
        db.session.commit()
        problem.name = f"Задача #{problem.id}"
        db.session.commit()
        return problem

    
class UserPool(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    pool_id = db.Column(db.Integer, db.ForeignKey("pool.id"))
    role = db.Column(RoleType)

class Problem(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String)
    pool_id = db.Column(db.Integer, db.ForeignKey("pool.id"))
    statement = db.Column(db.String)
    solution = db.Column(db.String)

class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, unique=True, nullable=True)
    archtags = db.relationship("ArchTag", backref="tag")

class ArchTag(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tag_id = db.Column(db.Integer, db.ForeignKey("tag.id"))
    arch_id = db.Column(db.Integer, db.ForeignKey("arch.id"))

class Arch(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String)
    statement = db.Column(db.String)
    solution = db.Column(db.String)
    moderated = db.Column(db.Boolean, default=False)
    show_solution = db.Column(db.Boolean, default=False)
    archtags = db.relationship("ArchTag", backref="arch")
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    def get_tags(self):
        return sorted([archtag.tag for archtag in ArchTag.query.filter_by(arch_id = self.id).all()], key=lambda t:t.name.lower())