from app.imports import *
from app.sqlalchemy_custom_types import *

class Tag(db.Model):
    # --> INITIALIZE
    __tablename__ = "tag"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, unique=True, nullable=True)

    # --> RELATIONS

    # --> FUNCTIONS
    @staticmethod
    def get_by_id(id):
        return Tag.query.filter_by(id=id).first()
    
    @staticmethod
    def get_by_name(name):
        return Tag.query.filter_by(name=name).first()
    

    @staticmethod
    def get_all_by_obj(obj):
        if obj is None:
            return []
        from app.dbc import Tag_Relation
        return [tr.tag for tr in Tag_Relation.get_all_by_parent(obj)]


    def act_set_name(self, name):
        self.name = name
        db.session.commit()
        return self


    def add(self):
        db.session.add(self)
        db.session.commit()
        return self
    
    def remove(self):
        raise NotImplementedError("Emplement remove tag")

    def save(self):
        db.session.commit()
        return self