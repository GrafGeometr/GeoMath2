from app.imports import *
from app.sqlalchemy_custom_types import *


class Chat_Invite(db.Model):
    # --> INITIALIZE
    __tablename__ = "chat_invite"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    code = db.Column(db.String, unique=True, nullable=True)
    expired_at = db.Column(db.DateTime)

    # --> RELATIONS
    chat_id = db.Column(db.Integer, db.ForeignKey("chat.id"))

    # --> FUNCTIONS
    def add(self):
        db.session.add(self)
        db.session.commit()
        self.act_set_code()
        self.act_set_expired_at()
        return self
    
    def remove(self):
        db.session.delete(self)
        db.session.commit()
    
    def is_expired(self):
        return self.expired_at <= current_time()

    def act_check_expired(self):
        if self.is_expired():
            self.remove()

    def act_set_code(self):
        while True:
            code = generate_token(10)
            if not Chat_Invite.query.filter_by(code=code).first():
                self.code = code
                break
        db.session.commit()

    def act_set_expired_at(self):
        timedelta = datetime.timedelta(hours=24)
        self.expired_at = current_time() + timedelta
        db.session.commit()
        return self