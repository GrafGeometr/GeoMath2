from app.db_classes.model_with_name.getter import ModelWithNameGetter
from app.imports import *
from app.db_classes.standard_model.normal import StandardModel
from app.db_classes.model_with_name.abstract import AbstractModelWithName
from app.db_classes.model_with_name.null import NullModelWithName


class ModelWithName(StandardModel, AbstractModelWithName):
    # --> INITIALIZE
    __abstract__ = True

    name_ = db.Column(db.String, unique=True)
    null_cls_ = NullModelWithName

    getter_cls_ = ModelWithNameGetter

    # --> PROPERTIES
    @property
    def name(self):
        return self.name_

    @name.setter
    def name(self, value):
        self.name_ = value
        self.save()

    # --> METHODS
