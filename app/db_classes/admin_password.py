from app.imports import *
from app.sqlalchemy_custom_types import *

from app.db_classes.standart_database_classes import *


class Admin_Password(db.Model, StandartModel):
    # --> INITIALIZE
    __tablename__ = "admin_password"

    password = db.Column(
        db.String, nullable=True, default=generate_password_hash("qwerty")
    )

    # --> RELATIONS

    # --> FUNCTIONS
