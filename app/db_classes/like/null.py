from app.imports import *

from app.sqlalchemy_custom_types import *

from app.db_classes.like.abstract import AbstractLike


class NullLike(AbstractLike):
    # --> INITIALIZE
    __abstract__ = True

    # --> RELATIONS

    # --> PROPERTIES
    @property
    def parent_type(self) -> "DbParentType":
        return None  # TODO : should we write Null DbParentType?

    @parent_type.setter
    def parent_type(self, value: "DbParentType"):
        pass

    @property
    def parent_id(self) -> int:
        return -1

    @parent_id.setter
    def parent_id(self, value: int):
        pass

    @property
    def good(self) -> bool:
        return False

    @good.setter
    def good(self, value: bool):
        pass

    @property
    def bad(self) -> bool:
        return False

    @bad.setter
    def bad(self, value: bool):
        pass

    @property
    def user_id(self) -> int:
        return -1

    @user_id.setter
    def user_id(self, value: int):
        pass

    @property
    def user(self) -> "User":
        from app.db_classes.user.null import NullUser

        return NullUser()

    @user.setter
    def user(self, value: "User"):
        pass

    # --> METHODS
    def get_parent(self) -> "AbstractStandardModel":
        return None  # TODO : decide what to return

    @staticmethod
    def exists(parent, user=current_user) -> bool:
        return False

    @staticmethod
    def act_add_like_to_parent(parent, user=current_user, good=True):
        pass

    @staticmethod
    def act_remove_like_from_parent(parent, user=current_user):
        pass
