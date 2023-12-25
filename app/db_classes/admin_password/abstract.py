from app.imports import *
from app.sqlalchemy_custom_types import *

from abc import abstractmethod
from app.db_classes.standard_model.normal import AbstractStandardModel


class AbstractPassword(AbstractStandardModel):
    # --> INITIALIZE
    __abstract__ = True