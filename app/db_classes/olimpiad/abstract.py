from typing import List

from app.imports import *

from app.sqlalchemy_custom_types import *

from abc import abstractmethod
from app.db_classes.standard_model.abstract import AbstractStandardModel


class AbstractOlimpiad(AbstractStandardModel):
    # --> INITIALIZE
    __abstract__ = True

    # --> RELATIONS

    # --> PROPERTIES
    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @name.setter
    @abstractmethod
    def name(self, value: str):
        pass

    @property
    @abstractmethod
    def short_name(self) -> str:
        pass

    @short_name.setter
    @abstractmethod
    def short_name(self, value: str):
        pass

    @property
    @abstractmethod
    def category(self) -> str:
        pass

    @category.setter
    @abstractmethod
    def category(self, value: str):
        pass

    @property
    @abstractmethod
    def contests(self) -> List["Contest"]:
        pass

    # --> METHODS
    @abstractmethod
    def num_of_seasons_to_str(self) -> str:
        pass

    @abstractmethod
    def act_add_contest(self, contest: "AbstractContest") -> "AbstractOlimpiad":
        pass

    @abstractmethod
    def get_structure(self) -> "OrderedDict":
        pass

    @abstractmethod
    def get_seasons_list(self) -> List[str]:
        pass

    @abstractmethod
    def get_grades_list(self) -> List[str]:
        pass

    @abstractmethod
    def fix_name(self) -> "AbstractOlimpiad":
        pass
