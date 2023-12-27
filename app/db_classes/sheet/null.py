from app.imports import *
from app.sqlalchemy_custom_types import *

from typing import List

from app.db_classes.model_with_name.null import NullModelWithName
from app.db_classes.sheet.abstract import AbstractSheet


class NullSheet(AbstractSheet, NullModelWithName):
    # --> INITIALIZE
    __abstract__ = True

    # --> RELATIONS

    # --> PROPERTIES
    @property
    def text(self) -> str:
        return ""

    @text.setter
    def text(self, text: str):
        pass

    @property
    def is_public(self) -> bool:
        return False

    @is_public.setter
    def is_public(self, is_public: bool):
        pass

    @property
    def total_likes(self) -> int:
        return 0

    @total_likes.setter
    def total_likes(self, total_likes: int):
        pass

    @property
    def total_dislikes(self) -> int:
        return 0

    @total_dislikes.setter
    def total_dislikes(self, total_dislikes: int):
        pass

    @property
    def pool_id(self) -> int:
        return -1

    @pool_id.setter
    def pool_id(self, pool_id: int):
        pass

    @property
    def pool(self) -> "AbstractPool":
        from app.db_classes.pool.null import NullPool

        return NullPool()

    @pool.setter
    def pool(self, pool: "AbstractPool"):
        pass

    # --> METHODS

    def is_liked_by(self, user: "User") -> bool:
        return False

    def act_add_like(self, user: "User") -> "AbstractSheet":
        pass

    def act_remove_like(self, user: "User") -> "AbstractSheet":
        pass

    def get_all_likes(self) -> List["Like"]:
        return []

    def get_all_good_likes(self) -> List["Like"]:
        return []

    def get_all_bad_likes(self) -> List["Like"]:
        return []

    def get_attachments(self) -> List["Attachment"]:
        return []

    def is_text_available(self) -> bool:
        return False

    def is_tags_available(self) -> bool:
        return False

    def is_my(self) -> bool:
        return False

    def get_nonsecret_attachments(self) -> List["Attachment"]:
        return []

    def get_tags(self) -> List["Tag"]:
        return []

    def get_tag_names(self) -> List[str]:
        return []

    def has_tag(self, tag: "Tag") -> bool:
        return False

    def act_add_tag(self, tag: "Tag") -> "AbstractSheet":
        pass

    def act_add_tag_by_name(self, tag_name: str) -> "AbstractSheet":
        pass

    def act_remove_tag(self, tag: "Tag") -> "AbstractSheet":
        pass

    def act_remove_tag_by_name(self, tag_name: str) -> "AbstractSheet":
        pass

    def act_set_tags(self, tags: List["Tag"]) -> "AbstractSheet":
        pass

    def has_attachment(self, attachment: "Attachment") -> bool:
        return False

    def act_add_attachment(self, attachment: "Attachment") -> "AbstractSheet":
        pass

    def act_add_attachment_by_db_filename(self, db_filename: str) -> "AbstractSheet":
        pass

    def act_remove_attachment(self, attachment: "Attachment") -> "AbstractSheet":
        pass

    def act_remove_attachment_by_db_filename(self, db_filename: str) -> "AbstractSheet":
        pass

    def act_set_attachments(self, attachments: List["Attachment"]) -> "AbstractSheet":
        pass

    def get_similar_sheets_link(self) -> str:
        return ""  # TODO : decide what link to return
