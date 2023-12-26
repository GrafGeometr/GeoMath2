from app.db_classes.model_with_name.getter import ModelWithNameGetter
from app.db_classes.model_with_hashed_id.getter import ModelWithHashedIdGetter


class UserGetter(ModelWithNameGetter, ModelWithHashedIdGetter):
    def by_verified_email(self, email):
        self.manager.filter(self.manager.normal_cls.email.id_ == email.id)
        return self
