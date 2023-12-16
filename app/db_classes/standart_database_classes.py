from app.imports import *
from app.sqlalchemy_custom_types import *


class StandartModel:
    # --> INITIALIZE

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    # --> FUNCTIONS
    def save(self):
        db.session.commit()
        return self

    def add(self):
        db.session.add(self)
        return self.save()

    def remove(self):
        db.session.delete(self)
        db.session.commit()
    
    @staticmethod
    def get_by_id(self, id):
        return type(self).query.filter_by(id=id).first()


class ModelWithHashedId(StandartModel):
    # --> INITIALIZE

    hashed_id = db.Column(db.String, unique=True, nullable=True)

    # --> FUNCTIONS
    def add(self):
        db.session.add(self)
        self.act_set_hashed_id()
        return self

    def act_set_hashed_id(self):
        while True:
            hashed_id = generate_token(20)
            if not type(self).query.filter_by(hashed_id=hashed_id).first():
                self.hashed_id = hashed_id
                break

        self.hashed_id = hashed_id
        return self.save()
