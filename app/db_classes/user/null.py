from app.db_classes.standard_model.null import NullStandardModel
from app.db_classes.user.abstract import AbstractUser
from app.db_classes.user_to_club_relation.null import NullUserToClubRelation
from app.db_classes.user_to_pool_relation.null import NullUserToPoolRelation
from app.db_classes.pool.null import NullPool


class NullUser(NullStandardModel, AbstractUser):
    # --> INITIALIZE
    __abstract__ = True

    # --> PROPERTIES
    @property
    def name(self):
        return ""

    @property
    def password(self):
        return ""

    @property
    def admin(self):
        return False

    @property
    def created_date(self):
        return ""

    @property
    def profile_pic(self):
        return ""

    @property
    def about(self):
        return ""

    @property
    def emails(self):
        return []

    @property
    def user_pools(self):
        return []

    @property
    def contest_judges(self):
        return []

    @property
    def contest_users(self):
        return []

    @property
    def likes(self):
        return []

    @property
    def notifications(self):
        return []

    @property
    def user_chats(self):
        return []

    @property
    def user_clubs(self):
        return []

    @property
    def user_messages(self):
        return []

    # --> METHODS

    @classmethod
    def get_current_user(cls):
        return NullUser()

    def set_password_hash(self, password):
        return self

    def check_password(self, password):
        return False

    def get_user_pools(self):
        return []

    def create_new_pool(self, name):
        return NullPool()

    def get_pool_relation(self, pool_id):
        return NullUserToPoolRelation()

    def is_chat_owner(self, chat):
        return False

    def is_chat_participant(self, chat):
        return False

    def get_chats(self):
        return []

    def get_nonclub_chats(self):
        return []

    def get_club_relation(self, club_id):
        return NullUserToClubRelation()

    def get_friends_from(self):
        return []

    def get_friends_to(self):
        return []

    def get_friends(self):
        return []

    def is_pool_access(self, pool_id):
        return False

    def is_judge(self, contest):
        return False

    @staticmethod
    def get_by_verified_email(email):
        return NullUser()
