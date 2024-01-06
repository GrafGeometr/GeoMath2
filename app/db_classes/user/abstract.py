from abc import abstractmethod
from app.db_classes.standard_model.abstract import AbstractStandardModel

from .actions import *


class AbstractUser(AbstractStandardModel):
    # --> INITIALIZE
    __abstract__ = True

    # --> ACTIONS
    def get_id(self):
        return GetId(self)

    def get_name(self):
        return GetName(self)

    def get_password_hash(self):
        return GetPasswordHash(self)

    def get_admin(self):
        return GetAdmin(self)

    def get_created_date(self):
        return GetCreatedDate(self)

    def get_profile_pic(self):
        return GetProfilePic(self)

    def get_about(self):
        return GetAbout(self)

    def get_emails(self):
        return GetEmails(self)

    def get_user_pools(self):
        return GetUserPools(self)

    def get_contest_judges(self):
        return GetContestJudges(self)

    def get_contest_users(self):
        return GetContestUsers(self)

    def get_likes(self):
        return GetLikes(self)

    def get_notifications(self):
        return GetNotifications(self)

    def get_user_chats(self):
        return GetUserChats(self)

    def set(self, **kwargs):
        return SetMany(self, **kwargs)

    @staticmethod
    def register(login="", email_name="", password="", repeat_password=""):
        return RegisterUser(login, email_name, password, repeat_password)

    @staticmethod
    def login(login="", password=""):
        return LoginUser(login, password)

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
    def password(self) -> str:
        pass

    @password.setter
    @abstractmethod
    def password(self, password: str):
        pass

    @property
    @abstractmethod
    def admin(self) -> bool:
        pass

    @admin.setter
    @abstractmethod
    def admin(self, admin: bool):
        pass

    @property
    @abstractmethod
    def created_date(self) -> str:
        pass

    @created_date.setter
    @abstractmethod
    def created_date(self, created_date: str):
        pass

    @property
    @abstractmethod
    def profile_pic(self) -> str:
        pass

    @profile_pic.setter
    @abstractmethod
    def profile_pic(self, profile_pic: str):
        pass

    @property
    @abstractmethod
    def about(self) -> str:
        pass

    @about.setter
    @abstractmethod
    def about(self, about: str):
        pass

    @property
    @abstractmethod
    def emails(self) -> list["Email"]:
        pass

    @property
    @abstractmethod
    def user_pools(self) -> list["User_Pool"]:
        pass

    @property
    @abstractmethod
    def contest_judges(self) -> list["Contest_Judge"]:
        pass

    @property
    @abstractmethod
    def contest_users(self) -> list["Contest_User"]:
        pass

    @property
    @abstractmethod
    def likes(self) -> list["Like"]:
        pass

    @property
    @abstractmethod
    def notifications(self) -> list["Notification"]:
        pass

    @property
    @abstractmethod
    def user_chats(self) -> list["User_Chat"]:
        pass

    @property
    @abstractmethod
    def user_clubs(self) -> list["User_Club"]:
        pass

    @property
    @abstractmethod
    def user_messages(self) -> list["User_Message"]:
        pass

    # --> RELATIONS

    # --> METHODS
    @classmethod
    @abstractmethod
    def get_current_user(cls) -> "AbstractUser":
        pass

    @abstractmethod
    def check_password(self, password: str) -> bool:
        pass

    @abstractmethod
    def get_user_pools(self) -> list["User_Pool"]:
        pass

    @abstractmethod
    def create_new_pool(self, name: str) -> "Pool":
        pass

    @abstractmethod
    def get_pool_relation(self, pool_id: int) -> "User_Pool":
        pass

    @abstractmethod
    def is_chat_owner(self, chat: "Chat") -> bool:
        pass

    @abstractmethod
    def is_chat_participant(self, chat: "Chat") -> bool:
        pass

    @abstractmethod
    def get_chats(self) -> list["Chat"]:
        pass

    @abstractmethod
    def get_nonclub_chats(self) -> list["Chat"]:
        pass

    @abstractmethod
    def get_club_relation(self, club_id: int) -> "User_Club":
        pass

    @abstractmethod
    def get_friends_from(self) -> list["User"]:
        pass

    @abstractmethod
    def get_friends_to(self) -> list["User"]:
        pass

    @abstractmethod
    def get_friends(self) -> list["User"]:
        pass

    @abstractmethod
    def is_pool_access(self, pool_id: int) -> bool:
        pass

    @abstractmethod
    def is_judge(self, contest: "Contest") -> bool:
        pass

    @staticmethod
    @abstractmethod
    def get_by_verified_email(email) -> "AbstractUser":
        pass
