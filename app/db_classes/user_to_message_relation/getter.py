from app.db_classes.standard_model.getter import StandardModelGetter


class UserToMessageRelationGetter(StandardModelGetter):
    def by_user(self, user):
        self.manager.filter(self.manager.normal_cls.user_id_ == user.id)
        return self

    def by_message(self, message):
        self.manager.filter(self.manager.normal_cls.message_id_ == message.id)
        return self

    def by_read(self, read):
        self.manager.filter(self.manager.normal_cls.read_ == read)
        return self
