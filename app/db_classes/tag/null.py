from app.imports import *

from app.dbc import NullModelWithName, AbstractTag


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
