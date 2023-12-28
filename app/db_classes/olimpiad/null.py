from typing import List

from app.imports import *

from app.sqlalchemy_custom_types import *

from app.db_classes.model_with_name.null import NullModelWithName
from app.db_classes.olimpiad.abstract import AbstractOlimpiad


class NullOlimpiad(AbstractOlimpiad, NullModelWithName):
    # --> INITIALIZE
    __abstract__ = True

    # --> RELATIONS

    # --> PROPERTIES
    @property
    def short_name(self) -> str:
        return ""

    @short_name.setter
    def short_name(self, value: str):
        pass

    @property
    def category(self) -> str:
        return ""

    @category.setter
    def category(self, value: str):
        pass

    @property
    def contests(self) -> List["Contest"]:
        return []

    # --> METHODS
    def num_of_seasons_to_str(self) -> str:
        return ""

    def act_add_contest(self, contest: "AbstractContest") -> "AbstractOlimpiad":
        pass

    def get_structure(self) -> "OrderedDict":
        return OrderedDict()

    def get_seasons_list(self) -> List[str]:
        return []

    def get_grades_list(self) -> List[str]:
        return []

    def fix_name(self) -> "AbstractOlimpiad":
        return self
