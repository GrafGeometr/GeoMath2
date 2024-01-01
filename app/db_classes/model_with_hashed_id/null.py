from app.db_classes.standard_model.null import NullStandardModel
from app.db_classes.model_with_hashed_id.abstract import AbstractModelWithHashedId


class NullModelWithHashedId(NullStandardModel, AbstractModelWithHashedId):
    # --> INITIALIZE
    __abstract__ = True

    # --> PROPERTIES
    @property
    def hashed_id(self):
        return ""

    @hashed_id.setter
    def hashed_id(self, value):
        pass

    # --> METHODS
    def add(self):
        return self

    def act_set_hashed_id(self):
        return self

    @classmethod
    def get_by_hashed_id(cls, hashed_id):
        return cls()
