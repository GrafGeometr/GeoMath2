from app.imports import *
from app.sqlalchemy_custom_types import *

from app.db_classes.standart_database_classes import *


class Problem(db.Model, ModelWithHashedId, ModelWithName):
    # --> INITIALIZE
    __tablename__ = "problem"

    statement = db.Column(db.String)
    solution = db.Column(db.String)
    is_public = db.Column(db.Boolean, default=False)
    total_likes = db.Column(db.Integer, default=0)
    total_dislikes = db.Column(db.Integer, default=0)

    # --> RELATIONS
    pool_id = db.Column(db.Integer, db.ForeignKey("pool.id"))
    contest_problems = db.relationship("Contest_Problem", backref="problem")

    # --> FUNCTIONS
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

    def set_is_public(self, is_public: bool) -> "Problem":
        self.is_public = is_public
        db.session.commit()
        return self
    
    def get_pool(self):
        from app.dbc import Pool_Null
        if (self.pool):
            return self.pool
        return Pool_Null()
    
    @staticmethod
    def get_by_hashed_id(hashed_id: string) -> "Problem":
        from app.dbc import Problem_Null
        problem = Problem.query.filter_by(hashed_id=hashed_id).first()
        if problem is None:
            problem = Problem_Null()
        return problem

    def is_liked(self):
        from app.dbc import Like

        return (
            Like.query.filter_by(
                parent_type="Problem", parent_id=self.id, user_id=current_user.id
            ).first()
            is not None
        )

    def act_add_like(self):
        if self.is_liked():
            return
        from app.dbc import Like

        Like(parent_type="Problem", parent_id=self.id, user_id=current_user.id).add()
        return

    def act_remove_like(self):
        if not self.is_liked():
            return
        from app.dbc import Like

        Like.query.filter_by(
            parent_type="Problem", parent_id=self.id, user_id=current_user.id
        ).remove()
        return

    def act_set_statement(self, statement):
        self.statement = statement
        return self.save()

    def act_set_solution(self, solution):
        self.solution = solution
        return self.save()

    def act_set_is_public(self, is_public):
        self.is_public = is_public
        return self.save()

    def act_make_public(self):
        self.is_public = True
        return self.save()

    def act_make_nonpublic(self):
        self.is_public = False
        return self.save()

    def is_archived(self):
        return self.is_public

    def get_all_contests(self):
        return [cp.contest for cp in self.contest_problems]

    def get_cu_participated(self, user=current_user):
        from app.dbc import Contest_User

        result = []
        for c in self.get_all_contests():
            result.extend(Contest_User.get_all_by_contest_and_user(c, current_user))
        return result

    def get_all_likes(self):
        from app.dbc import Like

        return Like.get_all_by_parent(self)

    def get_all_likes_good(self):
        return [like for like in self.get_all_likes() if like.good]

    def get_all_likes_bad(self):
        return [like for like in self.get_all_likes() if not like.good]

    def is_statement_available(self, user=current_user):
        from app.dbc import Contest_User_Solution

        all_cp = [cp for cp in self.contest_problems if cp.is_valid()]
        if any([user.is_judge(cp.contest) for cp in all_cp]):
            return True

        all_cus = []
        for cp in all_cp:
            all_cus.extend(
                Contest_User_Solution.query.filter_by(contest_problem_id=cp.id).all()
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
        from app.dbc import Contest_User_Solution

        all_cp = [cp for cp in self.contest_problems if cp.is_valid()]
        if any([user.is_judge(cp.contest) for cp in all_cp]):
            return True

        all_cus = []
        for cp in all_cp:
            all_cus.extend(
                Contest_User_Solution.query.filter_by(contest_problem_id=cp.id).all()
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
        from app.dbc import Contest_Problem

        return Contest_Problem.get_by_contest_and_problem(contest, self) is not None

    @staticmethod
    def get_all_by_pool(pool):
        if pool is None:
            return []
        return Problem.query.filter_by(pool_id=pool.id).all()

    # TAGS BLOCK

    def get_nonsorted_tags(self):
        from app.dbc import Tag, Tag_Relation

        return [
            Tag.query.filter_by(id=sheet_tag.tag_id).first()
            for sheet_tag in Tag_Relation.query.filter_by(
                parent_type=DbParent.fromType(type(self)), parent_id=self.id
            ).all()
        ]

    def get_tags(self):
        return sorted(self.get_nonsorted_tags(), key=lambda t: t.name.lower())

    def get_tag_names(self):
        return list(map(lambda t: t.name, self.get_tags()))

    def is_have_tag(self, tag):
        if tag is None:
            return False
        from app.dbc import Tag_Relation

        if Tag_Relation.get_by_parent_and_tag(self, tag) is None:
            return False
        return True

    def act_add_tags(self, tags):
        for tag in tags:
            self.act_add_tag(tag)
        return self

    def act_add_tag(self, tag):
        from app.dbc import Tag_Relation

        if tag is None:
            return self
        if not self.is_my():
            return self
        if self.is_have_tag(tag):
            return self
        Tag_Relation(
            parent_type=DbParent.fromType(type(self)), parent_id=self.id, tag_id=tag.id
        ).add()
        return self

    def act_add_tag_by_name(self, tag_name):
        from app.dbc import Tag

        tag = Tag.get_by_name(tag_name)
        if (tag is None) and (current_user.admin):
            tag = Tag(name=tag_name).add()

        return self.act_add_tag(tag)

    def act_remove_tag(self, tag):
        from app.dbc import Tag_Relation

        if tag is None:
            return self
        if not self.is_my():
            return self
        rel = Tag_Relation.get_by_parent_and_tag(self, tag)
        if rel is not None:
            rel.remove()
        return self

    def act_remove_tag_by_name(self, tag_name):
        from app.dbc import Tag

        return self.act_remove_tag(Tag.get_by_name(tag_name))

    def act_set_tags(self, names):
        for tag in self.get_nonsorted_tags():
            self.act_remove_tag(tag)
        for name in names:
            self.act_add_tag_by_name(name)
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
        return (
            attachment.parent_type == DbParent.fromType(type(self))
            and attachment.parent_id == self.id
        )

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

    def get_similar_problems_link(self):
        return url_for(
            "arch.archive_problem_search",
            tags="; ".join(self.get_tag_names()),
            page=1,
            username="all",
        )
