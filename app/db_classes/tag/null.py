from app.imports import *

from app.db_classes.model_with_name.null import NullModelWithName
from app.db_classes.tag.abstract import AbstractTag


class NullTag(NullModelWithName, AbstractTag):
    # --> INITIALIZE
    __abstract__ = True

    # --> RELATIONS

    # --> PROPERTIES
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
