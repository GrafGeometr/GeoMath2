from app.imports import *
from app.sqlalchemy_custom_types import *


class Topic(db.Model):
    # --> INITIALIZE
    __tablename__ = "topic"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)

    color = db.Column(db.String)

    tags = db.relationship("Tag", backref="topic")

    @staticmethod
    def get_by_id(id):
        if id is None:
            return None
        return Topic.query.filter_by(id=id).first()

    @staticmethod
    def get_by_name(name):
        if name is None:
            return None
        return Topic.query.filter_by(name=name).first()

    def add(self):
        db.session.add(self)
        db.session.commit()
        return self

    def save(self):
        db.session.commit()
        return self

    def remove(self):
        db.session.delete(self)
        db.session.commit()

    def act_set_name(self, name):
        self.name = name
        db.session.commit()
        return self

    def act_set_color(self, color):
        self.color = color
        db.session.commit()
        return self
