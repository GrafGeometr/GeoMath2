from app.db_classes.standard_model.getter import StandardModelGetter


class UserToChatRelationGetter(StandardModelGetter):
    def by_user(self, user):
        self.manager.filter(self.manager.normal_cls.user_id_ == user.id)
        return self

    def by_chat(self, chat):
        self.manager.filter(self.manager.normal_cls.chat_id_ == chat.id)
        return self
