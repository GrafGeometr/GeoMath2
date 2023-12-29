from app.imports import *
from app.sqlalchemy_custom_types import *

from abc import abstractmethod
from app.db_classes.standard_model.null import NullStandardModel
from app.db_classes.tag_relation.abstract import AbstractTagRelation


class NullTagRelation(NullStandardModel, AbstractTagRelation):
    # --> INITIALIZE
    __abstract__ = True

    # --> RELATIONS

    # --> PROPERTIES
    @property
    def tag_id(self):
        return -1

    @tag_id.setter
    def tag_id(self, value):
        pass

    @property
    def parent_id(self):
        return -1

    @parent_id.setter
    def parent_id(self, value):
        pass

    @property
    def parent_type(self):
        return None  # TODO what should be returned here?

    @parent_type.setter
    def parent_type(self, value):
        pass

    @property
    def other_data(self):
        return {}

    @other_data.setter
    def other_data(self, value):
        pass

    # --> METHODS

    def get_parent(self):
        pass  # TODO what should be returned here?

    @staticmethod
    def get_all_by_parent(parent):
        return []
