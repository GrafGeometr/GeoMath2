from app.db_classes.standard_model.getter import StandardModelGetter
class FriendGetter(StandardModelGetter):
    def by_friend_from(self, friend_from):
        self.manager.filter(self.manager.normal_cls.friend_from == friend_from.id)
        return self
    
    def by_friend_to(self, friend_to):
        self.manager.filter(self.manager.normal_cls.friend_to == friend_to.id)
        return self
    
    def by_accepted(self, accepted):
        self.manager.filter(self.manager.normal_cls.accepted == accepted)
        return self