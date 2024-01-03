from app.imports import *
from app.sqlalchemy_custom_types import *

from abc import abstractmethod
from app.db_classes.standard_model.null import NullStandardModel
from app.db_classes.topic.abstract import AbstractTopic


class NullTopic(NullStandardModel, AbstractTopic):
    # --> INITIALIZE
    __abstract__ = True