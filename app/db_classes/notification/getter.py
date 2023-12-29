from app.db_classes.standard_model.getter import StandardModelGetter


class NotificationGetter(StandardModelGetter):
    def by_user_id(self, user_id):
        self.manager.filter(self.manager.normal_cls.user_id_ == user_id)
        return self

    def by_user(self, user):
        return self.by_user_id(user.id)
