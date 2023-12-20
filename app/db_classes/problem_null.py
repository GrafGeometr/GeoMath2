from app.imports import *
from app.sqlalchemy_custom_types import *

from app.db_classes.standart_database_classes import *

class Problem_Null:
    def __init__(self):
        pass


    def set_is_public(self, is_public: bool) -> "Problem":
        return self
    
    def remove(self) -> "Problem":
        return self
    
    def get_pool(self):
        from app.dbc import Pool_Null
        return Pool_Null()