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
    def set_hashed_id(self):
        from app.dbc import Pool
        while True:
            hashed_id = generate_token(20)
            if not Pool.query.filter_by(hashed_id=hashed_id).first():
                self.hashed_id = hashed_id
                break

        self.hashed_id = hashed_id

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

    def is_judge(self):
        from app.dbc import Contest_Judge
        contests = self.get_all_contests()
        judge = any(
            [
                Contest_Judge.query.filter_by(
                    user_id=current_user.id, contest_id=c.id
                ).first()
                for c in contests
            ]
        )
        return judge

    def is_statement_available(self):
        if self.is_judge():
            return True
        contest_users = self.get_cu_participated()
        if self.is_public or self.is_my():
            if len(contest_users) == 0:
                return True
            return all([cu.is_started() for cu in contest_users])
        else:
            if len(contest_users) == 0:
                return False
            return all([cu.is_started() for cu in contest_users])

    def is_solution_available(self):
        if self.is_judge():
            return True
        contest_users = self.get_cu_participated()
        if self.is_public or self.is_my():
            if len(contest_users) == 0:
                return True
            return all([cu.is_ended() for cu in contest_users])
        else:
            if len(contest_users) == 0:
                return False
            return all([cu.is_ended() for cu in contest_users])

    def is_my(self):
        relation = current_user.get_pool_relation(self.pool_id)
        if relation is None:
            return False
        if relation.role.isOwner() or relation.role.isParticipant():
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