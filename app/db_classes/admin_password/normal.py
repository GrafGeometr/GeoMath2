from app.db_classes.standard_model.normal import *


class AdminPassword(StandardModel):
    # --> INITIALIZE
    __abstract__ = False
    __tablename__ = "admin_password"

    password_ = db.Column(
        db.String, nullable=True, default=generate_password_hash("qwerty")
    )

    # --> RELATIONS

    # --> PROPERTIES
    @property
    def password(self):
        return self.password_

    @password.setter
    def password(self, password):
        self.password_ = password
        self.save()

    # --> FUNCTIONS
