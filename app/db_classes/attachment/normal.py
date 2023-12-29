from app.imports import *
from app.sqlalchemy_custom_types import *

from app.db_classes.standard_model.normal import StandardModel


class Attachment(StandardModel):
    # --> INITIALIZE
    __abstract__ = False
    __tablename__ = "attachment"

    db_folder = db.Column(db.String)
    db_filename = db.Column(db.String)
    short_name = db.Column(db.String)
    parent_type = db.Column(DbParentType)
    # parent_type = db.Column(db.String)  # 'Problem' | 'Sheet' | 'Contest_User_Solution'
    parent_id = db.Column(db.Integer)
    other_data = db.Column(db.JSON, default={})

    # --> RELATIONS

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
