from app.db_classes.standard_model.abstract import AbstractStandardModel


class NullStandardModel(AbstractStandardModel):
    # --> INITIALIZE
    __abstract__ = True

    # --> PROPERTIES
    @property
    def id(self):
        return -1

    # --> METHODS
    def save(self):
        return self

    def add(self):
        return self

    def remove(self):
        pass

    def is_null(self):
        return True

    @classmethod
    def get_by_id(cls, id_):
        return cls()

    @classmethod
    def get_all(cls):
        return []
