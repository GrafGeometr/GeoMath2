from app.imports import *
from app.sqlalchemy_custom_types import *

class Contest_User_Solution(db.Model):
    # --> INITIALIZE
    __tablename__ = "contest_user_solution"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    hashed_id = db.Column(db.String, unique=True, nullable=True)
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
        return self

    def remove(self):
        for att in self.get_attachments():
            att.remove()
        db.session.delete(self)
        db.session.commit()

    def is_available(self, user=current_user):
        if user is None or self.contest_user is None or self.contest_user.user is None or self.contest_user.contest is None:
            return False
        return (self.contest_user.user.id == user.id) or (user.is_judge(self.contest_user.contest))
    
    def act_set_hashed_id(self):
        while True:
            hashed_id = generate_token(20)
            if not Contest_User_Solution.query.filter_by(hashed_id=hashed_id).first():
                self.hashed_id = hashed_id
                break

        self.hashed_id = hashed_id
        return self.save()

    def act_set_content(self, content):
        if content is None:
            return
        if content != "":
            self.content = content
            db.session.commit()
        return self

    def act_set_judge_comment(self, judge_comment):
        if not (current_user.is_judge(self.contest_problem.contest)):
            return
        if judge_comment is None:
            return
        if judge_comment != "":
            self.judge_comment = judge_comment
            db.session.commit()
        return self
    
    def act_set_score(self, score):
        if not (current_user.is_judge(self.contest_problem.contest)):
            return
        max_score = self.contest_problem.max_score
        try:
            score = int(score)
            if (score < 0 or score > max_score):
                score = None
        except:
            score = None
        if score is not None:
            self.score = score
        db.session.commit()
        return self

    @staticmethod
    def get_by_id(id):
        if id is None:
            return None
        return Contest_User_Solution.query.filter_by(id=id).first()
    
    @staticmethod
    def get_by_hashed_id(hashed_id):
        if hashed_id is None:
            return None
        return Contest_User_Solution.query.filter_by(hashed_id=hashed_id).first()

    
    @staticmethod
    def get_by_contest_problem_and_contest_user(contest_problem, contest_user):
        if contest_problem is None or contest_user is None or contest_problem.id is None or contest_user.id is None:
            return None
        return Contest_User_Solution.query.filter_by(contest_problem_id=contest_problem.id, contest_user_id=contest_user.id).first()
    
    def save(self):
        db.session.commit()
        return self
    
    # ATTACHMENTS BLOCK

    def get_attachments(self):
        from app.dbc import Attachment
        return Attachment.get_all_by_parent(self)

    def get_nonsecret_attachments(self):
        result = []
        for attachment in self.get_attachments():
            if not attachment.is_secret():
                if self.is_statement_available():
                    result.append(attachment)
            if attachment.is_secret():
                if self.is_solution_available():
                    result.append(attachment)
        return result
    
    def is_attachment(self, attachment):
        if attachment is None:
            return False
        return attachment.parent_type == DbParent.fromType(type(self)) and attachment.parent_id == self.id
    
    def act_add_attachment(self, attachment):
        attachment.parent_type = DbParent.fromType(type(self))
        attachment.parent_id = self.id
        return self.save()
    
    def act_add_attachment_by_db_filename(self, db_filename):
        if db_filename is None:
            return self
        from app.dbc import Attachment
        return self.act_add_attachment(Attachment.get_by_db_filename(db_filename))
    
    def act_remove_attachment(self, attachment):
        attachment.parent_type = None
        attachment.parent_id = None
        return self.save()
    
    def act_remove_attachment_by_db_filename(self, db_filename):
        if db_filename is None:
            return self
        from app.dbc import Attachment
        return self.act_remove_attachment(Attachment.get_by_db_filename(db_filename))
    
    def act_set_attachments(self, names):
        for attachment in self.get_attachments():
            self.act_remove_attachment(attachment)
        for name in names:
            self.act_add_attachment_by_db_filename(name)
        return self