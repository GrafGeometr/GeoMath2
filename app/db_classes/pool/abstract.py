from typing import List

from app.imports import *
from app.sqlalchemy_custom_types import *

from abc import abstractmethod
from app.db_classes.model_with_name.abstract import AbstractModelWithName
from app.db_classes.model_with_hashed_id.abstract import AbstractModelWithHashedId
from app.db_classes.invite.null import NullInvite


class AbstractPool(AbstractModelWithHashedId, AbstractModelWithName):
    # --> INITIALIZE
    __abstract__ = True

    # --> RELATIONS

    # --> PROPERTIES
    @property
    @abstractmethod
    def user_to_pool_relations(self) -> List["UserToPoolRelation"]:
        pass

    @user_to_pool_relations.setter
    @abstractmethod
    def user_to_pool_relations(self, value: List["UserToPoolRelation"]):
        pass

    @property
    @abstractmethod
    def problems(self) -> List["Problem"]:
        pass

    @problems.setter
    @abstractmethod
    def problems(self, value: List["Problem"]):
        pass

    @property
    @abstractmethod
    def sheets(self) -> List["Sheet"]:
        pass

    @sheets.setter
    @abstractmethod
    def sheets(self, value: List["Sheet"]):
        pass

    @property
    @abstractmethod
    def contests(self) -> List["Contest"]:
        pass

    @contests.setter
    @abstractmethod
    def contests(self, value: List["Contest"]):
        pass

    # --> METHODS
    @abstractmethod
    def contains_user(self, user=current_user) -> bool:
        pass

    @abstractmethod
    def is_my(self) -> bool:
        pass

    @abstractmethod
    def check_user_access(self, current_user) -> bool:
        pass

    @abstractmethod
    def check_user_owner(self, current_user) -> bool:
        pass

    @abstractmethod
    def add_user(self, user=current_user, role=Participant) -> "AbstractPool":
        pass

    @abstractmethod
    def remove_user(self, user=current_user) -> "AbstractPool":
        pass

    @abstractmethod
    def add_user_by_invite(
        self, user=current_user, invite=NullInvite()
    ) -> "AbstractPool":
        pass

    @abstractmethod
    def act_generate_new_invite_code(self) -> "AbstractInvite":
        pass

    @abstractmethod
    def get_users(self) -> List["User"]:
        pass

    @abstractmethod
    def get_owners(self) -> List["User"]:
        pass

    @abstractmethod
    def count_owners(self) -> int:
        pass

    @abstractmethod
    def get_participants(self) -> List["User"]:
        pass

    @abstractmethod
    def count_participants(self) -> int:
        pass

    @abstractmethod
    def get_problems(self) -> List["Problem"]:
        pass

    @abstractmethod
    def get_all_invites(self) -> List["Invite"]:
        pass

    @abstractmethod
    def new_problem(self) -> "AbstractProblem":
        pass

    @abstractmethod
    def new_sheet(self) -> "AbstractSheet":
        pass

    @abstractmethod
    def new_contest(self) -> "AbstractContest":
        pass
