from flask_login import AnonymousUserMixin

from app.actions import *
from app.imports import *
from app.logger_classes.exception_access_denied import ExceptionAccessDenied
from app.logger_classes.exception_invalid_email import ExceptionInvalidEmail
from app.logger_classes.exception_invalid_login_characters import (
    ExceptionInvalidLoginCharacters,
)
from app.logger_classes.exception_login_already_used import ExceptionLoginAlreadyUsed
from app.logger_classes.exception_login_is_too_short import ExceptionLoginIsTooShort
from app.logger_classes.exception_password_is_too_short import (
    ExceptionPasswordIsTooShort,
)
from app.logger_classes.exception_passwords_dont_match import (
    ExceptionPasswordsDontMatch,
)
from app.logger_classes.exception_wrong_login_or_password import (
    ExceptionLoginOrPasswordWrong,
)
from app.utils_and_functions.usefull_functions import (
    email_validity_checker,
    email_token_stuff,
)


def none_safe_user(user):
    from app.db_classes.user.null import NullUser
    from app.db_classes.user.abstract import AbstractUser

    if user is None:
        return NullUser()

    if not isinstance(user, AbstractUser):
        raise Exception("User must be a subclass of AbstractUser")

    return user


class StandardUserGetAction(AbstractAction):
    def __init__(self, user=None, actor=current_user):
        self.user = none_safe_user(user)
        self.actor = actor


class StandardUserSetAction(AbstractAction):
    def __init__(self, user=None, value=None, actor=current_user):
        self.user = none_safe_user(user)
        self.value = value
        self.actor = actor


class CheckForAdmin(AbstractAction):
    user: "AbstractUser"
    actor: "AbstractUser"

    def check_possibility(self):
        if self.actor.get_admin().act(context=self):
            return
        if self.user.id == self.actor.id:
            return
        raise ExceptionAccessDenied(self.user)


# TODO : fix AnonymousUserMixin!!! (it raises an exception)
class GetId(Action, StandardUserGetAction):
    def act(self, context=None):
        super().act(context)
        return self.user.id


class SetId(ContextOnlyAction, StandardUserSetAction):
    def act(self, context=None):
        super().act(context)
        self.user.id = self.value


class GetName(Action, StandardUserGetAction):
    def act(self, context=None):
        super().act(context)
        return self.user.name


class SetName(Action, StandardUserSetAction, CheckForAdmin):
    def act(self, context=None):
        super().act(context)
        self.user.name = self.value


class GetPasswordHash(Action, StandardUserGetAction):
    def act(self, context=None):
        super().act(context)
        return self.user.password


class SetPasswordHash(ContextOnlyAction, StandardUserSetAction):
    def act(self, context=None):
        super().act(context)
        self.user.password = self.value


class GetAdmin(Action, StandardUserGetAction):
    def check_possibility(self):
        if self.actor.is_admin:
            return
        if self.user.id == self.actor.id:
            return
        raise ExceptionAccessDenied(self.user)

    def act(self, context=None):
        super().act(context)
        return self.user.is_admin


class SetAdmin(ContextOnlyAction, StandardUserSetAction):
    def act(self, context=None):
        super().act(context)
        self.user.is_admin = self.value


class GetCreatedDate(Action, StandardUserGetAction):
    def act(self, context=None):
        super().act(context)
        return self.user.created


class SetCreatedDate(ContextOnlyAction, StandardUserSetAction):
    def act(self, context=None):
        super().act(context)
        self.user.created = self.value


class GetProfilePic(Action, StandardUserGetAction):
    def act(self, context=None):
        super().act(context)
        return self.user.profile_pic


class SetProfilePic(Action, StandardUserSetAction, CheckForAdmin):
    def act(self, context=None):
        super().act(context)
        self.user.profile_pic = self.value


class GetAbout(Action, StandardUserGetAction):
    def act(self, context=None):
        super().act(context)
        return self.user.about


class SetAbout(Action, StandardUserSetAction, CheckForAdmin):
    def act(self, context=None):
        super().act(context)
        self.user.about = self.value


class GetEmails(Action, StandardUserGetAction, CheckForAdmin):
    def act(self, context=None):
        super().act(context)
        return self.user.email


class GetUserPools(Action, StandardUserGetAction, CheckForAdmin):
    def act(self, context=None):
        super().act(context)
        return self.user.user_pools


