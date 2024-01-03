from typing import List

from app.imports import *
from app.sqlalchemy_custom_types import *

from app.db_classes.model_with_name.normal import ModelWithName
from app.db_classes.sheet.abstract import AbstractSheet
from app.db_classes.sheet.getter import SheetGetter
from app.db_classes.sheet.null import NullSheet


class Sheet(ModelWithName, AbstractSheet):
    # --> INITIALIZE
    __abstract__ = False
    __tablename__ = "sheet"

    text_ = db.Column(db.String)
    is_public_ = db.Column(db.Boolean, default=False)
    total_likes_ = db.Column(db.Integer, default=0)
    total_dislikes_ = db.Column(db.Integer, default=0)

    # --> RELATIONS
    pool_id_ = db.Column(db.Integer, db.ForeignKey("pool.id_"))

    null_cls_ = NullSheet
    getter_cls_ = SheetGetter

    # --> PROPERTIES
    @property
    def tags(self) -> List["Tag"]:
        from app.dbc import TagRelation
        return [tr.tag for tr in TagRelation.get.by_parent(self).all()]
    
    @property
    def text(self):
        return self.text_

    @text.setter
    def text(self, text):
        self.text_ = text
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
        for att in self.get_attachments():
            att.remove()

        for l in self.get_all_likes():
            l.remove(par=self)
        db.session.delete(self)
        db.session.commit()

    def is_liked_by(self, user=current_user):
        from app.dbc import Like

        return Like.get.by_parent(self).by_user(user).all()

    def act_add_like(self, user=current_user):
        if self.is_liked():
            return
        from app.dbc import Like

        Like(parent_type_="Sheet", parent_id_=self.id, user_id_=user.id).add()
        self.total_likes += 1
        return self

    def act_remove_like(self, user=current_user):
        if not self.is_liked():
            return
        from app.dbc import Like

        Like.get.by_parent(self).by_user(user).remove()
        self.total_likes -= 1
        return self

    def get_all_likes(self):
        from app.dbc import Like

        return Like.get_all_by_parent(self)

    def get_all_good_likes(self):
        return [like for like in self.get_all_likes() if like.good]

    def get_all_bad_likes(self):
        return [like for like in self.get_all_likes() if not like.good]

    def is_archived(self):
        return self.is_public

    def is_text_available(self, user=current_user):
        return self.is_archived() or self.is_my(user)

    def is_tags_available(self, user=current_user):
        return self.is_text_available(user)

    def is_my(self, user=current_user):
        return user.is_pool_access(self.pool)

    # TAGS BLOCK

    def get_tags(self):
        from app.dbc import Tag

        return sorted(
            Tag.get_all_by_obj(self),
            key=lambda t: t.name.lower(),
        )

    def get_tag_names(self):
        return [tag.name for tag in self.tags]

    def has_tag(self, tag):
        from app.dbc import TagRelation

        return not TagRelation.get.by_parent(self).by_tag(tag).first().is_null()

    def act_add_tag(self, tag):
        from app.dbc import TagRelation

        if not self.is_my() or self.has_tag(tag):
            return self
        TagRelation(
            parent_type=DbParent.from_type(type(self)), parent_id=self.id, tag_id=tag.id
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
        for tag in self.tags:
            self.act_remove_tag(tag)
        for name in names:
            self.act_add_tag_by_name(name)
        return self

    # ATTACHMENTS BLOCK

    def get_attachments(self):
        from app.dbc import Attachment

        return Attachment.get.by_parent(self).all()

    def get_nonsecret_attachments(self):
        return [
            attachment
            for attachment in self.get_attachments()
            if not attachment.is_secret() and self.is_text_available()
        ]

    def has_attachment(self, attachment):
        return (
            attachment.parent_type == DbParent.from_type(type(self))
            and attachment.parent_id == self.id
        )

    def act_add_attachment(self, attachment):
        attachment.parent_type = DbParent.from_type(type(self))
        attachment.parent_id = self.id
        return self

    def act_add_attachment_by_db_filename(self, db_filename):
        from app.dbc import Attachment

        return self.act_add_attachment(
            Attachment.get.by_db_filename(db_filename).first()
        )

    def act_remove_attachment(self, attachment):
        attachment.parent_type = None  # TODO: why not attachment.remove()
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

    def get_similar_sheets_link(self):
        return url_for(
            "arch.archive_sheet_search",
            tags="; ".join(self.get_tag_names()),
            page=1,
            username="all",
        )
