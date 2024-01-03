from typing import List
from app.imports import *

from app.db_classes.standard_model.normal import StandardModel
from .abstract import AbstractTopic
from .null import NullTopic
from .getter import TopicGetter

class Topic(StandardModel, AbstractTopic):
    # --> INITIALIZE
    __abstract__ = False
    __tablename__ = "topic"

    getter_cls_ = TopicGetter
    null_cls_ = NullTopic

    color_ = db.Column(db.String)
    # for frontend
    name_ = db.Column(db.String)
    # 'Олимпиада', 'Год', 'Класс', 'Геометрия', 'Алгебра', 'Комбинаторика', 'Теория чисел'

    # --> RELATIONS
    tags_ = db.relationship("Tag", backref="topic_")

    # --> JSON
    @property
    def JSON(self):
        return {
            "id": self.id,
            "name": self.name,
            "color": self.color,
            "tags": [tag.name for tag in self.tags]
        }

    # --> PROPERTIES
    @property
    def color(self) -> str:
        return self.color_
    
    @color.setter
    def color(self, value: str):
        self.color_ = value
        self.save()

    @property
    def name(self) -> str:
        return self.name_
    
    @name.setter
    def name(self, value: str):
        self.name_ = value
        self.save()

    @property
    def tags(self) -> List["Tag"]:
        return self.tags_
    
    @tags.setter
    def tags(self, value: List["Tag"]):
        self.tags_ = value
        self.save()

    def is_source(self) -> bool:
        return (self.name in ["Олимпиада", "Год", "Класс"])
    def is_theme(self) -> bool:
        return not self.is_source()