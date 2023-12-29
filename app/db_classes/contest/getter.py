from app.db_classes.model_with_name.getter import ModelWithNameGetter


class ContestGetter(ModelWithNameGetter):
    def by_pool(self, pool):
        self.manager.filter(self.manager.normal_cls.pool_id == pool.id)
        return self
    
    def by_id(self, id):
        self.manager.filter(self.manager.normal_cls.id == id)
        return self
    
    def by_olimpiad(self, olimpiad):
        self.manager.filter(self.manager.normal_cls.olimpiad == olimpiad)
        return self
    
    def by_season(self, season):
        self.manager.filter(self.manager.normal_cls.season == season)
        return self
    
    def by_grade(self, grade):
        self.manager.filter(self.manager.normal_cls.grade == grade)
        return self
