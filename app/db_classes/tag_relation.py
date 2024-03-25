from app.imports import *
from app.sqlalchemy_custom_types import *


class Tag_Relation(db.Model):
    # --> INITIALIZE
    __tablename__ = "tag_relation"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tag_id = db.Column(db.Integer)
    parent_type = db.Column(DbParentType)
    # parent_type = db.Column(db.String)  # 'Problem' | 'Sheet'
    parent_id = db.Column(db.Integer)
    other_data = db.Column(db.JSON, default={})

    # --> RELATIONS

    # --> FUNCTIONS
    def get_parent(self):
        par_type = self.parent_type.toType()
        if par_type is None:
            return None
        return par_type.get_by_id(self.parent_id)

    def add(self):
        db.session.add(self)
        return self.save()

    def remove(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def get_by_id(id):
        return Tag_Relation.query.filter_by(id=id).first()

    @staticmethod
    def get_all_by_parent(parent):
        if parent is None:
            return []
        parent_type = DbParent.fromType(type(parent))
        if parent_type is None:
            return []
        return Tag_Relation.query.filter_by(
            parent_type=parent_type, parent_id=parent.id
        ).all()

    @staticmethod
    def get_by_parent_and_tag(parent, tag):
        if parent is None or tag is None:
            return None
        return Tag_Relation.query.filter_by(
            parent_type=DbParent.fromType(type(parent)),
            parent_id=parent.id,
            tag_id=tag.id,
        ).first()
    
    @staticmethod
    def get_all_by_tag_id(tag_id):
        return Tag_Relation.query.filter_by(tag_id=tag_id).all()

    def save(self):
        db.session.commit()
        return self
