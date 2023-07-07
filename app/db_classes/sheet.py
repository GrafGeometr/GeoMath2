from app.imports import *
from app.sqlalchemy_custom_types import *


class Sheet(db.Model):
    # --> INITIALIZE
    __tablename__ = "sheet"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String)
    text = db.Column(db.String)
    is_public = db.Column(db.Boolean, default=False)

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
        db.session.delete(self)
        db.session.commit()

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

    def get_attachments(self):
        from app.dbc import Attachment

        return Attachment.query.filter_by(parent_type=DbParent.fromType(type(self)), parent_id=self.id).all()

    def is_archived(self):
        return self.is_public

    def is_text_available(self):
        return self.is_archived() or self.is_my()

    def is_my(self):
        relation = current_user.get_pool_relation(self.pool_id)
        if relation is None:
            return False
        if relation.role.isOwner() or relation.role.isParticipant():
            return True
        return False

    def is_have_tag(self, tag):
        if tag is None:
            return False
        from app.dbc import Tag_Relation

        if Tag_Relation.get_by_parent_and_tag(self, tag) is None:
            return False
        return True

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

        return self.act_add_tag(Tag.get_by_name(tag_name))

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

    def act_set_atgs(self, names):
        for tag in self.get_tags():
            self.act_remove_tag(tag)
        for name in names:
            self.act_add_tag_by_name(name)
        return self

    def save(self):
        db.session.commit()
        return self
