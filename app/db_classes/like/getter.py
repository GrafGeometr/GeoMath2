from app.db_classes.standard_model.getter import StandardModelGetter


class LikeGetter(StandardModelGetter):
    def by_parent(self, parent: "AbstractStandardModel") -> "LikeGetter":
        self.manager.filter(self.manager.normal_cls.parent_id_ == parent.id)
        return self

    def by_user(self, user: "AbstractUser") -> "LikeGetter":
        self.manager.filter(self.manager.normal_cls.user_id_ == user.id)
        return self
