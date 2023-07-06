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