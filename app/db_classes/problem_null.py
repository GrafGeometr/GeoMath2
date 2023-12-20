from app.imports import *
from app.sqlalchemy_custom_types import *

from app.db_classes.standart_database_classes import *


class Problem_Null:
    def __init__(self):
        pass


    def set_is_public(self, is_public: bool) -> "Problem":
        return self