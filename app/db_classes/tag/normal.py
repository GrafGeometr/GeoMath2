from app.imports import *

from app.db_classes.standard_model.normal import StandardModel
from .abstract import AbstractChat
from .null import NullChat
from .getter import Getter


class Tag(ModelWithName, AbstractTag):
    # --> INITIALIZE
    __abstract__ = False
    __tablename__ = "tag"

    hash_ = db.Column(db.Integer, nullable=True)

    # --> RELATIONS

    # --> PROPERTIES
    @property
    def hash(self):
        return self.hash_

    @hash.setter
    def hash(self, value):
        self.hash_ = value
        self.save()

    # --> METHODS
    @staticmethod
    def get_all_by_obj(obj):
        from app.dbc import TagRelation

        return [tr.tag for tr in TagRelation.get.by_parent(obj).all()]

    def add(self):
        t = Tag.get_by_name(self.name)
        if t is not None:
            return t
        db.session.add(self)
        db.session.commit()
        return self

    def remove(self):
        raise NotImplementedError("Emplement remove tag")

    def get_hash(self):
        from app.utils_and_functions.usefull_functions import get_string_hash

        if self.hash is None:
            self.hash = get_string_hash(self.name.lower())
            self.save()
        return self.hash
