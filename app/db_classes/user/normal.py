from app.imports import *
from app.sqlalchemy_custom_types import *

from app.db_classes.model_with_name.normal import ModelWithName
from app.db_classes.user.abstract import AbstractUser
from app.db_classes.user.null import NullUser


class User(UserMixin, ModelWithName, AbstractUser):
    # --> INITIALIZE
    __abstract__ = False
    __tablename__ = "user"

    password_ = db.Column(db.String, nullable=True)
    admin_ = db.Column(db.Boolean, default=False)
    created_date_ = db.Column(db.DateTime, default=current_time)
    profile_pic_ = db.Column(db.String(), nullable=True)
    about_ = db.Column(db.String(), nullable=True, default="")

    null_cls = NullUser

    # --> RELATIONS
    emails_ = db.relationship("Email", backref="user")
    user_pools_ = db.relationship("UserToPoolRelation", backref="user")
    contest_judges_ = db.relationship("ContestToJudgeRelation", backref="user")
    contest_users_ = db.relationship("Contest_User", backref="user")
    likes_ = db.relationship("Like", backref="user")
    notifications_ = db.relationship("Notification", backref="user")
    user_chats_ = db.relationship("UserToChatRelation", backref="user")
    user_clubs_ = db.relationship("UserToClubRelation", backref="user")
    user_messages_ = db.relationship("User_Message", backref="user")

    # --> PROPERTIES
    getter_singleton_ = None

    @classmethod
    @property
    def get(cls):
        if cls.getter_singleton_ is None:
            from .getter import Getter
            getter_singleton_ = Getter(User)
        return cls.getter_singleton_

    @property
    def password(self):
        return self.password_

    @password.setter
    def password(self, password):
        self.password_ = password
        self.save()

    @property
    def admin(self):
        return self.admin_

    @admin.setter
    def admin(self, admin):
        self.admin_ = admin
        self.save()

    @property
    def created_date(self):
        return self.created_date_

    @created_date.setter
    def created_date(self, created_date):
        self.created_date_ = created_date
        self.save()

    @property
    def profile_pic(self):
        return self.profile_pic_

    @profile_pic.setter
    def profile_pic(self, profile_pic):
        self.profile_pic_ = profile_pic
        self.save()

    @property
    def about(self):
        return self.about_

    @about.setter
    def about(self, about):
        self.about_ = about
        self.save()

    @property
    def emails(self):
        return self.emails_

    @emails.setter
    def emails(self, emails):
        self.emails_ = emails
        self.save()

    @property
    def user_pools(self):
        return self.user_pools_

    @user_pools.setter
    def user_pools(self, user_pools):
        self.user_pools_ = user_pools
        self.save()

    @property
    def contest_judges(self):
        return self.contest_judges_

    @contest_judges.setter
    def contest_judges(self, contest_judges):
        self.contest_judges_ = contest_judges
        self.save()

    @property
    def contest_users(self):
        return self.contest_users_

    @contest_users.setter
    def contest_users(self, contest_users):
        self.contest_users_ = contest_users
        self.save()

    @property
    def likes(self):
        return self.likes_

    @likes.setter
    def likes(self, likes):
        self.likes_ = likes
        self.save()

    @property
    def notifications(self):
        return self.notifications_

    @notifications.setter
    def notifications(self, notifications):
        self.notifications_ = notifications
        self.save()

    @property
    def user_chats(self):
        return self.user_chats_

    @user_chats.setter
    def user_chats(self, user_chats):
        self.user_chats_ = user_chats
        self.save()

    @property
    def user_clubs(self):
        return self.user_clubs_

    @user_clubs.setter
    def user_clubs(self, user_clubs):
        self.user_clubs_ = user_clubs
        self.save()

    @property
    def user_messages(self):
        return self.user_messages_

    @user_messages.setter
    def user_messages(self, user_messages):
        self.user_messages_ = user_messages
        self.save()

    # --> METHODS
    @classmethod
    def get_current_user(cls):
        if current_user.is_authenticated:
            return current_user
        return cls.null_cls()

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def get_user_pools(self):
        from app.dbc import UserToPoolRelation

        return UserToPoolRelation.query.filter_by(user_id_=self.id).all()

    def create_new_pool(self, name):
        from app.dbc import Pool, UserToPoolRelation

        pool = Pool(name=name).add()

        UserToPoolRelation(
            user_id=self.id,
            pool_id=pool.id,
            role=Owner,
            invited_date=current_time(),
            joined_date=current_time(),
        ).add()

        return pool

    def get_pool_relation(self, pool_id):
        from app.dbc import UserToPoolRelation

        return UserToPoolRelation.query.filter_by(user_id_=self.id, pool_id_=pool_id).first()

    def is_chat_owner(self, chat):
        from app.dbc import UserToChatRelation

        uc = UserToChatRelation.query.filter_by(user_id_=self.id, chat_id_=chat.id).first()
        return uc.is_owner()

    def is_chat_participant(self, chat):
        from app.dbc import UserToChatRelation

        uc = UserToChatRelation.query.filter_by(user_id_=self.id, chat_id_=chat.id).first()
        return uc.is_participant()

    def get_chats(self):
        from app.dbc import UserToChatRelation

        chats = [uc.chat for uc in UserToChatRelation.query.filter_by(user_id_=self.id).all()]
        return chats

    def get_nonclub_chats(self):
        return [chat for chat in self.get_chats() if chat.club_id is None]

    def get_club_relation(self, club_id):
        from app.dbc import UserToClubRelation

        return UserToClubRelation.query.filter_by(user_id_=self.id, club_id_=club_id).first()

    def get_friends_from(self):
        from app.dbc import Friend

        friends = Friend.query.filter_by(friend_from_=self.id, accepted_=False).all()
        return [User.query.filter_by(id_=f.friend_to).first() for f in friends]

    def get_friends_to(self):
        from app.dbc import Friend

        friends = Friend.query.filter_by(friend_to_=self.id, accepted_=False).all()
        return [User.query.filter_by(id_=f.friend_from).first() for f in friends]

    def get_friends(self):
        from app.dbc import Friend, User

        res = []
        for f in Friend.query.filter_by(accepted_=True).all():
            if f.friend_from == self.id:
                res.append(User.query.filter_by(id_=f.friend_to).first())
            elif f.friend_to == self.id:
                res.append(User.query.filter_by(id_=f.friend_from).first())
        return res

    def is_has_unread_notifications(self):
        for notification in self.notifications:
            if not notification.read:
                return True
        return False

    def get_notifications(self):
        from app.dbc import Notification

        return sorted(
            Notification.query.filter_by(user_id_=self.id).all(),
            key=lambda n: n.date,
            reverse=True,
        )

    def is_pool_access(self, pool_id):
        from app.dbc import UserToPoolRelation

        relation = UserToPoolRelation.query.filter_by(user_id_=self.id, pool_id_=pool_id).first()
        return relation.role.is_owner() or relation.role.is_invited()

    def is_judge(self, contest):
        from app.dbc import ContestToJudgeRelation

        return not ContestToJudgeRelation.query.filter_by(
            user_id_=self.id, contest_id_=contest.id
        ).first().is_null()

    @classmethod
    def get_by_verified_email(cls, email):
        from app.dbc import Email

        users = [
            email.user
            for email in Email.query.filter_by(verified_=True, name_=email).all()
        ]
        if users:
            return users[0]
        else:
            return cls.null_cls()