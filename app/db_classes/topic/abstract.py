from app.imports import *

from abc import abstractmethod
from app.dbc import AbstractStandardModel

class AbstractTagRelation(AbstractStandardModel):
    # --> INITIALIZE
    __abstract__ = True