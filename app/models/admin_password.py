from app.imports import *
from app.sqlalchemy_custom_types import *

class AdminPassword(db.Model):
    __tablename__ = "admin_password"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    password = db.Column(
        db.String, nullable=True, default=generate_password_hash("qwerty")
    )