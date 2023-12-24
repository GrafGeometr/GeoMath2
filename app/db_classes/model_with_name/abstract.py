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
    @abstractmethod
    def act_set_name(self, name: str):
        pass

    @classmethod
    def get_by_name(cls, name: str) -> "AbstractModelWithName":
        pass
