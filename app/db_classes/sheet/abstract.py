from app.imports import *
from app.sqlalchemy_custom_types import *

from typing import List

from abc import abstractmethod
from app.dbc import AbstractModelWithName


class AbstractSheet(AbstractModelWithName):
    # --> INITIALIZE
    __abstract__ = True

    # --> RELATIONS

    # --> PROPERTIES
    @property
    @abstractmethod
    def text(self) -> str:
        pass

    @text.setter
    @abstractmethod
    def text(self, text: str):
        pass

    @property
    @abstractmethod
    def is_public(self) -> bool:
        pass

    @is_public.setter
    @abstractmethod
    def is_public(self, is_public: bool):
        pass

    @property
    @abstractmethod
    def total_likes(self) -> int:
        pass

    @property
    @abstractmethod
    def total_dislikes(self) -> int:
        pass

    @property
    @abstractmethod
    def pool_id(self) -> int:
        pass

    @pool_id.setter
    @abstractmethod
    def pool_id(self, pool_id: int):
        pass

    @property
    @abstractmethod
    def pool(self) -> "AbstractPool":
        pass

    @pool.setter
    def pool(self, pool: "AbstractPool"):
        pass

    # --> METHODS
    @abstractmethod
    def is_liked_by(self, user: "User") -> bool:
        pass

    @abstractmethod
    def act_add_like(self, user: "User") -> "AbstractSheet":
        pass

    @abstractmethod
    def act_remove_like(self, user: "User") -> "AbstractSheet":
        pass

    @abstractmethod
    def get_all_likes(self) -> List["Like"]:
        pass

    @abstractmethod
    def get_all_good_likes(self) -> List["Like"]:
        pass

    @abstractmethod
    def get_all_bad_likes(self) -> List["Like"]:
        pass

    @abstractmethod
    def get_attachments(self) -> List["Attachment"]:
        pass

    @abstractmethod
    def is_text_available(self) -> bool:
        pass

    @abstractmethod
    def is_tags_available(self) -> bool:
        pass

    @abstractmethod
    def is_my(self) -> bool:
        pass

    @abstractmethod
    def get_nonsecret_attachments(self) -> List["Attachment"]:
        pass

    @abstractmethod
    def get_tags(self) -> List["Tag"]:
        pass

    @abstractmethod
    def get_tag_names(self) -> List[str]:
        pass

    @abstractmethod
    def is_have_tag(self, tag: "Tag") -> bool:
        pass

    @abstractmethod
    def act_add_tag(self, tag: "Tag") -> "AbstractSheet":
        pass

    @abstractmethod
    def act_add_tag_by_name(self, tag_name: str) -> "AbstractSheet":
        pass

    @abstractmethod
    def act_remove_tag(self, tag: "Tag") -> "AbstractSheet":
        pass

    @abstractmethod
    def act_remove_tag_by_name(self, tag_name: str) -> "AbstractSheet":
        pass

    @abstractmethod
    def act_set_tags(self, tags: List["Tag"]) -> "AbstractSheet":
        pass

    @abstractmethod
    def is_attachment(self, attachment: "Attachment") -> bool:
        pass

    @abstractmethod
    def act_add_attachment(self, attachment: "Attachment") -> "AbstractSheet":
        pass

    @abstractmethod
    def act_add_attachment_by_db_filename(self, db_filename: str) -> "AbstractSheet":
        pass

    @abstractmethod
    def act_remove_attachment(self, attachment: "Attachment") -> "AbstractSheet":
        pass

    @abstractmethod
    def act_remove_attachment_by_db_filename(self, db_filename: str) -> "AbstractSheet":
        pass

    @abstractmethod
    def act_set_attachments(self, attachments: List["Attachment"]) -> "AbstractSheet":
        pass

    @abstractmethod
    def get_similar_sheets_link(self) -> str:
        pass
