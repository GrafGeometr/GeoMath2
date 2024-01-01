from app.imports import *
from app.db_classes.standard_model.normal import StandardModel
from app.db_classes.model_with_hashed_id.abstract import AbstractModelWithHashedId
from app.db_classes.model_with_hashed_id.null import NullModelWithHashedId
from app.db_classes.model_with_hashed_id.getter import ModelWithHashedIdGetter


class ModelWithHashedId(StandardModel, AbstractModelWithHashedId):
    # --> INITIALIZE
    __abstract__ = True

    hashed_id_ = db.Column(db.String, unique=True, nullable=True)
    null_cls_ = NullModelWithHashedId

    getter_cls_ = ModelWithHashedIdGetter

    # --> PROPERTIES
    @property
    def hashed_id(self):
        return self.hashed_id_

    @hashed_id.setter
    def hashed_id(self, value):
        self.hashed_id_ = value
        self.save()

    # --> METHODS
    #def __init__(self):
        #super().__init__()
        #self.hashed_id = type(self).generate_hashed_id()

    @classmethod
    def generate_hashed_id(cls):
        while True:
            hashed_id = generate_token(20)
            if cls.get_by_hashed_id(hashed_id).is_null():
                break
        return hashed_id

    def add(self):
        db.session.add(self)
        self.act_set_hashed_id()
        return self

    def act_set_hashed_id(self):
        while True:
            hashed_id = generate_token(20)
            print("DEBUG")
            if type(self).get.by_hashed_id(hashed_id).first().is_null():
                break

        self.hashed_id = hashed_id
        return self

    @classmethod
    def get_by_hashed_id(cls, hashed_id):
        if hashed_id is None:
            return cls.null_cls_()
        result = cls.query.filter_by(hashed_id=hashed_id).first()
        if result is not None:
            return result
        return cls.null_cls_()
