from typing import List

from app.imports import *

from abc import abstractmethod
from app.db_classes.model_with_hashed_id.abstract import AbstractModelWithHashedId


class AbstractProblem(AbstractModelWithHashedId):
    # --> INITIALIZE
    __abstract__ = True

    # --> RELATIONS

    # --> PROPERTIES
    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @name.setter
    @abstractmethod
    def name(self, name: str):
        pass

    @property
    @abstractmethod
    def tags(self) -> List["Tag"]:
        pass

    @property
    @abstractmethod
    def statement(self) -> str:
        pass

    @statement.setter
    @abstractmethod
    def statement(self, statement: str):
        pass

    @property
    @abstractmethod
    def solution(self) -> str:
        pass

    @solution.setter
    @abstractmethod
    def solution(self, solution: str):
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

    @total_likes.setter
    @abstractmethod
    def total_likes(self, total_likes: int):
        pass

    @property
    @abstractmethod
    def total_dislikes(self) -> int:
        pass

    @total_dislikes.setter
    @abstractmethod
    def total_dislikes(self, total_dislikes: int):
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
    @abstractmethod
    def pool(self, pool: "AbstractPool"):
        pass

    # --> METHODS

    @abstractmethod
    def is_liked(self) -> bool:
        pass

    @abstractmethod
    def act_add_like(self) -> "AbstractProblem":
        pass

    @abstractmethod
    def act_remove_like(self) -> "AbstractProblem":
        pass

    @abstractmethod
    def is_archived(self) -> bool:
        pass

    @abstractmethod
    def get_all_contests(self) -> List["Contest"]:
        pass

    @abstractmethod
    def get_all_likes(self) -> List["Like"]:
        pass

    @abstractmethod
    def get_all_good_likes(self) -> List["Like"]:
        pass

    def get_all_bad_likes(self) -> List["Like"]:
        pass

    @abstractmethod
    def is_statement_available(self, user=current_user) -> bool:
        pass

    @abstractmethod
    def is_solution_available(self, user=current_user) -> bool:
        pass

    @abstractmethod
    def is_tags_available(self, user=current_user) -> bool:
        pass

    @abstractmethod
    def is_my(self, user=current_user) -> bool:
        pass

    @abstractmethod
    def is_in_contest(self, contest) -> bool:
        pass

    # TAGS BLOCK

    @abstractmethod
    def get_nonsorted_tags(self) -> List["Tag"]:
        pass

    @abstractmethod
    def get_tags(self) -> List["Tag"]:
        pass

    @abstractmethod
    def get_tag_names(self) -> List[str]:
        pass

    @abstractmethod
    def has_tag(self, tag: "AbstractTag") -> bool:
        pass

    @abstractmethod
    def act_add_tags(self, tags: List["Tag"]) -> "AbstractProblem":
        pass

    @abstractmethod
    def act_add_tag(self, tag: "AbstractTag") -> "AbstractProblem":
        pass

    @abstractmethod
    def act_add_tag_by_name(self, tag_name: str) -> "AbstractProblem":
        pass

    @abstractmethod
    def act_remove_tag(self, tag: "AbstractTag") -> "AbstractProblem":
        pass

    @abstractmethod
    def act_remove_tag_by_name(self, tag_name: str) -> "AbstractProblem":
        pass

    @abstractmethod
    def act_set_tags(self, names: List[str]) -> "AbstractProblem":
        pass

    # ATTACHMENTS BLOCK

    @abstractmethod
    def get_attachments(self) -> List["Attachment"]:
        pass

    @abstractmethod
    def get_nonsecret_attachments(self) -> List["Attachment"]:
        pass

    @abstractmethod
    def has_attachment(self, attachment: "AbstractAttachment") -> bool:
        pass

    @abstractmethod
    def act_add_attachment(self, attachment: "AbstractAttachment") -> "AbstractProblem":
        pass

    @abstractmethod
    def act_add_attachment_by_db_filename(self, db_filename: str) -> "AbstractProblem":
        pass

    @abstractmethod
    def act_remove_attachment(
        self, attachment: "AbstractAttachment"
    ) -> "AbstractProblem":
        pass

    @abstractmethod
    def act_remove_attachment_by_db_filename(
        self, db_filename: str
    ) -> "AbstractProblem":
        pass

    @abstractmethod
    def act_set_attachments(self, names: List[str]) -> "AbstractProblem":
        pass

    @abstractmethod
    def get_similar_problems_link(self) -> str:
        pass
