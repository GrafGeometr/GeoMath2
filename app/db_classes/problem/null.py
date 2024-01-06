from typing import List

from app.imports import *


from app.db_classes.model_with_hashed_id.null import NullModelWithHashedId
from app.db_classes.problem.abstract import AbstractProblem


class NullProblem(NullModelWithHashedId, AbstractProblem):
    # --> INITIALIZE
    __abstract__ = True

    # --> RELATIONS

    # --> PROPERTIES
    @property
    def name(self):
        return ""

    @property
    def tags(self) -> List["Tag"]:
        return []

    @property
    def statement(self) -> str:
        return ""

    @statement.setter
    def statement(self, statement: str):
        pass

    @property
    def solution(self) -> str:
        return ""

    @solution.setter
    def solution(self, solution: str):
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

    def is_liked(self) -> bool:
        return False

    def act_add_like(self) -> "AbstractProblem":
        pass

    def act_remove_like(self) -> "AbstractProblem":
        pass

    def is_archived(self) -> bool:
        return False

    def get_all_contests(self) -> List["Contest"]:
        return []

    def get_all_likes(self) -> List["Like"]:
        return []

    def get_all_good_likes(self) -> List["Like"]:
        return []

    def get_all_bad_likes(self) -> List["Like"]:
        return []

    def is_statement_available(self, user=current_user) -> bool:
        return False

    def is_solution_available(self, user=current_user) -> bool:
        return False

    def is_tags_available(self, user=current_user) -> bool:
        return False

    def is_my(self, user=current_user) -> bool:
        return False

    def is_in_contest(self, contest) -> bool:
        return False

    # TAGS BLOCK

    def get_nonsorted_tags(self) -> List["Tag"]:
        return []

    def get_tags(self) -> List["Tag"]:
        return []

    def get_tag_names(self) -> List[str]:
        return []

    def has_tag(self, tag: "AbstractTag") -> bool:
        return False

    def act_add_tags(self, tags: List["Tag"]) -> "AbstractProblem":
        pass

    def act_add_tag(self, tag: "AbstractTag") -> "AbstractProblem":
        pass

    def act_add_tag_by_name(self, tag_name: str) -> "AbstractProblem":
        pass

    def act_remove_tag(self, tag: "AbstractTag") -> "AbstractProblem":
        pass

    def act_remove_tag_by_name(self, tag_name: str) -> "AbstractProblem":
        pass

    def act_set_tags(self, names: List[str]) -> "AbstractProblem":
        pass

    # ATTACHMENTS BLOCK

    def get_attachments(self) -> List["Attachment"]:
        return []

    def get_nonsecret_attachments(self) -> List["Attachment"]:
        return []

    def has_attachment(self, attachment: "AbstractAttachment") -> bool:
        return False

    def act_add_attachment(self, attachment: "AbstractAttachment") -> "AbstractProblem":
        pass

    def act_add_attachment_by_db_filename(self, db_filename: str) -> "AbstractProblem":
        pass

    def act_remove_attachment(
        self, attachment: "AbstractAttachment"
    ) -> "AbstractProblem":
        pass

    def act_remove_attachment_by_db_filename(
        self, db_filename: str
    ) -> "AbstractProblem":
        pass

    def act_set_attachments(self, names: List[str]) -> "AbstractProblem":
        pass

    def get_similar_problems_link(self) -> str:
        return ""  # TODO : decide what link to return
