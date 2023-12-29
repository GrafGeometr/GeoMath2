from app.db_classes.model_with_name.null import NullModelWithName
from .abstract import AbstractChat


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
