from abc import abstractmethod
from app.db_classes.standard_model.abstract import AbstractStandardModel


class AbstractModelWithHashedId(AbstractStandardModel):
    # --> INITIALIZE
    __abstract__ = True

    # --> PROPERTIES
    @property
    @abstractmethod
    def hashed_id(self) -> str:
        pass

    @hashed_id.setter
    @abstractmethod
    def hashed_id(self, hashed_id: str):
        pass

    # --> METHODS
    @abstractmethod
    def add(self) -> "AbstractModelWithHashedId":
        pass

    @abstractmethod
    def act_set_hashed_id(self) -> "AbstractModelWithHashedId":
        pass

    @classmethod
    @abstractmethod
    def get_by_hashed_id(cls, hashed_id: str) -> "AbstractModelWithHashedId":
        pass
