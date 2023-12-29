from app.imports import *
from app.sqlalchemy_custom_types import *

from app.db_classes.standard_model.null import NullStandardModel
from app.db_classes.admin_password.abstract import AbstractAdminPassword


class NullAdminPassword(NullStandardModel, AbstractAdminPassword):
    # --> INITIALIZE
    __abstract__ = True

    # --> PROPERTIES
    @property
    def password(self):
        return None

    @password.setter
    def password(self, password):
        pass
