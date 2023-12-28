from app.imports import *

from app.db_classes.standard_model.null import NullStandardModel
from app.db_classes.notification.abstract import AbstractNotification


class NullNotification(NullStandardModel, AbstractNotification):
    # --> INITIALIZE
    __abstract__ = True

    # --> RELATIONS

    # --> PROPERTIES
    @property
    def head(self) -> str:
        return ""

    @head.setter
    def head(self, value: str):
        pass

    @property
    def content(self) -> str:
        return ""

    @content.setter
    def content(self, value: str):
        pass

    @property
    def url(self) -> str:
        return ""

    @url.setter
    def url(self, value: str):
        pass

    @property
    def date(self):
        return datetime.datetime.min

    @date.setter
    def date(self, value):
        pass

    @property
    def read(self) -> bool:
        return True

    @read.setter
    def read(self, value: bool):
        pass

    # --> METHODS

    def get_date_as_str(self) -> str:
        pass

    @staticmethod
    def send_to_user(head, content, url, user=current_user):
        pass

    @staticmethod
    def send_to_users(head, content, url, users=[]):
        pass

    @staticmethod
    def send_to_friends(head, content, url, user=current_user):
        pass

    @staticmethod
    def mark_all_as_read(user=current_user):
        pass
