from app.imports import *
from app.sqlalchemy_custom_types import *

from abc import abstractmethod
from app.db_classes.standard_model.normal import AbstractStandardModel


class AbstractAttachment(AbstractStandardModel):
    # --> INITIALIZE
    __abstract__ = True

    # --> PROPERTIES
    @property
    @abstractmethod
    def db_folder(self) -> str:
        pass

    @db_folder.setter
    @abstractmethod
    def db_folder(self, db_folder: str):
        pass

    @property
    @abstractmethod
    def db_filename(self) -> str:
        pass

    @db_filename.setter
    @abstractmethod
    def db_filename(self, db_filename: str):
        pass

    @property
    @abstractmethod
    def short_name(self) -> str:
        pass

    @short_name.setter
    @abstractmethod
    def short_name(self, short_name: str):
        pass

    @property
    @abstractmethod
    def parent_type(self) -> DbParentType:
        pass

    @parent_type.setter
    @abstractmethod
    def parent_type(self, parent_type: DbParentType):
        pass

    @property
    @abstractmethod
    def parent_id(self) -> int:
        pass

    @parent_id.setter
    @abstractmethod
    def parent_id(self, parent_id: int):
        pass

    @property
    @abstractmethod
    def other_data(self) -> dict:
        pass

    @other_data.setter
    @abstractmethod
    def other_data(self, other_data: dict):
        pass

    # --> METHODS


    @classmethod
    @abstractmethod
    def get_all_by_parent(cls, parent):
        pass

    @abstractmethod
    def get_parent(self):
        pass

    @abstractmethod
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
