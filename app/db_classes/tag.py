from app.imports import *
from app.sqlalchemy_custom_types import *

class Tag(db.Model):
    # --> INITIALIZE
    __tablename__ = "tag"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, unique=True, nullable=True)

    # --> RELATIONS

    # --> FUNCTIONS