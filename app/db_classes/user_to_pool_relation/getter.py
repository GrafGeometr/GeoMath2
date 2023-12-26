from app.db_classes.standard_model.getter import StandardModelGetter


class UserToPoolRelationGetter(StandardModelGetter):
    def by_user(self, user):
        self.manager.filter(self.manager.normal_cls.user_id_ == user.id)
        return self

    def by_pool(self, pool):
        self.manager.filter(self.manager.normal_cls.pool_id_ == pool.id)
        return self

    def by_role(self, role):
        self.manager.filter(self.manager.normal_cls.role_ == role)
        return self
