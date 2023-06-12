from .imports import *
from .sqlalchemy_custom_types import *
from .utils_and_functions.token_gen import generate_token

class User(UserMixin, db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, unique=True, nullable=True)
    password = db.Column(db.String, nullable=True)
    admin = db.Column(db.Boolean, default=False)
    created_date = db.Column(db.DateTime, default=datetime.datetime.now)
    profile_pic = db.Column(db.String(), nullable=True)
    emails = db.relationship("Email", backref="user")

    userpools = db.relationship("User_Pool", backref="user")

    
    def set_password(self, password):
        self.password = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password, password)
    
    def get_verified_emails_count(self):
        return len([email for email in self.emails if email.verified])
    
    def get_pools(self):
        return User_Pool.query.filter_by(user_id = self.id).all()
    
    def create_new_pool(self, name):
        pool = Pool(name=name)
        pool.set_hashed_id()
        db.session.add(pool)
        db.session.commit()

        relation = User_Pool(user_id=self.id, pool_id=pool.id, role=Owner)
        db.session.add(relation)
        db.session.commit()

        return pool.hashed_id
    
    def get_pool_relation(self, pool_id):
        relation = User_Pool.query.filter_by(user_id = self.id, pool_id = pool_id).first()
        return relation

class AdminPassword(db.Model):
    __tablename__ = 'admin_password'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    password = db.Column(db.String, nullable=True, default=generate_password_hash("qwerty"))

class Email(db.Model):
    __tablename__ = 'email'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=True)
    created_date = db.Column(db.DateTime, default=datetime.datetime.now)
    verified = db.Column(db.Boolean, default=False)
    token = db.Column(db.String, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))

class Pool(db.Model):
    __tablename__ = 'pool'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=True)
    hashed_id = db.Column(db.String, unique=True, nullable=True)
    userpools = db.relationship("User_Pool", backref="pool")
    problems = db.relationship("Problem", backref="pool")

    # open_for_new_problems = db.Column(db.Boolean, default=False) 

    def set_hashed_id(self):
        while True:
            hashed_id = generate_token(20)
            if not Pool.query.filter_by(hashed_id = hashed_id).first():
                self.hashed_id = hashed_id
                break
        
        self.hashed_id = hashed_id

    def get_users(self):
        userpools = User_Pool.query.filter_by(pool_id = self.id).all()
        userpools.sort(key = lambda up: (0, up.user.name) if up.role.isOwner() else (1, up.user.name) if up.role.isParticipant() else (2, up.user.name))
        return userpools
    
    def count_owners(self):
        return len([user for user in self.get_users() if user.role.isOwner()])
    def count_participants(self):
        return len([user for user in self.get_users() if user.role.isParticipant()])
    def count_invited(self):
        return len([user for user in self.get_users() if user.role.isInvited()])
    
    def get_problems(self):
        return Problem.query.filter_by(pool_id = self.id).all()
    
    def new_problem(self):
        problem = Problem(statement="Условие", solution="Решение", pool_id=self.id)
        db.session.add(problem)
        db.session.commit()
        problem.name = f"Задача #{problem.id}"
        db.session.commit()
        return problem
    
    def new_collection(self):
        collection = Problem_Collection(description="Описание")
        db.session.add(collection)
        db.session.commit()
        collection.name = f"Подборка #{collection.id}"
        db.session.commit()
        return collection
    
class User_Pool(db.Model):
    __tablename__ = 'user_pool'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    pool_id = db.Column(db.Integer, db.ForeignKey("pool.id"))
    role = db.Column(RoleType)

class Problem(db.Model):
    __tablename__ = 'problem'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    name = db.Column(db.String)
    statement = db.Column(db.String)
    solution = db.Column(db.String)

    pool_id = db.Column(db.Integer, db.ForeignKey("pool.id"))

    is_public = db.Column(db.Boolean, default=False)
    moderated = db.Column(db.Boolean, default=False)
    show_solution = db.Column(db.Boolean, default=False)

    problem_tags = db.relationship("Problem_Tag", backref="problem")

    attachments = db.relationship("ProblemAttachment", backref="problem")

    problem_collections = db.relationship("Problem_Collection", backref="problem")

    def get_tags(self):
        return sorted([problem_tag.tag for problem_tag in Problem_Tag.query.filter_by(problem_id = self.id).all()], key=lambda t:t.name.lower())
    def get_tag_names(self):
        return list(map(lambda t:t.name, self.get_tags()))
    
    def delete_attachment(self, attachment):
        try:
            os.remove(os.path.join(attachment.db_folder, attachment.db_filename))
        except:
            pass
        db.session.delete(attachment)
        db.session.commit()


class Tag(db.Model):
    __tablename__ = 'tag'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, unique=True, nullable=True)
    problem_tags = db.relationship("Problem_Tag", backref="tag")


class Problem_Tag(db.Model):
    __tablename__ = 'problem_tag'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tag_id = db.Column(db.Integer, db.ForeignKey("tag.id"))
    problem_id = db.Column(db.Integer, db.ForeignKey("problem.id"))

class ProblemAttachment(db.Model):
    __tablename__ = 'problem_attachment'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    db_folder = db.Column(db.String)
    db_filename = db.Column(db.String)
    preview_name = db.Column(db.String)
    locked = db.Column(db.Boolean, default=True)
    problem_id = db.Column(db.Integer, db.ForeignKey("problem.id"))


class Collection(db.Model):
    __tablename__ = 'collection'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String)
    description = db.Column(db.String)
    
    problem_collections = db.relationship("Problem_Collection", backref="collection")


class Problem_Collection(db.Model):
    __tablename__ = 'problem_collection'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    collection_id = db.Column(db.Integer, db.ForeignKey("collection.id"))
    problem_id = db.Column(db.Integer, db.ForeignKey("problem.id"))
