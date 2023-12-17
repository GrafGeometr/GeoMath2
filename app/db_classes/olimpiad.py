from app.imports import *
from app.sqlalchemy_custom_types import *

from app.db_classes.standart_database_classes import *


class Olimpiad(db.Model, ModelWithName):
    # --> INITIALIZE
    __tablename__ = "olimpiad"

    category = db.Column(db.String)

    # --> RELATIONS
    contests = db.relationship("Contest", backref="olimpiad")

    # --> FUNCTIONS
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

    def act_set_category(self, category):
        self.category = category
        return self.save()

    def act_add_contest(self, contest):
        self.contests.append(contest)
        return self.save()

    def get_contests(self):
        return self.contests

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

    def get_contest_by_season_and_grade(self, season, grade):
        from app.db_classes.contest import Contest

        return (
            db.session.query(Contest)
            .filter(
                Contest.olimpiad_id == self.id,
                Contest.grade == grade,
                Contest.name == season,
            )
            .first()
        )

    def get_seasons_list(self):
        return list(set(contest.name for contest in self.contests))

    def get_grades_list(self):
        return list(set(contest.grade for contest in self.contests))
