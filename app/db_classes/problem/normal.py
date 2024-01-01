from app.imports import *
from app.sqlalchemy_custom_types import *

from app.db_classes.model_with_hashed_id.normal import ModelWithHashedId
from app.db_classes.model_with_name.normal import ModelWithName
from app.db_classes.problem.abstract import AbstractProblem
from app.db_classes.problem.null import NullProblem
from app.db_classes.problem.getter import ProblemGetter


class Problem(ModelWithHashedId, ModelWithName, AbstractProblem):
    # --> INITIALIZE
    __abstract__ = False
    __tablename__ = "problem"

    statement_ = db.Column(db.String)
    solution_ = db.Column(db.String)
    is_public_ = db.Column(db.Boolean, default=False)
    total_likes_ = db.Column(db.Integer, default=0)
    total_dislikes_ = db.Column(db.Integer, default=0)

    null_cls_ = NullProblem
    getter_cls_ = ProblemGetter

    # --> RELATIONS
    pool_id_ = db.Column(db.Integer, db.ForeignKey("pool.id_"))
    contest_problems_ = db.relationship("ContestToProblemRelation", backref="problem_")

    # --> PROPERTIES
    @property
    def statement(self):
        return self.statement_

    @statement.setter
    def statement(self, statement):
        self.statement_ = statement
        self.save()

    @property
    def solution(self):
        return self.solution_

    @solution.setter
    def solution(self, solution):
        self.solution_ = solution
        self.save()

    @property
    def is_public(self):
        return self.is_public_

    @is_public.setter
    def is_public(self, is_public):
        self.is_public_ = is_public
        self.save()

    @property
    def total_likes(self):
        return self.total_likes_

    @total_likes.setter
    def total_likes(self, total_likes):
        self.total_likes_ = total_likes
        self.save()

    @property
    def total_dislikes(self):
        return self.total_dislikes_

    @total_dislikes.setter
    def total_dislikes(self, total_dislikes):
        self.total_dislikes_ = total_dislikes
        self.save()

    @property
    def pool_id(self):
        return self.pool_id_

    @pool_id.setter
    def pool_id(self, pool_id):
        self.pool_id_ = pool_id
        self.save()

    @property
    def pool(self):
        from app.db_classes.pool.null import NullPool

        if self.pool_ is None:
            return NullPool()
        return self.pool_

    @pool.setter
    def pool(self, pool):
        self.pool_ = pool
        self.save()

    # --> METHODS
    def remove(self):
        for cp in self.contest_problems:
            cp.remove()
        for att in self.get_attachments():
            att.remove()
        from app.dbc import Like

        for l in Like.get_all_by_parent(self):
            l.remove(par=self)
        db.session.delete(self)
        db.session.commit()

    def is_liked(self):
        from app.dbc import Like

        return Like.get.by_parent(self).by_user(current_user).first() is not None

    def act_add_like(self):
        if self.is_liked():
            return self
        from app.dbc import Like

        Like(parent_type_="Problem", parent_id_=self.id, user_id_=current_user.id).add()
        return self

    def act_remove_like(self):
        from app.dbc import Like

        Like.get.by_parent(self).by_user(current_user).remove()
        return self

    def is_archived(self):
        return self.is_public

    def get_all_contests(self):
        return [cp.contest for cp in self.contest_problems]

    def get_all_likes(self):
        from app.dbc import Like

        return Like.get_all_by_parent(self)

    def get_all_good_likes(self):
        return [like for like in self.get_all_likes() if like.good]

    def get_all_bad_likes(self):
        return [like for like in self.get_all_likes() if not like.good]

    def is_statement_available(self, user=current_user):
        from app.db_classes.contest_to_user_solution_relation.normal import (
            ContestUserSolution,
        )

        all_cp = [cp for cp in self.contest_problems if cp.is_valid()]
        if any([user.is_judge(cp.contest) for cp in all_cp]):
            return True

        all_cus = []
        for cp in all_cp:
            all_cus.extend(
                ContestUserSolution.get.by_contest_problem(cp).all()
            )
        if self.is_archived() or self.is_my():
            if len(all_cus) == 0:
                return True
            return all([cus.contest_user.is_started() for cus in all_cus])
        else:
            if len(all_cus) == 0:
                return False
            return all([cus.contest_user.is_started() for cus in all_cus])

    def is_solution_available(self, user=current_user):
        from app.db_classes.contest_to_user_solution_relation.normal import (
            ContestUserSolution,
        )

        all_cp = [cp for cp in self.contest_problems if cp.is_valid()]
        if any([user.is_judge(cp.contest) for cp in all_cp]):
            return True

        all_cus = []
        for cp in all_cp:
            all_cus.extend(
                ContestUserSolution.get.by_contest_problem(cp).all()
            )
        if self.is_archived() or self.is_my():
            if len(all_cus) == 0:
                return True
            return all([cus.contest_user.is_ended() for cus in all_cus])
        else:
            if len(all_cus) == 0:
                return False
            return all([cus.contest_user.is_ended() for cus in all_cus])

    def is_tags_available(self, user=current_user):
        return self.is_solution_available()

    def is_my(self, user=current_user):
        return user.is_pool_access(self.pool_id)

    def is_in_contest(self, contest):
        from app.db_classes.contest_to_problem_relation.normal import (
            ContestToProblemRelation,
        )

        return (
            not ContestToProblemRelation.get.by_contest(contest)
            .by_problem(self)
            .first()
            .is_null()
        )

    # TAGS BLOCK

    def get_nonsorted_tags(self):
        from app.dbc import Tag

        return Tag.get_all_by_obj(self)

    def get_tags(self):
        return sorted(self.get_nonsorted_tags(), key=lambda t: t.name.lower())

    def get_tag_names(self):
        return [tag.name for tag in self.get_tags()]

    def has_tag(self, tag):
        from app.dbc import TagRelation

        return TagRelation.get.by_parent(self).by_tag(tag).is_null()

    def act_add_tags(self, tags):
        for tag in tags:
            self.act_add_tag(tag)
        return self

    def act_add_tag(self, tag):
        from app.dbc import TagRelation

        if not self.is_my() or self.is_have_tag(tag):
            return self
        TagRelation(
            parent_type_=DbParent.from_type(type(self)),
            parent_id_=self.id,
            tag_id_=tag.id,
        ).add()
        return self

    def act_add_tag_by_name(self, tag_name):
        from app.dbc import Tag

        tag = Tag.get.by_name(tag_name).first()
        if tag.is_null() and current_user.admin:
            tag = Tag(name=tag_name).add()

        return self.act_add_tag(tag)

    def act_remove_tag(self, tag):
        from app.dbc import TagRelation

        if not self.is_my():
            return self
        rel = TagRelation.get.by_parent(self).by_tag(tag).first()
        rel.remove()
        return self

    def act_remove_tag_by_name(self, tag_name):
        from app.dbc import Tag

        return self.act_remove_tag(Tag.get.by_name(tag_name).first())

    def act_set_tags(self, names):
        for tag in self.get_nonsorted_tags():
            self.act_remove_tag(tag)
        for name in names:
            self.act_add_tag_by_name(name)
        return self

    # ATTACHMENTS BLOCK

    def get_attachments(self):
        from app.dbc import Attachment

        return Attachment.get.by_parent(self).all()

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

    def has_attachment(self, attachment):
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

    def get_similar_problems_link(self):
        return url_for(
            "arch.archive_problem_search",
            tags="; ".join(self.get_tag_names()),
            page=1,
            username="all",
        )
