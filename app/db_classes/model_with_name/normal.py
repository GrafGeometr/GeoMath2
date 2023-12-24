from app.imports import *
from app.db_classes.standard_model.normal import StandardModel
from app.db_classes.model_with_name.abstract import AbstractModelWithName
from app.db_classes.model_with_name.null import NullModelWithName


class ModelWithName(StandardModel, AbstractModelWithName):
    # --> INITIALIZE
    __abstract__ = True

    name_ = db.Column(db.String, unique=True)
    null_cls = NullModelWithName

    # --> PROPERTIES
    @property
    def name(self):
        return self.name_

    @name.setter
    def name(self, value):
        self.name_ = value
        self.save()

    # --> METHODS
    def act_set_name(self, name):
        self.name = name
        return self

    @classmethod
    def get_by_name(cls, name):
        result = cls.query.filter_by(name=name).first()
        if result is not None:
            return result
        return cls.null_cls()
