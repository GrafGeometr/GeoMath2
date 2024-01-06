from abc import abstractmethod
from app.db_classes.standard_model.abstract import AbstractStandardModel


class AbstractModelWithName(AbstractStandardModel):
    # --> INITIALIZE
    __abstract__ = True

    # --> PROPERTIES
    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @name.setter
    @abstractmethod
    def name(self, name: str):
        pass

    # --> METHODS
