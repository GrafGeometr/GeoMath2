from app.db_classes.model_with_name.getter import ModelWithNameGetter


class EmailGetter(ModelWithNameGetter):
    def by_verified(self, verified):
        self.manager.filter(self.manager.normal_cls.verified_ == verified)
        return self

    def by_user_id(self, user_id):
        print(user_id)
        self.manager.filter(self.manager.normal_cls.user_id_ == user_id)
        return self

    def by_user(self, user):
        print(user.id)
        return self.by_user_id(user.id)
