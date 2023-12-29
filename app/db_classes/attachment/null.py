from app.imports import *
from app.sqlalchemy_custom_types import *

from app.db_classes.standard_model.null import NullStandardModel
from app.db_classes.attachment.abstract import AbstractAttachment


class NullAttachment(NullStandardModel, AbstractAttachment):
    # --> INITIALIZE
    __abstract__ = True

    # --> PROPERTIES
    @property
    def db_folder(self) -> str:
        pass

    @db_folder.setter
    def db_folder(self, db_folder: str):
        pass

    @property
    def db_filename(self) -> str:
        pass

    @db_filename.setter
    def db_filename(self, db_filename: str):
        pass

    @property
    def short_name(self) -> str:
        pass

    @short_name.setter
    def short_name(self, short_name: str):
        pass

    @property
    def parent_type(self) -> DbParentType:
        pass

    @parent_type.setter
    def parent_type(self, parent_type: DbParentType):
        pass

    @property
    def parent_id(self) -> int:
        pass

    @parent_id.setter
    def parent_id(self, parent_id: int):
        pass

    @property
    def other_data(self) -> dict:
        pass

    @other_data.setter
    def other_data(self, other_data: dict):
        pass

    # --> METHODS

    @classmethod
    def get_by_db_filename(cls, db_filename):
        pass

    @classmethod
    def get_all_by_parent(cls, parent):
        pass

    def get_parent(self):
        pass

    def is_secret(self):
        pass

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
