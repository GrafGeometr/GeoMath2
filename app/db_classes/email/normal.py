from app.imports import *

from app.db_classes.standard_model.normal import StandardModel
from .abstract import AbstractEmail
from .null import NullEmail
from .getter import EmailGetter


class Email(ModelWithName):
    # --> INITIALIZE
    __tablename__ = "email"

    created_date = db.Column(db.DateTime, default=current_time)
    verified = db.Column(db.Boolean, default=False)
    token = db.Column(db.String, nullable=True)

    # --> RELATIONS
    user_id = db.Column(db.Integer, db.ForeignKey("user.id_"))

    # --> FUNCTIONS
