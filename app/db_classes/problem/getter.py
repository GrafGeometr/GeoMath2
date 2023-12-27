from app.db_classes.model_with_name.getter import ModelWithNameGetter
from app.db_classes.model_with_hashed_id.getter import ModelWithHashedIdGetter


class ProblemGetter(ModelWithNameGetter, ModelWithHashedIdGetter):
    def by_pool(self, pool):
        self.manager.filter(self.manager.normal_cls.pool_id_ == pool.id)
        return self
