from app.db_classes.standard_model.getter import StandardModelGetter


class MessageGetter(StandardModelGetter):
    def by_user(self, user: "AbstractUser") -> "LikeGetter":
        self.manager.filter(self.manager.normal_cls.user_id_ == user.id)
        return self
