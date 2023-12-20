from app.imports import *
from app.sqlalchemy_custom_types import *

from app.db_classes.standart_database_classes import *


class User_Null:
    def __init__(self):
        pass


    def get_id(self) -> int:
        return -1