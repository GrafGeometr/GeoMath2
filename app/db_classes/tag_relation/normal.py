from app.imports import *
from app.sqlalchemy_custom_types import *

from app.db_classes.tag_relation.abstract import AbstractTagRelation
from app.db_classes.standard_model.normal import StandardModel
from app.db_classes.tag_relation.getter import TagRelationGetter
from app.db_classes.tag_relation.null import NullTagRelation


class TagRelation(StandardModel, AbstractTagRelation):
    # --> INITIALIZE
    __abstract__ = False
    __tablename__ = "tag_relation"

    tag_id_ = db.Column(db.Integer)
    parent_type_ = db.Column(DbParentType)
    # parent_type = db.Column(db.String)  # 'Problem' | 'Sheet'
    parent_id_ = db.Column(db.Integer)
    other_data_ = db.Column(db.JSON, default={})

    null_cls_ = NullTagRelation
    getter_cls_ = TagRelationGetter

    # --> RELATIONS

    # --> PROPERTIES
    @property
    def tag_id(self):
        return self.tag_id_

    @tag_id.setter
    def tag_id(self, value):
        self.tag_id_ = value
        self.save()

    @property
    def parent_type(self):
        return self.parent_type_

    @parent_type.setter
    def parent_type(self, value):
        self.parent_type_ = value
        self.save()

    @property
    def parent_id(self):
        return self.parent_id_

    @parent_id.setter
    def parent_id(self, value):
        self.parent_id_ = value
        self.save()

    @property
    def other_data(self):
        return self.other_data_

    @other_data.setter
    def other_data(self, value):
        self.other_data_ = value
        self.save()

    # --> METHODS
    def get_parent(self):
        par_type = self.parent_type.to_type()
        if par_type is None:
            return None
        return par_type.get_by_id(self.parent_id)
