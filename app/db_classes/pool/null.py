from typing import List

from app.imports import *
from app.sqlalchemy_custom_types import *

from app.db_classes.model_with_name.null import NullModelWithName
from app.db_classes.model_with_hashed_id.null import NullModelWithHashedId
from app.db_classes.invite.null import NullInvite

from app.db_classes.pool.abstract import AbstractPool


class NullPool(NullModelWithHashedId, NullModelWithName, AbstractPool):
    # --> INITIALIZE
    __abstract__ = False

    # --> RELATIONS

    # --> PROPERTIES
    @property
    def user_to_pool_relations(self) -> List["UserToPoolRelation"]:
        return []

    @user_to_pool_relations.setter
    def user_to_pool_relations(self, value: List["UserToPoolRelation"]):
        pass

    @property
    def problems(self) -> List["Problem"]:
        return []

    @problems.setter
    def problems(self, value: List["Problem"]):
        pass

    @property
    def sheets(self) -> List["Sheet"]:
        return []

    @sheets.setter
    def sheets(self, value: List["Sheet"]):
        pass

    @property
    def contests(self) -> List["Contest"]:
        return []

    @contests.setter
    def contests(self, value: List["Contest"]):
        pass

    # --> METHODS
    def contains_user(self, user=current_user) -> bool:
        return False

    def is_my(self) -> bool:
        return False

    def check_user_access(self, current_user) -> bool:
        return False

    def check_user_owner(self, current_user) -> bool:
        return False

    def add_user(self, user=current_user, role=Participant) -> "AbstractPool":
        return self

    def remove_user(self, user=current_user) -> "AbstractPool":
        return self

    def add_user_by_invite(
        self, user=current_user, invite=NullInvite()
    ) -> "AbstractPool":
        return self

    def act_generate_new_invite_code(self) -> "AbstractInvite":
        return NullInvite()

    def get_users(self) -> List["User"]:
        return []

    def get_owners(self) -> List["User"]:
        return []

    def count_owners(self) -> int:
        return 0

    def get_participants(self) -> List["User"]:
        return []

    def count_participants(self) -> int:
        return 0

    def get_problems(self) -> List["Problem"]:
        return []

    def get_all_invites(self) -> List["Invite"]:
        return []

    def new_problem(self) -> "AbstractProblem":
        from app.db_classes.problem.null import NullProblem

        return NullProblem()

    def new_sheet(self) -> "AbstractSheet":
        from app.db_classes.sheet.null import NullSheet

        return NullSheet()

    def new_contest(self) -> "AbstractContest":
        from app.db_classes.contest.null import NullContest

        return NullContest()
