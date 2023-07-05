from app.imports import *
from app.sqlalchemy_custom_types import *

class Attachment(db.Model):
    # --> INITIALIZE
    __tablename__ = "attachment"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    db_folder = db.Column(db.String)
    db_filename = db.Column(db.String)
    short_name = db.Column(db.String)
    parent_type = db.Column(db.String)  # 'Problem' | 'Sheet' | 'Contest_User_Solution'
    parent_id = db.Column(db.Integer)
    other_data = db.Column(db.JSON, default={})

    # --> RELATIONS

    # --> FUNCTIONS
    def get_parent(self):
        from app.dbc import Problem, Sheet, Contest_User_Solution
        if self.parent_type == "Problem":  
            return Problem.query.filter_by(id=self.parent_id).first()
        elif self.parent_type == "Sheet":
            return Sheet.query.filter_by(id=self.parent_id).first()
        elif self.parent_type == "Contest_User_Solution":
            return Contest_User_Solution.query.filter_by(id=self.parent_id).first()

    def remove(self):
        try:
            os.remove(os.path.join(self.db_folder, self.db_filename))
        except:
            pass
        db.session.delete(self)
        db.session.commit()