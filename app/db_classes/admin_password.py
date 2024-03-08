from app.imports import *
from app.sqlalchemy_custom_types import *


class Admin_Password(db.Model):
    # --> INITIALIZE
    __tablename__ = "admin_password"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    password = db.Column(
        db.String, nullable=True, default=generate_password_hash("qwerty")
    )

    # --> RELATIONS

    # --> FUNCTIONS

    @staticmethod
    def get_by_id(id):
        return Admin_Password.query.filter_by(id=id).first()
