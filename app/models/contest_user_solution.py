from app.imports import *
from app.sqlalchemy_custom_types import *

class Contest_User_Solution(db.Model):
    __tablename__ = "contest_user_solution"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    hashed_id = db.Column(db.String, unique=True)
    contest_user_id = db.Column(db.Integer, db.ForeignKey("contest_user.id"))
    problem_id = db.Column(db.Integer, db.ForeignKey("problem.id"))
    score = db.Column(db.Integer, nullable=True)

    content = db.Column(db.Text)

    def set_hashed_id(self):
        while True:
            hashed_id = generate_token(20)
            if not Pool.query.filter_by(hashed_id=hashed_id).first():
                self.hashed_id = hashed_id
                break

        self.hashed_id = hashed_id

    def contest_problem(self):
        return Contest_Problem.query.filter_by(contest_id=self.contest_user.contest_id, problem_id=self.problem_id).first()


    def get_attachments(self):
        return Attachment.query.filter_by(parent_type="Contest_User_Solution", parent_id=self.id).all()