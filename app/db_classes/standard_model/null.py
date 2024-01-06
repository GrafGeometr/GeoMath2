from app.db_classes.standard_model.abstract import AbstractStandardModel
from app.db_classes.getter.getter import NullGetter


class NullStandardModel(AbstractStandardModel):
    # --> INITIALIZE
    __abstract__ = True

    getter_cls_ = NullGetter
    getter_singleton_ = None

    @classmethod
    @property
    def get(cls):
        if cls.getter_singleton_ is None:
            cls.getter_singleton_ = cls.getter_class_(cls)
        return cls.getter_singleton_

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

    def __str__(self):
        return f"{self.__class__.__name__}()"

    def __repr__(self):
        return f"{self.__class__.__name__}()"
