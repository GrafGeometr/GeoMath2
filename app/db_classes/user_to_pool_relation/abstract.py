from abc import abstractmethod
from app.sqlalchemy_custom_types import *
from app.dbc import AbstractStandardModel


class AbstractUserToPoolRelation(AbstractStandardModel):
    # --> INITIALIZE
    __abstract__ = True

    # --> PROPERTIES
    @property
    @abstractmethod
    def role(self) -> "Role":
        pass

    @role.setter
    @abstractmethod
    def role(self, value: "Role"):
        pass

    @property
    @abstractmethod
    def user_id(self) -> int:
        pass

    @user_id.setter
    @abstractmethod
    def user_id(self, value: int):
        pass

    @property
    @abstractmethod
    def user(self) -> "User":
        pass

    @user.setter
    @abstractmethod
    def user(self, user: "User"):
        pass

    @property
    @abstractmethod
    def pool_id(self) -> int:
        pass

    @pool_id.setter
    @abstractmethod
    def pool_id(self, value: int):
        pass

    @property
    @abstractmethod
    def pool(self) -> "Pool":
        pass

    @pool.setter
    @abstractmethod
    def pool(self, pool: "Pool"):
        pass

    # --> METHODS
    @abstractmethod
    def act_accept_invitation(self):
        pass
