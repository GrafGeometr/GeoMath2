from app.db_classes.standard_model.normal import *


class AdminPassword(StandardModel):
    # --> INITIALIZE
    __abstract__ = False
    __tablename__ = "admin_password"

    password = db.Column(
        db.String, nullable=True, default=generate_password_hash("qwerty")
    )

    # --> RELATIONS

    # --> FUNCTIONS