class GetContestJudges(Action, StandardUserGetAction, CheckForAdmin):
    def act(self, context=None):
        super().act(context)
        return self.user.contest_judges


class GetContestUsers(Action, StandardUserGetAction, CheckForAdmin):
    def act(self, context=None):
        super().act(context)
        return self.user.contest_users


class GetLikes(Action, StandardUserGetAction):
    def act(self, context=None):
        super().act(context)
        return self.user.likes


class GetNotifications(Action, StandardUserGetAction, CheckForAdmin):
    def act(self, context=None):
        super().act(context)
        return self.user.notifications


class GetUserChats(Action, StandardUserGetAction, CheckForAdmin):
    def act(self, context=None):
        super().act(context)
        return self.user.user_chats


class GetUserClubs(Action, StandardUserGetAction, CheckForAdmin):
    def act(self, context=None):
        super().act(context)
        return self.user.user_clubs


class GetUserMessages(Action, StandardUserGetAction, CheckForAdmin):
    def act(self, context=None):
        super().act(context)
        return self.user.user_messages


class SetMany(Action):
    def __init__(
        self,
        user=None,
        id=None,
        name=None,
        password_hash=None,
        password=None,
        admin=None,
        about=None,
        created_date=None,
        profile_pic=None,
        actor=current_user,
    ):
        self.user = none_safe_user(user)
        self.id = id
        self.name = name
        self.password_hash = password_hash
        self.password = password
        self.admin = admin
        self.about = about
        self.created_date = created_date
        self.profile_pic = profile_pic
        self.actor = actor

    def act(self, context=None):
        super().act(context)
        SetId(user=self.user, value=self.id).act(context)
        SetName(user=self.user, value=self.name).act(context)
        SetPasswordHash(user=self.user, value=self.password_hash).act(context)
        SetPassword(user=self.user, value=self.password).act(context)
        SetAdmin(user=self.user, value=self.admin).act(context)
        SetAbout(user=self.user, value=self.about).act(context)
        SetCreatedDate(user=self.user, value=self.created_date).act(context)
        SetProfilePic(user=self.user, value=self.profile_pic).act(context)


class SetPassword(ContextOnlyAction, StandardUserSetAction):
    def act(self, context=None):
        super().act(context)
        self.user.set(password_hash=generate_password_hash(self.value)).act(
            context=self
        )


class RegisterUser(Action):
    def __init__(self, login="", email_name="", password="", repeat_password=""):
        self.login = login
        self.email_name = email_name
        self.password = password
        self.repeat_password = repeat_password

    def check_possibility(self):
        from app.db_classes.user.normal import User

        if len(self.login) < 4:
            raise ExceptionLoginIsTooShort(None)
        possible_characters = string.ascii_letters + string.digits + "_-."
        if not all(c in possible_characters for c in self.login):
            raise ExceptionInvalidLoginCharacters(None)
        if self.login.lower() in [user.name.lower() for user in User.get.all()]:
            raise ExceptionLoginAlreadyUsed(None)
        if not email_validity_checker(self.email_name):
            raise ExceptionInvalidEmail(None)  # TODO : move this to email actions
        if self.password != self.repeat_password:
            raise ExceptionPasswordsDontMatch(None)
        if len(self.password) < 6:
            raise ExceptionPasswordIsTooShort(None)

    def act(self, context=None):
        super().act(context)
        from app.db_classes.user.normal import User
        from app.db_classes.email.normal import Email

        user = User()
        user.set(name=self.login).act(context=self)
        email = Email(name=self.email_name, user=user)
        email_token_stuff(email)
        user.set(password=self.password).act(context=self)
        db.session.add(user)  # TODO : replace with user.add()
        db.session.add(email)  # TODO : replace with email.add()
        db.session.commit()

        login_user(user, remember=True, duration=datetime.timedelta(days=5))
        confirm_login()

        return user


class LoginUser(Action):
    def __init__(self, login="", password=""):
        self.login = login
        self.password = password

    def check_possibility(self):
        from app.db_classes.user.normal import User

        user = User.get.by_name(self.login).first()
        if user.is_null():
            user = User.get_by_verified_email(self.login)
        if user.is_null() or not user.check_password(self.password):
            raise ExceptionLoginOrPasswordWrong(user)

    def act(self, context=None):
        super().act(context)
        from app.db_classes.user.normal import User

        user = User.get.by_name(self.login).first()
        login_user(user, remember=True, duration=datetime.timedelta(days=5))
        confirm_login()
        return user
