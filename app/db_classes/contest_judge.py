from app.imports import *
from app.sqlalchemy_custom_types import *

class Contest_Judge(db.Model):
    # --> INITIALIZE
    __tablename__ = "contest_judge"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    # --> RELATIONS
    contest_id = db.Column(db.Integer, db.ForeignKey("contest.id"))
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    # --> FUNCTIONS
    @staticmethod
    def get_by_id(id):
        if id is None:
            return None
        return Contest_Judge.query.filter_by(id=id).first()
    
    @staticmethod
    def get_by_contest_and_user(contest, user):
        if contest is None or user is None or contest.id is None or user.id is None:
            return None
        return Contest_Judge.query.filter_by(contest_id=contest.id, user_id=user.id).first()

    def add(self):
        db.session.add(self)
        db.session.commit()
        return self
    
    
    def remove(self):
        db.session.delete(self)
        db.session.commit()
    

    def save(self):
        db.session.commit()
        return self