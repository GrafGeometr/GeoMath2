from app.imports import *

from app.db_classes.standard_model.null import NullStandardModel
from app.db_classes.tag.abstract import AbstractTag


class NullTag(NullStandardModel, AbstractTag):
    # --> INITIALIZE
    __abstract__ = True

    # --> RELATIONS

    # --> PROPERTIES
    @property
    def name(self):
        return ""

    @property
    def hash(self):
        return -1

    @hash.setter
    def hash(self, value):
        pass

    # --> METHODS
    @staticmethod
    def get_all_by_obj(obj):
        return []
