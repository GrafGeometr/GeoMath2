from app.imports import *
from app.sqlalchemy_custom_types import *

class Problem(db.Model):
    # --> INITIALIZE
    __tablename__ = "problem"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    hashed_id = db.Column(db.String, unique=True, nullable=True)
    name = db.Column(db.String)
    statement = db.Column(db.String)
    solution = db.Column(db.String)
    is_public = db.Column(db.Boolean, default=False)
    show_solution = db.Column(db.Boolean, default=False)

    # --> RELATIONS
    pool_id = db.Column(db.Integer, db.ForeignKey("pool.id"))
    contest_problems = db.relationship("Contest_Problem", backref="problem")

    # --> FUNCTIONS
    def add(self):
        db.session.add(self)
        db.session.commit()
        self.act_set_hashed_id()

    def remove(self):
        db.session.delete(self)
        db.session.commit()

    def act_set_hashed_id(self):
        while True:
            hashed_id = generate_token(20)
            if not Problem.query.filter_by(hashed_id=hashed_id).first():
                self.hashed_id = hashed_id
                break

        self.hashed_id = hashed_id
        db.session.commit()

    @staticmethod
    def get_by_hashed_id(hashed_id):
        if hashed_id is None:
            return None
        return Problem.query.filter_by(hashed_id=hashed_id).first()

    def get_tags(self):
        from app.dbc import Tag, Tag_Relation
        return sorted(
            [
                Tag.query.filter_by(id=problem_tag.tag_id).first()
                for problem_tag in Tag_Relation.query.filter_by(
                    parent_type="Problem", parent_id=self.id
                ).all()
            ],
            key=lambda t: t.name.lower(),
        )

    def get_tag_names(self):
        return list(map(lambda t: t.name, self.get_tags()))

    def get_attachments(self):
        from app.dbc import Attachment
        return Attachment.query.filter_by(
            parent_type="Problem", parent_id=self.id
        ).all()

    def is_archived(self):
        return self.is_public and self.moderated

    def get_all_contests(self):
        return [cp.contest for cp in self.contest_problems]

    def get_cu_participated(self):
        from app.dbc import Contest_User
        result = []
        for c in self.get_all_contests():
            result.extend(
                Contest_User.query.filter_by(
                    user_id=current_user.id, contest_id=c.id
                ).all()
            )
        return result

    def is_judge(self, user=current_user):
        from app.dbc import Contest_Judge
        contests = self.get_all_contests()
        judge = any(
            [
                Contest_Judge.query.filter_by(
                    user_id=user.id, contest_id=c.id
                ).first()
                for c in contests
            ]
        )
        return judge

    def is_statement_available(self, user=current_user):
        from app.dbc import Contest_User_Solution
        all_cp = [cp for cp in self.contest_problems if cp.is_valid()]
        if any([user.is_judge(cp.contest) for cp in all_cp]):
            return True
        
        all_cus = []
        for cp in all_cp:
            all_cus.extend(Contest_User_Solution.query.filter_by(contest_problem_id=cp.id).all())
        if self.is_archived() or self.is_my():
            if len(all_cus) == 0:
                return True
            return all([cus.contest_user.is_started() for cus in all_cus])
        else:
            if len(all_cus) == 0:
                return False
            return all([cus.contest_user.is_started() for cus in all_cus])

    def is_solution_available(self, user=current_user):
        from app.dbc import Contest_User_Solution
        all_cp = [cp for cp in self.contest_problems if cp.is_valid()]
        if any([user.is_judge(cp.contest) for cp in all_cp]):
            return True
        
        all_cus = []
        for cp in all_cp:
            all_cus.extend(Contest_User_Solution.query.filter_by(contest_problem_id=cp.id).all())
        if self.is_archived() or self.is_my():
            if len(all_cus) == 0:
                return True
            return all([cus.contest_user.is_ended() for cus in all_cus])
        else:
            if len(all_cus) == 0:
                return False
            return all([cus.contest_user.is_ended() for cus in all_cus])

    def is_my(self, user=current_user):
        return user.is_pool_access(self.pool_id)
    
    def is_in_contest(self, contest):
        from app.dbc import Contest_Problem
        return (Contest_Problem.query.filter_by(problem_id=self.id, contest_id=contest.id).first() is not None)

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

    @staticmethod
    def get_by_id(id):
        return Problem.query.filter_by(id=id).first()
    
    @staticmethod
    def get_by_hashed_id(hashed_id):
        return Problem.query.filter_by(hashed_id=hashed_id).first()