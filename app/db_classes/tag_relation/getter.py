from app.db_classes.standard_model.getter import StandardModelGetter
from app.sqlalchemy_custom_types import *


class TagRelationGetter(StandardModelGetter):
    def by_tag(self, tag):
        self.manager.filter(self.manager.normal_cls.tag_id_ == tag.id)
        return self

    def by_parent(self, parent):
        self.manager.filter(
            self.manager.normal_cls.parent_type_ == DbParent.from_type(type(parent))
        )
        self.manager.filter(self.manager.normal_cls.parent_id_ == parent.id)
        return self
