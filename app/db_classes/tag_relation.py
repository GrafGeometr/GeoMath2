from app.imports import *
from app.sqlalchemy_custom_types import *

from app.db_classes.standart_database_classes import *


class Tag_Relation(db.Model, StandartModel):
    # --> INITIALIZE
    __tablename__ = "tag_relation"

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
