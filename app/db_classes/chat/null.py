from typing import List

from app.db_classes.model_with_name.null import NullModelWithName
from .abstract import AbstractChat
from app.imports import *


class NullChat(NullModelWithName, AbstractChat):
    # --> INITIALIZE
    __abstract__ = True

    # --> PROPERTIES
    @property
    def readonly(self) -> bool:
        return True

    @property
    def user_chats(self) -> list["UserChat"]:
        return []

    @property
    def club_id(self):
        return -1

    @property
    def club(self) -> "AbstractClub":
        from app.db_classes.club.null import NullClub

        return NullClub()

    # --> METHODS
    def contains_user(self, user=current_user) -> bool:
        return False

    def all_messages(self) -> List["Message"]:
        return []

    def unread_messages(self, user=current_user) -> List["Message"]:
        return []

    def last_message_date(self) -> datetime.datetime:
        return datetime.datetime.min

    def other_user(self, user=current_user) -> "AbstractUser":
        from app.db_classes.user.null import NullUser

        return NullUser()

    def count_owners(self) -> int:
        return 0

    def count_participants(self) -> int:
        return 0

    def add_user(self, user=current_user) -> "AbstractChat":
        return self

    def remove_user(self, user=current_user) -> "AbstractChat":
        return self

    def is_my(self) -> bool:
        return False

    def act_refresh_chat_invites(self) -> "AbstractChat":
        return self

    def act_generate_new_invite_code(self) -> "AbstractChat":
        return self

    def act_mark_all_as_read(self, user=current_user) -> "AbstractChat":
        return self
