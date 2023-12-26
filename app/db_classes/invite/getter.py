from app.db_classes.standard_model.getter import StandardModelGetter
from app.sqlalchemy_custom_types import *

class Getter(StandardModelGetter):
    def by_parent(self, parent):
        self.manager.filter(self.manager.normal_cls.parent_id_ == parent.id)
        self.manager.filter(self.manager.normal_cls.parent_type_ == DbParent.from_type(type(parent)))
        return self