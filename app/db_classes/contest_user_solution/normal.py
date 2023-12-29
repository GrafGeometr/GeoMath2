from app.imports import *
from app.sqlalchemy_custom_types import *

from app.db_classes.standard_model.normal import StandardModel
from .abstract import AbstractContestUserSolution
from .null import NullContestUserSolution
from .getter import ContestUserSolutionGetter
from ..model_with_hashed_id.normal import ModelWithHashedId


class ContestUserSolution(ModelWithHashedId, AbstractContestUserSolution):
    # --> INITIALIZE
    __abstract__ = False
    __tablename__ = "contest_user_solution"

    score_ = db.Column(db.Integer, nullable=True)
    content_ = db.Column(db.String)
    judge_comment_ = db.Column(db.String)

    null_cls_ = NullContestUserSolution
    getter_cls_ = ContestUserSolutionGetter

    # --> RELATIONS
    contest_to_user_relation_id_ = db.Column(
        db.Integer, db.ForeignKey("contest_to_user_relation.id_")
    )
    contest_to_problem_relation_id_ = db.Column(
        db.Integer, db.ForeignKey("contest_to_problem_relation.id_")
    )

    # --> PROPERTIES
    @property
    def score(self):
        return self.score_

    @score.setter
    def score(self, score):
        self.score_ = score
        self.save()

    @property
    def content(self):
        return self.content_

    @content.setter
    def content(self, content):
        self.content_ = content
        self.save()

    @property
    def judge_comment(self):
        return self.judge_comment_

    @judge_comment.setter
    def judge_comment(self, judge_comment):
        self.judge_comment_ = judge_comment
        self.save()

    @property
    def contest_to_user_relation_id(self):
        return self.contest_to_user_relation_id_

    @contest_to_user_relation_id.setter
    def contest_to_user_relation_id(self, contest_to_user_relation_id):
        self.contest_to_user_relation_id_ = contest_to_user_relation_id
        self.save()

    @property
    def contest_to_user_relation(self):
        return self.contest_to_user_relation_

    @contest_to_user_relation.setter
    def contest_to_user_relation(self, contest_to_user_relation):
        self.contest_to_user_relation_ = contest_to_user_relation
        self.save()

    @property
    def contest_to_problem_relation_id(self):
        return self.contest_to_problem_relation_id_

    @contest_to_problem_relation_id.setter
    def contest_to_problem_relation_id(self, contest_to_problem_relation_id):
        self.contest_to_problem_relation_id_ = contest_to_problem_relation_id
        self.save()

    @property
    def contest_to_problem_relation(self):
        return self.contest_to_problem_relation_

    @contest_to_problem_relation.setter
    def contest_to_problem_relation(self, contest_to_problem_relation):
        self.contest_to_problem_relation_ = contest_to_problem_relation
        self.save()

    # --> METHODS
    def remove(self):
        for att in self.get_attachments():
            att.remove()
        db.session.delete(self)
        db.session.commit()

    def is_available(self, user=current_user):
        if (
            user is None
            or self.contest_user is None
            or self.contest_user.user is None
            or self.contest_user.contest is None
        ):
            return False
        return (
            (self.contest_user.user.id == user.id)
            or (self.contest_user.contest.is_rating_public())
            or (user.is_judge(self.contest_user.contest))
        )

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
            if score < 0 or score > max_score:
                score = None
        except:
            score = None
        if score is not None:
            self.score = score
        db.session.commit()
        return self

    @staticmethod
    def get_by_contest_problem_and_contest_user(contest_problem, contest_user):
        if (
            contest_problem is None
            or contest_user is None
            or contest_problem.id is None
            or contest_user.id is None
        ):
            return None
        return (
            ContestUserSolution.get.by_contest_problem(contest_problem)
            .by_contest_user(contest_user)
            .first()
        )

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
        return (
            attachment.parent_type == DbParent.from_type(type(self))
            and attachment.parent_id == self.id
        )

    def act_add_attachment(self, attachment):
        attachment.parent_type = DbParent.from_type(type(self))
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
