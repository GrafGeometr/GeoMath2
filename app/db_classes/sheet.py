from app.imports import *
from app.sqlalchemy_custom_types import *


class Sheet(db.Model):
    # --> INITIALIZE
    __tablename__ = "sheet"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String)
    text = db.Column(db.String)
    is_public = db.Column(db.Boolean, default=False)
    total_likes = db.Column(db.Integer, default=0)
    total_dislikes = db.Column(db.Integer, default=0)

    # --> RELATIONS
    pool_id = db.Column(db.Integer, db.ForeignKey("pool.id"))

    # --> FUNCTIONS
    def add(self):
        db.session.add(self)
        db.session.commit()
        return self

    def remove(self):
        for att in self.get_attachments():
            att.remove()
        from app.dbc import Like
        for l in Like.get_all_by_parent(self):
            l.remove(par=self)
        db.session.delete(self)
        db.session.commit()

    
    def is_liked(self):
        from app.dbc import Like
        return Like.query.filter_by(parent_type="Sheet", parent_id=self.id, user_id=current_user.id).first() is not None

    def act_add_like(self):
        if self.is_liked():
            return
        from app.dbc import Like
        Like(parent_type="Sheet", parent_id=self.id, user_id=current_user.id).add()
        return
    
    def act_remove_like(self):
        if not self.is_liked():
            return
        from app.dbc import Like
        Like.query.filter_by(parent_type="Sheet", parent_id=self.id, user_id=current_user.id).remove()
        return
    
    def get_all_likes(self):
        from app.dbc import Like
        return Like.get_all_by_parent(self)
    def get_all_likes_good(self):
        return [like for like in self.get_all_likes() if like.good]
    
    def get_all_likes_bad(self):
        return [like for like in self.get_all_likes() if not like.good]

    def get_attachments(self):
        from app.dbc import Attachment

        return Attachment.query.filter_by(parent_type=DbParent.fromType(type(self)), parent_id=self.id).all()

    def is_archived(self):
        return self.is_public

    def is_text_available(self, user=current_user):
        return self.is_archived() or self.is_my(user)
    
    def is_tags_available(self, user=current_user):
        return self.is_text_available(user)

    def is_my(self, user=current_user):
        return user.is_pool_access(self.pool_id)

    

    def get_nonsecret_attachments(self):
        result = []
        for attachment in self.get_attachments():
            if self.is_text_available():
                result.append(attachment)
        return result

    @staticmethod
    def get_by_id(id):
        return Sheet.query.filter_by(id=id).first()

    def act_set_name(self, name):
        self.name = name
        db.session.commit()
        return self

    def act_set_text(self, text):
        self.text = text
        db.session.commit()
        return self

    def act_set_is_public(self, is_public):
        self.is_public = is_public
        db.session.commit()
        return self

    def act_make_public(self):
        self.is_public = True
        db.session.commit()
        return self

    def act_make_nonpublic(self):
        self.is_public = False
        db.session.commit()
        return self

    

    def save(self):
        db.session.commit()
        return self

    # TAGS BLOCK

    def get_tags(self):
        from app.dbc import Tag, Tag_Relation

        return sorted(
            [
                Tag.query.filter_by(id=sheet_tag.tag_id).first()
                for sheet_tag in Tag_Relation.query.filter_by(
                    parent_type=DbParent.fromType(type(self)), parent_id=self.id
                ).all()
            ],
            key=lambda t: t.name.lower(),
        )
    
    def get_tag_names(self):
        return list(map(lambda t: t.name, self.get_tags()))
    
    def is_have_tag(self, tag):
        if tag is None:
            return False
        from app.dbc import Tag_Relation

        if Tag_Relation.get_by_parent_and_tag(self, tag) is None:
            return False
        return True
    
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
        if tag is None:
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
        for tag in self.get_tags():
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
                if self.is_text_available():
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

    def get_similar_sheets_link(self):
        return url_for("arch.archive_sheet_search", tags="; ".join(self.get_tag_names()), page=1, username="all")