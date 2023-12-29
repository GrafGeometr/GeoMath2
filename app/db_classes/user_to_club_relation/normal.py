from app.imports import *
from app.sqlalchemy_custom_types import *

from app.db_classes.standard_model.normal import StandardModel
from app.db_classes.user_to_club_relation.abstract import AbstractUserToClubRelation
from app.db_classes.user_to_club_relation.getter import UserToClubRelationGetter
from app.db_classes.user_to_club_relation.null import NullUserToClubRelation


class UserToClubRelation(AbstractUserToClubRelation, StandardModel):
    # --> INITIALIZE
    __abstract__ = False
    __tablename__ = "user_to_club_relation"

    role_ = db.Column(RoleType)

    # --> RELATIONS
    user_id_ = db.Column(db.Integer, db.ForeignKey("user.id_"))
    club_id_ = db.Column(db.Integer, db.ForeignKey("club.id_"))

    null_cls_ = NullUserToClubRelation
    getter_cls_ = UserToClubRelationGetter

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
