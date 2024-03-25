from app.imports import *
from app.sqlalchemy_custom_types import *


class Olimpiad_Variant(db.Model):
    # --> INITIALIZE
    __tablename__ = "olimpiad_variant"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    grade = db.Column(GradeClassType)
    year = db.Column(db.String)
    variant = db.Column(db.String)

    # --> RELATIONS
    olimpiad_id = db.Column(db.Integer, db.ForeignKey("olimpiad.id"))
    contests = db.relationship("Contest", backref="olimpiad_variant")

    # --> FUNCTIONS
    def add(self):
        db.session.add(self)
        db.session.commit()
        return self
    
    def remove(self):
        for c in self.contests:
            c.remove()
        db.session.delete(self)
        db.session.commit()
