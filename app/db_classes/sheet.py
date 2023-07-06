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

    def remove(self):
        db.session.delete(self)
        db.session.commit()

    def get_tags(self):
        from app.dbc import Tag, Tag_Relation
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
        from app.dbc import Attachment
        return Attachment.query.filter_by(parent_type="Sheet", parent_id=self.id).all()

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

    def get_nonsecret_attachments(self):
        result = []
        for attachment in self.get_attachments():
            if self.is_text_available():
                result.append(attachment)
        return result
    
    @staticmethod
    def get_by_id(id):
        return Sheet.query.filter_by(id=id).first()