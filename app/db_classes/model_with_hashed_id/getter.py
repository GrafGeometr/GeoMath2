from app.db_classes.standard_model.getter import StandardModelGetter


class ModelWithHashedIdGetter(StandardModelGetter):
    def by_hashed_id(self, hashed_id):
        self.manager.filter(self.manager.normal_cls.hashed_id == hashed_id)
        return self
