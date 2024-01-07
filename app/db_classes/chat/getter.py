from app.db_classes.model_with_name.getter import ModelWithNameGetter
from app.db_classes.model_with_hashed_id.getter import ModelWithHashedIdGetter


class ChatGetter(ModelWithNameGetter, ModelWithHashedIdGetter):
    pass
