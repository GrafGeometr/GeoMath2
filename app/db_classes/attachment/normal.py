from app.imports import *
from app.sqlalchemy_custom_types import *

from app.db_classes.standard_model.normal import StandardModel
from .abstract import AbstractAttachment
from .null import NullAttachment
from .getter import AttachmentGetter


class Attachment(AbstractAttachment, StandardModel):
    # --> INITIALIZE
    __abstract__ = False
    __tablename__ = "attachment"

    db_folder_ = db.Column(db.String)
    db_filename_ = db.Column(db.String)
    short_name_ = db.Column(db.String)
    parent_type_ = db.Column(DbParentType)
    # parent_type = db.Column(db.String)  # 'Problem' | 'Sheet' | 'Contest_User_Solution'
    parent_id_ = db.Column(db.Integer)
    other_data_ = db.Column(db.JSON, default={})

    null_cls_ = NullAttachment
    getter_cls_ = AttachmentGetter

    # --> RELATIONS

    # --> PROPERTIES
    @property
    def db_folder(self):
        return self.db_folder_

    @db_folder.setter
    def db_folder(self, value):
        self.db_folder_ = value
        self.save()

    @property
    def db_filename(self):
        return self.db_filename_

    @db_filename.setter
    def db_filename(self, value):
        self.db_filename_ = value
        self.save()

    @property
    def short_name(self):
        return self.short_name_

    @short_name.setter
    def short_name(self, value):
        self.short_name_ = value
        self.save()

    @property
    def parent_type(self):
        return self.parent_type_

    @parent_type.setter
    def parent_type(self, value):
        self.parent_type_ = value
        self.save()

    @property
    def parent_id(self):
        return self.parent_id_

    @parent_id.setter
    def parent_id(self, value):
        self.parent_id_ = value
        self.save()

    @property
    def other_data(self):
        return self.other_data_

    @other_data.setter
    def other_data(self, value):
        self.other_data_ = value
        self.save()

    # --> FUNCTIONS

    def get_parent(self):
        par_type = self.parent_type.to_type()

        if par_type is None:
            return None
        return par_type.get_by_id(self.parent_id)

    def is_secret(self):
        if self.other_data.get("is_secret") is None:
            self.other_data["is_secret"] = False
        return self.other_data["is_secret"]

    def is_from_parent(self, obj):
        return (
            self.parent_type == DbParent.from_type(type(obj))
            and self.parent_id == obj.id
        )

    def remove(self):
        try:
            os.remove(os.path.join(self.db_folder, self.db_filename))
        except:
            pass
        db.session.delete(self)
        db.session.commit()
