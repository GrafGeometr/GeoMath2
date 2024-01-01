from app.db_classes.standard_model.getter import StandardModelGetter


class EmailGetter(StandardModelGetter):
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
    
    def by_name(self, name):
        self.manager.filter(self.manager.normal_cls.name_ == name)
        return self
