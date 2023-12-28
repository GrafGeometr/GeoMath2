from app.db_classes.model_with_name.getter import ModelWithNameGetter


class OlimpiadGetter(ModelWithNameGetter):
    def by_grade(self, grade: str):
        self.manager.filter(self.manager.normal_cls.grade_ == grade)
        return self

    def by_category(self, category: str):
        self.manager.filter(self.manager.normal_cls.category_ == category)
        return self

    def by_short_name(self, short_name: str):
        self.manager.filter(self.manager.normal_cls.short_name_ == short_name)
        return self
