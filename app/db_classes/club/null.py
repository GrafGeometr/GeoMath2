from typing import List

from app.imports import *
from app.sqlalchemy_custom_types import *

from app.db_classes.standard_model.null import NullStandardModel
from app.db_classes.club.abstract import AbstractClub


class NullClub(NullStandardModel, AbstractClub):
    # --> INITIALIZE
    __abstract__ = True

    # --> PROPERTIES
    @property
    def user_clubs(self) -> List["User_Club"]:
        return []

    @user_clubs.setter
    def user_clubs(self, user_clubs: List["User_Club"]):
        pass

    @property
    def chats(self) -> List["Chat"]:
        return []

    @chats.setter
    def chats(self, chats: List["Chat"]):
        pass

    @property
    def club_contests(self) -> List["Club_Contest"]:
        return []

    @club_contests.setter
    def club_contests(self, club_contests: List["Club_Contest"]):
        pass
