from app.imports import *
from app.sqlalchemy_custom_types import *

from abc import abstractmethod
from app.db_classes.standard_model.normal import AbstractStandardModel


class AbstractClub(AbstractStandardModel):
    # --> INITIALIZE
    __abstract__ = True

    # --> PROPERTIES
    @property
    @abstractmethod
    def user_clubs(self) -> list["User_Club"]:
        pass

    @user_clubs.setter
    @abstractmethod
    def user_clubs(self, user_clubs: list["User_Club"]):
        pass

    @property
    @abstractmethod
    def chats(self) -> list["Chat"]:
        pass

    @chats.setter
    @abstractmethod
    def chats(self, chats: list["Chat"]):
        pass

    @property
    @abstractmethod
    def club_contests(self) -> list["Club_Contest"]:
        pass

    @club_contests.setter
    @abstractmethod
    def club_contests(self, club_contests: list["Club_Contest"]):
        pass
