from app.imports import *

from abc import abstractmethod
from app.db_classes.standard_model.abstract import AbstractStandardModel


class AbstractNotification(AbstractStandardModel):
    # --> INITIALIZE
    __abstract__ = True

    # --> RELATIONS

    # --> PROPERTIES
    @property
    @abstractmethod
    def head(self) -> str:
        pass

    @head.setter
    @abstractmethod
    def head(self, value: str):
        pass

    @property
    @abstractmethod
    def content(self) -> str:
        pass

    @content.setter
    @abstractmethod
    def content(self, value: str):
        pass

    @property
    @abstractmethod
    def url(self) -> str:
        pass

    @url.setter
    @abstractmethod
    def url(self, value: str):
        pass

    @property
    @abstractmethod
    def date(self) -> "datetime.datetime":
        pass

    @date.setter
    @abstractmethod
    def date(self, value: "datetime.datetime"):
        pass

    @property
    @abstractmethod
    def read(self) -> bool:
        pass

    @read.setter
    @abstractmethod
    def read(self, value: bool):
        pass

    # --> METHODS

    @abstractmethod
    def get_date_as_str(self) -> str:
        pass

    @staticmethod
    @abstractmethod
    def send_to_user(head, content, url, user=current_user):
        pass

    @staticmethod
    @abstractmethod
    def send_to_users(head, content, url, users=[]):
        pass

    @staticmethod
    @abstractmethod
    def send_to_friends(head, content, url, user=current_user):
        pass

    @staticmethod
    @abstractmethod
    def mark_all_as_read(user=current_user):
        pass
