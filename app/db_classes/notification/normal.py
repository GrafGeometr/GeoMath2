from app.imports import *

from app.db_classes.standard_model.normal import StandardModel


class Notification(StandardModel):
    # --> INITIALIZE
    __tablename__ = "notification"

    head = db.Column(db.String)
    content = db.Column(db.String)
    url = db.Column(db.String)
    date = db.Column(db.DateTime)
    read = db.Column(db.Boolean, default=False)

    # --> RELATIONS
    user_id = db.Column(db.Integer, db.ForeignKey("user.id_"))

    # --> FUNCTIONS
    def add(self):
        db.session.add(self)
        db.session.commit()
        self.date = current_time()
        db.session.commit()

    def is_read(self):
        return int(self.read)

    def get_date_as_str(self):
        return str_from_dt(self.date)

    @staticmethod
    def send_to_user(head, content, url, user=current_user):
        from app.dbc import Notification

        Notification(head=head, content=content, url=url, user_id=user.id).add()
        return

    @staticmethod
    def send_to_users(head, content, url, users=[]):
        from app.dbc import Notification

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
        db.session.commit()
        return
