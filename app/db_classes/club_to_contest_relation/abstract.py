from app.imports import *
from app.sqlalchemy_custom_types import *

from abc import abstractmethod
from app.db_classes.standard_model.normal import AbstractStandardModel


class AbstractClubToContestRelation(AbstractStandardModel):
    # --> INITIALIZE
    __abstract__ = True

    # --> PROPERTIES
    @property
    @abstractmethod
    def club_id(self) -> int:
        pass

    @club_id.setter
    @abstractmethod
    def club_id(self, club_id: int):
        pass

    @property
    @abstractmethod
    def contest_id(self) -> int:
        pass

    @contest_id.setter
    @abstractmethod
    def contest_id(self, contest_id: int):
        pass
