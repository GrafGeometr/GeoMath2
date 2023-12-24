from app.db_classes.standard_model.null import NullStandardModel
from app.db_classes.model_with_name.abstract import AbstractModelWithName


class NullModelWithName(NullStandardModel, AbstractModelWithName):
    # --> INITIALIZE
    __abstract__ = True

    # --> PROPERTIES
    @property
    def name(self):
        return ""

    @name.setter
    def name(self, value):
        pass

    # --> METHODS
    def act_set_name(self, name):
        return self

    @classmethod
    def get_by_name(cls, name):
        return cls()
