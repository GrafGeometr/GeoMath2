from .imports import *
from .model_imports import *

to_olimpiads = Blueprint("to_olimpiads", __name__)


@login_required
@admin_required
@to_olimpiads.route("/to_olimpiads")
def to_olimpiads_page():
    olimpiads_old_names = [
        "Всероссийская олимпиада школьников",
        "Санкт-Петербургская олимпиада школьников по математике",
        "Формула Единства",
    ]

    rename_dict = {x: x for x in olimpiads_old_names}
    rename_dict[
        "Формула Единства"
    ] = "Олимпиада «Формула Единства» / «Третье тысячелетие»\n(Заключительный этап)"
    rename_dict[
        "Санкт-Петербургская олимпиада школьников по математике"
    ] = "Санкт-Петербургская олимпиада школьников по математике\n(Заключительный этап)"

    tags = list(map(lambda tag: tag.name, Tag.query.all()))

    seasons = set(filter(
            lambda s: len(s) == 7
            and s[:4].isdigit()
            and s[4] == "-"
            and s[5:].isdigit(),
            tags
        )
    )

    grades = set(filter(lambda s: s.endswith("класс"), tags))

    for name in olimpiads_old_names:
        if name == "Всероссийская олимпиада школьников":
            Olimpiad(name=name + "\n(Заключительный этап)").add().act_set_category(
                "Всероссийская"
            )
            Olimpiad(name=name + "\n(Региональный этап)").add().act_set_category(
                "Всероссийская"
            )
        else:
            Olimpiad(name=rename_dict[name]).add().act_set_category("Перечневая")

    for problem in Problem.query.all():
        cur_seasons = set(problem.get_tag_names()).intersection(seasons)
        cur_grades = set(problem.get_tag_names()).intersection(grades)
        cur_olimpiad_names = set(problem.get_tag_names()).intersection(
            olimpiads_old_names
        )

        for season in cur_seasons:
            for grade in cur_grades:
                for olimpiad_name in cur_olimpiad_names:
                    if olimpiad_name == "Всероссийская олимпиада школьников":
                        if "Заключительный этап" in problem.get_tag_names():
                            olimpiad = Olimpiad.get_by_name(
                                olimpiad_name + "\n(Заключительный этап)"
                            )
                        else:
                            olimpiad = Olimpiad.get_by_name(
                                olimpiad_name + "\n(Региональный этап)"
                            )
                    else:
                        olimpiad = Olimpiad.get_by_name(rename_dict[olimpiad_name])

                    contest = olimpiad.get_contest_by_season_and_grade(season, grade)
                    if contest is None:
                        contest = Contest(
                            name=season,
                            grade=grade,
                            olimpiad_id=olimpiad.id,
                            is_public=True
                        ).add()


                    if problem.is_in_contest(contest):
                        continue
                    cp = Contest_Problem(contest_id=contest.id, problem_id=problem.id).add()
                    cp.act_set_max_score(1 if olimpiad_name == "Санкт-Петербургская олимпиада школьников по математике\n(Заключительный этап)" else 7)

    return "DONE!"
