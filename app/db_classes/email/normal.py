from app.imports import *

from app.db_classes.standard_model.normal import StandardModel
from .abstract import AbstractEmail
from .null import NullEmail
from .getter import EmailGetter


class Email(StandardModel, AbstractEmail):
    # --> INITIALIZE
    __abstract__ = False
    __tablename__ = "email"

    name_ = db.Column(db.String)
    created_date_ = db.Column(db.DateTime, default=current_time)
    verified_ = db.Column(db.Boolean, default=False)
    token_ = db.Column(db.String, nullable=True)

    null_cls_ = NullEmail
    getter_cls_ = EmailGetter

    # --> RELATIONS
    user_id_ = db.Column(db.Integer, db.ForeignKey("user.id_"))

    # --> PROPERTIES
    @property
    def name(self):
        return self.name_

    @name.setter
    def name(self, value):
        self.name_ = value
        self.save()

    @property
    def created_date(self):
        return self.created_date_

    @created_date.setter
    def created_date(self, created_date):
        self.created_date_ = created_date
        self.save()

    @property
    def verified(self):
        return self.verified_

    @verified.setter
    def verified(self, verified):
        self.verified_ = verified
        self.save()

    @property
    def token(self):
        return self.token_

    @token.setter
    def token(self, token):
        self.token_ = token
        self.save()

    @property
    def user_id(self):
        return self.user_id_

    @user_id.setter
    def user_id(self, user_id):
        self.user_id_ = user_id
        self.save()

    @property
    def user(self):
        return self.user_

    @user.setter
    def user(self, user):
        self.user_ = user
        self.save()
