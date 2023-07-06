from app.imports import *
from app.sqlalchemy_custom_types import *

class Contest_User_Solution(db.Model):
    # --> INITIALIZE
    __tablename__ = "contest_user_solution"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    hashed_id = db.Column(db.String, unique=True)
    score = db.Column(db.Integer, nullable=True)
    content = db.Column(db.String)
    judge_comment = db.Column(db.String)

    # --> RELATIONS
    contest_user_id = db.Column(db.Integer, db.ForeignKey("contest_user.id"))
    contest_problem_id = db.Column(db.Integer, db.ForeignKey("contest_problem.id"))
    
    # --> FUNCTIONS
    def add(self):
        db.session.add(self)
        db.session.commit()
        self.act_set_hashed_id()

    def remove(self):
        db.session.delete(self)
        db.session.commit()

    def is_available(self, user=current_user):
        return (self.contest_user.user.id == user.id) or (user.is_judge(self.contest_user.contest))

    def act_set_hashed_id(self):
        while True:
            hashed_id = generate_token(20)
            if not Contest_User_Solution.query.filter_by(hashed_id=hashed_id).first():
                self.hashed_id = hashed_id
                break

        self.hashed_id = hashed_id
        db.session.commit()

    def act_update_content(self, content):
        if content != "":
            self.content = content
            db.session.commit()
    
    def act_update_judge_comment(self, judge_comment):
        if judge_comment != "":
            self.judge_comment = judge_comment
            db.session.commit()

    @staticmethod
    def get_by_id(id):
        return Contest_User_Solution.query.filter_by(id=id).first()
    
    @staticmethod
    def get_by_hashed_id(hashed_id):
        return Contest_User_Solution.query.filter_by(hashed_id=hashed_id).first()

    def get_attachments(self):
        from app.dbc import Attachment
        return Attachment.query.filter_by(parent_type="Contest_User_Solution", parent_id=self.id).all()
    
    @staticmethod
    def get_by_contest_problem_and_contest_user(contest_problem, contest_user):
        if contest_problem is None or contest_user is None:
            return None
        return Contest_User_Solution.query.filter_by(contest_problem_id=contest_problem.id, contest_user_id=contest_user.id).first()
    