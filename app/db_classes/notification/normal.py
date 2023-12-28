from app.imports import *

from app.db_classes.standard_model.normal import StandardModel
from app.db_classes.notification.abstract import AbstractNotification
from app.db_classes.notification.null import NullNotification
from app.db_classes.notification.getter import NotificationGetter


class Notification(StandardModel, AbstractNotification):
    # --> INITIALIZE
    __abstract__ = False
    __tablename__ = "notification"

    head_ = db.Column(db.String)
    content_ = db.Column(db.String)
    url_ = db.Column(db.String)
    date_ = db.Column(db.DateTime)
    read_ = db.Column(db.Boolean, default=False)

    null_cls_ = NullNotification
    getter_cls_ = NotificationGetter

    # --> RELATIONS
    user_id_ = db.Column(db.Integer, db.ForeignKey("user.id_"))

    # --> PROPERTIES
    @property
    def head(self):
        return self.head_

    @head.setter
    def head(self, value):
        self.head_ = value
        self.save()

    @property
    def content(self):
        return self.content_

    @content.setter
    def content(self, value):
        self.content_ = value
        self.save()

    @property
    def url(self):
        return self.url_

    @url.setter
    def url(self, value):
        self.url_ = value
        self.save()

    @property
    def date(self):
        return self.date_

    @date.setter
    def date(self, value):
        self.date_ = value
        self.save()

    @property
    def read(self):
        return self.read_

    @read.setter
    def read(self, value):
        self.read_ = value
        self.save()

    # --> METHODS
    def add(self):
        db.session.add(self)
        self.date = current_time()
        return self

    def get_date_as_str(self):
        return str_from_dt(self.date)

    @staticmethod
    def send_to_user(head, content, url, user=current_user):
        Notification(head_=head, content_=content, url_=url, user_id_=user.id).add()
        return

    @staticmethod
    def send_to_users(head, content, url, users=[]):
        for user in users:
            Notification.send_to_user(head=head, content=content, url=url, user=user)
        return

    @staticmethod
    def send_to_friends(head, content, url, user=current_user):
        friends = user.get_friends()
        Notification.send_to_users(head=head, content=content, url=url, users=friends)

    @staticmethod
    def mark_all_as_read(user=current_user):
        notifications = user.notifications
        for notification in notifications:
            notification.read = True
        return
