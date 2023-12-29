from app.imports import *
from app.sqlalchemy_custom_types import *

from app.db_classes.friend.abstract import AbstractFriend


class NullFriend(AbstractFriend):
    # --> INITIALIZE
    __abstract__ = True

    # --> PROPERTIES
    @property
    def friend_from(self) -> int:
        return -1

    @friend_from.setter
    def friend_from(self, friend_from: int):
        pass

    @property
    def friend_to(self) -> int:
        return -1

    @friend_to.setter
    def friend_to(self, friend_to: int):
        pass

    @property
    def accepted(self) -> bool:
        return False

    @accepted.setter
    def accepted(self, accepted: bool):
        pass
