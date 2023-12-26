from app.imports import *

from app.db_classes.standard_model.abstract import AbstractStandardModel
from app.db_classes.standard_model.null import NullStandardModel


class StandardModel(AbstractStandardModel):
    # --> INITIALIZE
    __abstract__ = True

    id_ = db.Column(db.Integer, primary_key=True, autoincrement=True)
    null_cls = NullStandardModel

    

    # --> PROPERTIES
    
    from app.db_classes.getter.getter import BaseGetter
    getter_class_ = BaseGetter
    getter_singleton_ = None
    @classmethod
    @property
    def get(cls):
        if cls.getter_singleton_ is None:
            getter_singleton_ = cls.getter_class_(cls)
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

    @classmethod
    def get_by_id(cls, id_):
        result = cls.query.filter_by(id=id_).first()
        if result is not None:
            return result
        return cls.null_cls()

    @classmethod
    def get_all(cls):
        return cls.query.all()


StandardModel.query = db.session.query_property()
