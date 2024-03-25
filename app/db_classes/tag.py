from app.imports import *
from app.sqlalchemy_custom_types import *


class Tag(db.Model):
    # --> INITIALIZE
    __tablename__ = "tag"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, unique=True, nullable=True)

    hash = db.Column(db.Integer, nullable=True)

    topic_id = db.Column(db.Integer, db.ForeignKey("topic.id"))

    # --> RELATIONS

    # --> FUNCTIONS
    @staticmethod
    def add_by_name_and_topic(name, topic):
        from app.db_classes.topic import Topic

        topic = Topic.get_by_name(topic)
        return Tag(name=name, topic_id=topic.id).add()

    @staticmethod
    def get_by_id(id):
        return Tag.query.filter_by(id=id).first()

    @staticmethod
    def get_by_name(name):
        return Tag.query.filter_by(name=name).first()

    @staticmethod
    def get_all_by_obj(obj):
        if obj is None:
            return []
        from app.dbc import Tag_Relation

        return [tr.tag for tr in Tag_Relation.get_all_by_parent(obj)]

    def act_set_name(self, name):
        self.name = name
        db.session.commit()
        return self

    def add(self):
        t = Tag.get_by_name(self.name)
        if t is not None:
            return t
        db.session.add(self)
        db.session.commit()
        return self

    def remove(self):
        from app.db_classes.tag_relation import Tag_Relation

        tr = Tag_Relation.get_all_by_tag_id(self.id)
        for el in tr:
            db.session.delete(el)
        db.session.delete(self)
        db.session.commit()

    def save(self):
        db.session.commit()
        return self

    def get_hash(self):
        from app.utils_and_functions.usefull_functions import get_string_hash

        if self.hash is None:
            self.hash = get_string_hash(self.name.lower())
            self.save()
        return self.hash
