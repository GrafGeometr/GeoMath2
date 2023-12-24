from app.imports import *
from app.sqlalchemy_custom_types import *

from app.dbc import AbstractUserToClubRelation, StandardModel


class UserToClubRelation(AbstractUserToClubRelation, StandardModel):
    # --> INITIALIZE
    __abstract__ = False
    __tablename__ = "user_club"

    role_ = db.Column(RoleType)

    # --> RELATIONS
    user_id_ = db.Column(db.Integer, db.ForeignKey("user.id_"))
    club_id_ = db.Column(db.Integer, db.ForeignKey("club.id_"))

    # --> PROPERTIES
    @property
    def role(self):
        return self.role_

    @role.setter
    def role(self, value):
        self.role_ = value
        self.save()

    @property
    def user_id(self):
        return self.user_id_

    @user_id.setter
    def user_id(self, value):
        self.user_id_ = value
        self.save()

    @property
    def club_id(self):
        return self.club_id_

    @club_id.setter
    def club_id(self, value):
        self.club_id_ = value
        self.save()

    # --> METHODS
