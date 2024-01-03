from app.imports import *

from app.db_classes.standard_model.abstract import AbstractStandardModel
from app.db_classes.standard_model.null import NullStandardModel
from app.db_classes.standard_model.getter import StandardModelGetter


class StandardModel(AbstractStandardModel):
    # --> INITIALIZE
    __abstract__ = True

    id_ = db.Column(db.Integer, primary_key=True, autoincrement=True)
    null_cls_ = NullStandardModel

    # --> PROPERTIES

    getter_cls_ = StandardModelGetter
    getter_singleton_ = None

    @classmethod
    @property
    def get(cls):
        if cls.getter_singleton_ is None:
            cls.getter_singleton_ = cls.getter_cls_(cls)
        return cls.getter_singleton_

    @property
    def id(self):
        return self.id_

    @id.setter
    def id(self, value):
        self.id_ = value

    # --> METHODS
    def save(self):
        db.session.commit()
        return self

    def add(self):
        db.session.add(self)
        return self.save()

    def remove(self):
        db.session.delete(self)
        db.session.commit()

    def is_null(self):
        return False
