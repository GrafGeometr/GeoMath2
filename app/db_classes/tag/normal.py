from app.imports import *
from typing import List

from app.db_classes.model_with_name.normal import ModelWithName
from app.db_classes.tag.abstract import AbstractTag
from app.db_classes.tag.null import NullTag
from app.db_classes.tag.getter import TagGetter


class Tag(ModelWithName, AbstractTag):
    # --> INITIALIZE
    __abstract__ = False
    __tablename__ = "tag"

    hash_ = db.Column(db.Integer, nullable=True)


    null_cls_ = NullTag
    getter_cls_ = TagGetter

    # --> RELATIONS
    topic_id_ = db.Column(db.Integer, db.ForeignKey("topic.id_"))
    tag_relations_ = db.relationship("TagRelation", backref="tag_")

    # --> JSON
    @property
    def JSON(self):
        return {
            "id": self.id,
            "name": self.name,
            "hash": self.hash,
            "topic": self.topic.JSON
        }

    # --> PROPERTIES
    @property
    def hash(self) -> int:
        return self.get_hash()

    @hash.setter
    def hash(self, hash: int):
        self.hash_ = hash
        self.save()

    @property
    def topic_id(self) -> int:
        return self.topic_id_
    
    @topic_id.setter
    def topic_id(self, topic_id: int):
        self.topic_id_ = topic_id
        self.save()

    @property
    def topic(self) -> "Topic":
        return self.topic_
    
    @topic.setter
    def topic(self, topic: "Topic"):
        self.topic_ = topic
        self.save()

    @property
    def tag_relations(self) -> List["TagRelation"]:
        return self.tag_relations_
    
    @tag_relations.setter
    def tag_relations(self, tag_relations: List["TagRelation"]):
        self.tag_relations_ = tag_relations
        self.save()

    # --> METHODS
    @staticmethod
    def get_all_by_obj(obj):
        from app.dbc import TagRelation

        return [tr.tag for tr in TagRelation.get.by_parent(obj).all()]

    def add(self):
        t = Tag.get_by_name(self.name)
        if t is not None:
            return t
        db.session.add(self)
        db.session.commit()
        return self

    def remove(self):
        raise NotImplementedError("Emplement remove tag")

    def get_hash(self):
        from app.utils_and_functions.usefull_functions import get_string_hash

        if self.hash_ is None:
            self.hash = get_string_hash(self.name.lower())
        return self.hash_
    
    def is_source(self):
        return self.topic.is_source()
    def is_theme(self):
        return self.topic.is_theme()
