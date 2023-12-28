from app.imports import *

from app.sqlalchemy_custom_types import *

from app.db_classes.model_with_name.normal import ModelWithName

from app.db_classes.olimpiad.abstract import AbstractOlimpiad
from app.db_classes.olimpiad.null import NullOlimpiad
from app.db_classes.olimpiad.getter import OlimpiadGetter


class Olimpiad(ModelWithName, AbstractOlimpiad):
    # --> INITIALIZE
    __abstract__ = False
    __tablename__ = "olimpiad"

    short_name_ = db.Column(db.String, unique=True)
    category_ = db.Column(db.String)

    null_cls_ = NullOlimpiad
    getter_cls_ = OlimpiadGetter

    # --> RELATIONS
    contests_ = db.relationship("Contest", backref="olimpiad_")

    # --> PROPERTIES
    @property
    def short_name(self):
        return self.short_name_

    @short_name.setter
    def short_name(self, value):
        self.short_name_ = value
        self.save()

    @property
    def category(self):
        return self.category_

    @category.setter
    def category(self, value):
        self.category_ = value
        self.save()

    @property
    def contests(self):
        return self.contests_

    @contests.setter
    def contests(self, value):
        self.contests_ = value
        self.save()

    # --> METHODS
    def num_of_seasons_to_str(self):
        n = len(self.get_structure())
        if n % 10 == 1:
            if n % 100 == 11:
                return f"{n} сезонов"
            return f"{n} сезон"
        if n % 10 == 0:
            return f"{n} сезонов"
        if 2 <= n % 10 <= 4:
            return f"{n} сезона"
        return f"{n} сезонов"

    def act_add_contest(self, contest):
        self.contests.append(contest)
        return self.save()

    def get_structure(self):
        result = OrderedDict()
        for contest in sorted(
            self.contests,
            key=lambda contest: (contest.name, contest.grade),
            reverse=True,
        ):
            if contest.name not in result:
                result[contest.name] = {}
            result[contest.name][str(contest.grade)] = contest
        return result

    def get_seasons_list(self):
        return list(set(contest.name for contest in self.contests))

    def get_grades_list(self):
        return list(set(contest.grade for contest in self.contests))

    def fix_name(self):
        self.name = self.name.replace("\n", " ")
        return self.save()
