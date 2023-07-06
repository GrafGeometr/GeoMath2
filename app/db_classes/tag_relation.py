from app.imports import *
from app.sqlalchemy_custom_types import *

class Tag_Relation(db.Model):
    # --> INITIALIZE
    __tablename__ = "tag_relation"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tag_id = db.Column(db.Integer)
    parent_type = db.Column(db.String)  # 'Problem' | 'Sheet'
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

    def add(self):
        db.session.add(self)
        db.session.commit()
        return self

    def remove(self):
        db.session.delete(self)
        db.session.commit()
    
    @staticmethod
    def get_by_id(id):
        return Tag_Relation.query.filter_by(id=id).first()
    
    @staticmethod
    def get_all_by_parent(parent):
        if parent is None:
            return []
        from app.dbc import Problem, Sheet, Contest
        parent_type = {Problem: "Problem", Sheet: "Sheet", Contest: "Contest"}.get(type(parent), None)
        if parent_type is None:
            return []
        return Tag_Relation.query.filter_by(parent_type=parent_type, parent_id=parent.id).all()
    
    def save(self):
        db.session.commit()
        return self