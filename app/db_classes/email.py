from app.imports import *
from app.sqlalchemy_custom_types import *

class Email(db.Model):
    __tablename__ = "email"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=True)
    created_date = db.Column(db.DateTime, default=current_time)
    verified = db.Column(db.Boolean, default=False)
    token = db.Column(db.String, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))