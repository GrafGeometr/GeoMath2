from app.db_classes.getter.getter import BaseGetter


class StandardModelGetter(BaseGetter):
    def by_id(self, id):
        self.manager.filter(self.manager.normal_cls.id == id)
        return self
