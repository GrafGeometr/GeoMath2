from app.imports import *
from app.sqlalchemy_custom_types import *

class Contest_User(db.Model):
    __tablename__ = "contest_user"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    contest_id = db.Column(db.Integer, db.ForeignKey("contest.id"))
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    contest_user_solutions = db.relationship(
        "Contest_User_Solution", backref="contest_user"
    )
    start_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)
    virtual = db.Column(db.Boolean, default=False)

    def is_started(self):
        return self.start_date <= current_time()

    def is_ended(self):
        return self.end_date <= current_time()

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