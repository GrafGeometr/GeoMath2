from app.imports import *
from app.sqlalchemy_custom_types import *

from app.db_classes.standard_model.null import NullStandardModel
from app.db_classes.user_to_club_relation.abstract import AbstractUserToClubRelation


class NullUserToClubRelation(AbstractUserToClubRelation, NullStandardModel):
    # --> INITIALIZE
    __abstract__ = True
    __tablename__ = "user_club"

    # --> RELATIONS

    # --> PROPERTIES
    @property
    def role(self):
        return Null_Role

    @role.setter
    def role(self, value):
        pass

    @property
    def user_id(self):
        return -1

    @user_id.setter
    def user_id(self, value):
        pass

    @property
    def club_id(self):
        return -1

    @club_id.setter
    def club_id(self, value):
        pass

    # --> METHODS
