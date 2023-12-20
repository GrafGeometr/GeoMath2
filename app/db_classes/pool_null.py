from app.imports import *
from app.sqlalchemy_custom_types import *

from app.db_classes.standart_database_classes import *


class Pool_Null:
    def __init__(self):
        pass
    
    def check_user_access(self, current_user) -> bool:
        from app.log import Exception_Access_Denied
        Exception_Access_Denied(self).flash()
        return False
    
    def check_user_owner(self, current_user) -> bool:
        from app.log import Exception_Access_Denied
        Exception_Access_Denied(self).flash()
        return False
    
    def get_name(self) -> str:
        return ""