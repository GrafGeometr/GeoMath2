from app.db_classes.standard_model.getter import StandardModelGetter


class ChatGetter(StandardModelGetter):
    def by_name(self, name):
        self.manager.filter(self.manager.normal_cls.name == name)
        return self
