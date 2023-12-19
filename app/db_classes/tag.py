from app.imports import *
from app.sqlalchemy_custom_types import *

from app.db_classes.standart_database_classes import *


class Tag(db.Model, ModelWithName):
    # --> INITIALIZE
    __tablename__ = "tag"

    hash = db.Column(db.Integer, nullable=True)

    # --> RELATIONS

    # --> FUNCTIONS
    @staticmethod
    def get_all_by_obj(obj):
        if obj is None:
            return []
        from app.dbc import Tag_Relation

        return [tr.tag for tr in Tag_Relation.get_all_by_parent(obj)]


    def add(self):
        t = Tag.get_by_name(self.name)
        if t is not None:
            return t
        db.session.add(self)
        db.session.commit()
        return self
    
    def remove(self):
        raise NotImplementedError("Emplement remove tag")

    def get_hash(self):
        from app.utils_and_functions.usefull_functions import get_string_hash

        if self.hash is None:
            self.hash = get_string_hash(self.name.lower())
            self.save()
        return self.hash
