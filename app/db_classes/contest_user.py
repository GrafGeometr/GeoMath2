from app.imports import *
from app.sqlalchemy_custom_types import *

class Contest_User(db.Model):
    # --> INITIALIZE
    __tablename__ = "contest_user"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    start_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)
    virtual = db.Column(db.Boolean, default=False)

    # --> RELATIONS
    contest_id = db.Column(db.Integer, db.ForeignKey("contest.id"))
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    contest_user_solutions = db.relationship("Contest_User_Solution", backref="contest_user")
    
    # --> FUNCTIONS
    def is_started(self):
        return self.start_date <= current_time()

    def is_ended(self):
        return self.end_date <= current_time()
    
    def is_active(self):
        return not self.is_ended()

    def end_manually(self):
        if self.is_ended():
            return
        if self.is_started():
            self.end_date = current_time()
            return
        for cus in self.contest_user_solutions:
            db.session.delete(cus)
        db.session.delete(self)
        db.session.commit()
    
    @staticmethod
    def get_by_id(id):
        return Contest_User.query.filter_by(id=id).first()

    @staticmethod
    def get_active_by_contest_and_user(contest, user):
        if contest is None or user is None:
            return None
        active_list =  [x for x in Contest_User.query.filter_by(contest_id=contest.id, user_id=user.id).all() if x.is_active()]
        if len(active_list) != 1:
            return None
        return active_list[0]
    