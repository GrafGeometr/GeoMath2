from app.db_classes.standard_model.getter import StandardModelGetter


class ModelWithNameGetter(StandardModelGetter):
    def by_name(self, name):
        self.manager.filter(self.manager.normal_cls.name_ == name)
        return self
