from app.db_classes.model_with_name.getter import ModelWithNameGetter


class ChatGetter(ModelWithNameGetter):
    def by_name(self, name):
        self.manager.filter(self.manager.normal_cls.name == name)
        return self
