from app.imports import *
from app.sqlalchemy_custom_types import *

class Sheet(db.Model):
    __tablename__ = "sheet"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String)
    text = db.Column(db.String)

    is_public = db.Column(db.Boolean, default=False)

    pool_id = db.Column(db.Integer, db.ForeignKey("pool.id"))

    def get_tags(self):
        return sorted(
            [
                Tag.query.filter_by(id=sheet_tag.tag_id).first()
                for sheet_tag in Tag_Relation.query.filter_by(
                    parent_type="Sheet", parent_id=self.id
                ).all()
            ],
            key=lambda t: t.name.lower(),
        )

    def get_tag_names(self):
        return list(map(lambda t: t.name, self.get_tags()))

    def get_attachments(self):
        return Attachment.query.filter_by(parent_type="Sheet", parent_id=self.id).all()

    def is_archived(self):
        return self.is_public

    def is_text_available(self):
        if self.is_public:
            return True
        relation = current_user.get_pool_relation(self.pool_id)
        if relation.role.isOwner() or relation.role.isParticipant():
            return True
        return False

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
            if self.is_text_available():
                result.append(attachment)
        return result