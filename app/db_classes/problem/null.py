from app.imports import *
from app.sqlalchemy_custom_types import *




class ProblemNull:
    def __init__(self):
        pass

    def set_is_public(self, is_public: bool) -> "ProblemNull":
        return self

    def remove(self) -> "ProblemNull":
        return self

    def get_pool(self):
        from app.dbc import Pool_Null
        return Pool_Null()
