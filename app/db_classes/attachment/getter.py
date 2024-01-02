from app.db_classes.standard_model.getter import StandardModelGetter
from app.sqlalchemy_custom_types import *


class AttachmentGetter(StandardModelGetter):
    def by_id(self, id):
        self.manager.filter(self.manager.normal_cls.id == id)

    def by_short_name(self, name):
        self.manager.filter(self.manager.normal_cls.name == name)

    def by_db_filename(self, name):
        self.manager.filter(self.manager.normal_cls.db_filename == name)

    def by_parent(self, parent):
        self.manager.filter(self.manager.normal_cls.parent_id_ == parent.id)
        self.manager.filter(
            self.manager.normal_cls.parent_type_ == DbParent.from_type(type(parent))
        )
        return self
