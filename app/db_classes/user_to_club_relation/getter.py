from app.db_classes.standard_model.getter import StandardModelGetter


class UserToClubRelationGetter(StandardModelGetter):
    def by_user(self, user):
        self.manager.filter(self.manager.normal_cls.user_id_ == user.id)
        return self

    def by_club(self, club):
        self.manager.filter(self.manager.normal_cls.pool_id_ == club.id)
        return self

    def by_role(self, role):
        self.manager.filter(self.manager.normal_cls.role_ == role)
        return self
