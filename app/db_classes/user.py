from app.imports import *
from app.sqlalchemy_custom_types import *

class User(UserMixin, db.Model):
    # --> INITIALIZE
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, unique=True, nullable=True)
    password = db.Column(db.String, nullable=True)
    admin = db.Column(db.Boolean, default=False)
    created_date = db.Column(db.DateTime, default=current_time)
    profile_pic = db.Column(db.String(), nullable=True)

    # --> RELATIONS
    emails = db.relationship("Email", backref="user")
    user_pools = db.relationship("User_Pool", backref="user")
    contest_judges = db.relationship("Contest_Judge", backref="user")
    contest_users = db.relationship("Contest_User", backref="user")
    likes = db.relationship("Like", backref="user")
    user_chats = db.relationship("User_Chat", backref="user")
    user_messages = db.relationship("User_Message", backref="user")

    # --> FUNCTIONS
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
        pool = Pool(name=name).add()

        relation = User_Pool(user_id=self.id, pool_id=pool.id, role=Owner, invited_date=current_time(), joined_date=current_time()).add()

        return pool.hashed_id

    def get_pool_relation(self, pool_id):
        from app.dbc import User_Pool
        relation = User_Pool.query.filter_by(user_id=self.id, pool_id=pool_id).first()
        return relation
    
    def get_chat_relation(self, chat_id):
        from app.dbc import User_Chat
        relation = User_Chat.query.filter_by(user_id=self.id, chat_id=chat_id).first()
        return relation
    
    def is_pool_access(self, pool_id):
        from app.dbc import User_Pool
        relation = User_Pool.query.filter_by(user_id=self.id, pool_id=pool_id).first()
        return (relation is not None) and (not relation.role.isInvited())
    
    def is_judge(self, contest):
        from app.dbc import Contest_Judge
        return (Contest_Judge.query.filter_by(user_id=self.id, contest_id=contest.id).first() is not None)
    
    @staticmethod
    def get_by_id(id):
        return User.query.filter_by(id=id).first()
    
    @staticmethod
    def get_by_name(name):
        return User.query.filter_by(name=name).first()

    def save(self):
        db.session.commit()
        return self
        