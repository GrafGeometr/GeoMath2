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
    sheets = db.relationship("Sheet", backref="pool")

    # open_for_new_problems = db.Column(db.Boolean, default=False) 

    def set_hashed_id(self):
        while True:
            hashed_id = generate_token(20)
            if not Problem.query.filter_by(hashed_id = hashed_id).first():
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
        problem.set_hashed_id()
        db.session.add(problem)
        db.session.commit()
        problem.name = f"Задача #{problem.id}"
        db.session.commit()
        return problem
    
    def new_sheet(self):
        sheet = Sheet(text="Описание", pool_id=self.id)
        db.session.add(sheet)
        db.session.commit()
        sheet.name = f"Подборка #{sheet.id}"
        db.session.commit()
        return sheet
    
class User_Pool(db.Model):
    __tablename__ = 'user_pool'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    pool_id = db.Column(db.Integer, db.ForeignKey("pool.id"))
    role = db.Column(RoleType)

class Problem(db.Model):
    __tablename__ = 'problem'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    hashed_id = db.Column(db.String, unique=True, nullable=True)

    name = db.Column(db.String)
    statement = db.Column(db.String)
    solution = db.Column(db.String)

    pool_id = db.Column(db.Integer, db.ForeignKey("pool.id"))

    is_public = db.Column(db.Boolean, default=False)
    moderated = db.Column(db.Boolean, default=False)
    show_solution = db.Column(db.Boolean, default=False)


    def set_hashed_id(self):
        while True:
            hashed_id = generate_token(20)
            if not Pool.query.filter_by(hashed_id = hashed_id).first():
                self.hashed_id = hashed_id
                break
        
        self.hashed_id = hashed_id

    def get_tags(self):
        return sorted([Tag.query.filter_by(id = problem_tag.tag_id).first() for problem_tag in Tag_Relation.query.filter_by(parent_type = "Problem", parent_id = self.id).all()], key=lambda t:t.name.lower())

    def get_tag_names(self):
        return list(map(lambda t:t.name, self.get_tags()))
    
    def get_attachments(self):
        return Attachment.query.filter_by(parent_type = "Problem", parent_id = self.id).all()

    
    def is_archived(self):
        return self.is_public and self.moderated
    
    def is_statement_available(self):
        if (self.is_public):
            return True
        relation = current_user.get_pool_relation(self.pool_id)
        if (relation.role.isOwner() or relation.role.isParticipant()):
            return True
        return False
    
    def is_solution_available(self):
        if (self.is_public):
            return True
        relation = current_user.get_pool_relation(self.pool_id)
        if (relation.role.isOwner() or relation.role.isParticipant()):
            return True
        return False
    
    def get_nonsecret_attachments(self):
        result = []
        for attachment in self.get_attachments():
            if not attachment.other_data["is_secret"]:
                if self.is_statement_available():
                    result.append(attachment)
            if attachment.other_data["is_secret"]:
                if self.is_solution_available():
                    result.append(attachment)
        return result


class Tag(db.Model):
    __tablename__ = 'tag'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, unique=True, nullable=True)


class Tag_Relation(db.Model):
    __tablename__ = 'tag_relation'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tag_id = db.Column(db.Integer)

    parent_type = db.Column(db.String) # 'Problem' | 'Sheet'
    parent_id = db.Column(db.Integer)

    other_data = db.Column(db.JSON, default={})

    def get_parent(self):
        if self.parent_type == "Problem":
            return Problem.query.filter_by(id = self.parent_id).first()
        elif self.parent_type == "Sheet":
            return Sheet.query.filter_by(id = self.parent_id).first()
        
    def remove(self):
        db.session.delete(self)
        db.session.commit()

class Attachment(db.Model):
    __tablename__ = 'attachment'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    db_folder = db.Column(db.String)
    db_filename = db.Column(db.String)

    short_name = db.Column(db.String)

    parent_type = db.Column(db.String) # 'Problem' | 'Sheet'
    parent_id = db.Column(db.Integer)

    other_data = db.Column(db.JSON, default={})

    def get_parent(self):
        if self.parent_type == "Problem":
            return Problem.query.filter_by(id = self.parent_id).first()
        elif self.parent_type == "Sheet":
            return Sheet.query.filter_by(id = self.parent_id).first()
    
    def remove(self):
        try:
            os.remove(os.path.join(self.db_folder, self.db_filename))
        except:
            pass
        db.session.delete(self)
        db.session.commit()


class Sheet(db.Model):
    __tablename__ = 'sheet'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String)
    text = db.Column(db.String)

    is_public = db.Column(db.Boolean, default=False)

    pool_id = db.Column(db.Integer, db.ForeignKey("pool.id"))

    def get_tags(self):
        return sorted([Tag.query.filter_by(id = sheet_tag.tag_id).first() for sheet_tag in Tag_Relation.query.filter_by(parent_type = "Sheet", parent_id = self.id).all()], key=lambda t:t.name.lower())
    def get_tag_names(self):
        return list(map(lambda t:t.name, self.get_tags()))
    
    def get_attachments(self):
        return Attachment.query.filter_by(parent_type = "Sheet", parent_id = self.id).all()

    def is_archived(self):
        return self.is_public
