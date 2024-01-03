from app.imports import *

from abc import abstractmethod
from app.dbc import AbstractStandardModel

class AbstractTopic(AbstractStandardModel):
    # --> INITIALIZE
    __abstract__ = True