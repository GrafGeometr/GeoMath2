from abc import abstractmethod
from app.db_classes.model_with_name.abstract import AbstractModelWithName


class AbstractUser(AbstractModelWithName):
    # --> INITIALIZE
    __abstract__ = True

    # --> PROPERTIES
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

    @emails.setter
    @abstractmethod
    def emails(self, emails: list["Email"]):
        pass

    @property
    @abstractmethod
    def user_pools(self) -> list["User_Pool"]:
        pass

    @user_pools.setter
    @abstractmethod
    def user_pools(self, user_pools: list["User_Pool"]):
        pass

    @property
    @abstractmethod
    def contest_judges(self) -> list["Contest_Judge"]:
        pass

    @contest_judges.setter
    @abstractmethod
    def contest_judges(self, contest_judges: list["Contest_Judge"]):
        pass

    @property
    @abstractmethod
    def contest_users(self) -> list["Contest_User"]:
        pass

    @contest_users.setter
    @abstractmethod
    def contest_users(self, contest_users: list["Contest_User"]):
        pass

    @property
    @abstractmethod
    def likes(self) -> list["Like"]:
        pass

    @likes.setter
    @abstractmethod
    def likes(self, likes: list["Like"]):
        pass

    @property
    @abstractmethod
    def notifications(self) -> list["Notification"]:
        pass

    @notifications.setter
    @abstractmethod
    def notifications(self, notifications: list["Notification"]):
        pass

    @property
    @abstractmethod
    def user_chats(self) -> list["User_Chat"]:
        pass

    @user_chats.setter
    @abstractmethod
    def user_chats(self, user_chats: list["User_Chat"]):
        pass

    @property
    @abstractmethod
    def user_clubs(self) -> list["User_Club"]:
        pass

    @user_clubs.setter
    @abstractmethod
    def user_clubs(self, user_clubs: list["User_Club"]):
        pass

    @property
    @abstractmethod
    def user_messages(self) -> list["User_Message"]:
        pass

    @user_messages.setter
    @abstractmethod
    def user_messages(self, user_messages: list["User_Message"]):
        pass

    # --> RELATIONS

    # --> METHODS
    @classmethod
    @abstractmethod
    def get_current_user(cls) -> "AbstractUser":
        pass

    @abstractmethod
    def set_password(self, password: str) -> "AbstractUser":
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

    @classmethod
    @abstractmethod
    def get_by_verified_email(cls, email: "Email") -> "AbstractUser":
        pass
