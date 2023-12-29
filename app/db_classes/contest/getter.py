from app.db_classes.model_with_name.getter import ModelWithNameGetter


class ContestGetter(ModelWithNameGetter):
    def by_pool(self, pool):
        self.manager.filter(self.manager.normal_cls.pool_id == pool.id)
        return self
    
    def by_id(self, id):
        self.manager.filter(self.manager.normal_cls.id == id)
        return self
