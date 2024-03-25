from .imports import *
from .model_imports import *

parse = Blueprint("parse", __name__)

import bs4
import requests
from bs4 import BeautifulSoup
import time
import re
import json


# --> НЕКОТОРЫЕ ПОЛЕЗНЫЕ ФУНКЦИИ <--
def get_soup(
    url, clear=False
):  # парсит HTML со страницы и удаляет теги <p>, если clear
    time.sleep(0.5)
    page = requests.get(url)
    text = page.text
    if clear:
        for bad_tag in ["p", "/p", "p/"]:
            text = text.replace(f"<{bad_tag}>", " ")
    soup = BeautifulSoup(text, "html.parser")
    return soup


def stripper(s):  # убирает пробельные символы по краям
    return s.strip("\n").strip("\t").strip("\r")


def clearing(s):  # убирает множественные пробелы
    return " ".join(el for el in s.split() if el != "")


def fix_year(n):  # записывает год в формате 2023/24
    return str(n - 1) + "/" + str(n)[-2:]


def get_all_numbers(s):  # считывает числа из строки, в том числе диапазоны
    _s = ""
    for c in s:
        if c.isdigit() or c == "-":
            _s += c
        else:
            _s += " "
    res = []
    for el in _s.split():
        if "-" not in el:  # число
            res.append(el)
        else:  # диапазон вида 8-11
            r = el.split("-")
            for i in range(int(r[0]), int(r[1]) + 1):
                res.append(str(i))
    return res


def work(id):  # записывает данные о задаче в JSON
    p = parse(id)
    with open(f"problem-{id}.json", "w") as f:
        f.write(str(p))


# --> СПИСОК ТЕМ <--
# TODO: ПЕРЕНЕСТИ ИХ В ОТДЕЛЬНЫЙ ФАЙЛ ИЛИ В SQL)
themes_renamer = {
    "Логика и теория множеств": "Комбинаторика",
    "Алгебра и арифметика": "Алгебра",
    "Геометрия": "Геометрия",
    "Комбинаторика": "Комбинаторика",
    "Вероятность и статистика": "Алгебра",
    "Математический анализ": "Алгебра",
    "Методы": "Комбинаторика",
}

second_themes_renamer = {
    "Математическая логика": "Комбинаторика",
    "Теория множеств": "Комбинаторика",
    "Отношение порядка": "Комбинаторика",
    "Отношение эквивалентности. Классы эквивалентности": "Комбинаторика",
    "Лингвистика": "Комбинаторика",
    "Задачи-шутки": None,
    "Теория алгоритмов": "Комбинаторика",
    "Логика и теория множеств (прочее)": "Комбинаторика",
    "Арифметика. Устный счет и т.п.": None,
    "Арифметические действия. Числовые тождества": None,
    "Средние величины": None,
    "Текстовые задачи": None,
    "Дроби": "Теория чисел",
    "Системы счисления": "Теория чисел",
    "Модуль числа": "Алгебра",
    "Многочлены": "Алгебра",
    "Формальные степенные ряды": "Алгебра",
    "Алгебраическая геометрия": "Алгебра",
    "Рациональные функции": "Теория чисел",
    "Корни. Степень с рациональным показателем": "Алгебра",
    "Линейная и полилинейная алгебра": "Алгебра",
    "Теория групп": "Комбинаторика",
    "Теория чисел. Делимость": "Теория чисел",
    "Теория чисел. Делимость (прочее)": "Теория чисел",
    "Последовательности": None,
    "Алгебраические неравенства и системы неравенств": "Алгебра",
    "Алгебраические уравнения и системы уравнений": "Алгебра",
    "Тригонометрия": "Алгебра",
    "Показательные функции и логарифмы": "Алгебра",
    "Комплексные числа": "Алгебра",
    "Графики и ГМТ на координатной плоскости": None,
    "Алгебра и арифметика (прочее)": "Алгебра",
    "Планиметрия": "Геометрия",
    "Стереометрия": "Геометрия",
    "Проективная геометрия": "Геометрия",
    "Аффинная геометрия": "Геометрия",
    "Комбинаторная геометрия": "Комбинаторная геометрия",
    "Топология": None,
    "Выпуклый анализ и линейное программирование": None,
    "Геометрия (прочее)": "Геометрия",
    "Классическая комбинаторика": "Комбинаторика",
    "Треугольник Паскаля и бином Ньютона": "Комбинаторика",
    "Производящие функции": "Алгебра",
    "Числа Каталана": "Комбинаторика",
    "Теория графов": "Комбинаторика",
    "Комбинаторика (прочее)": "Комбинаторика",
    "Теория вероятностей": "Комбинаторика",
    "Математическая статистика": "Комбинаторика",
    "Действительные числа": "Теория чисел",
    "Числовые последовательности": "Теория чисел",
    "Функции одной переменной. Непрерывность": "Алгебра",
    "Производная": "Алгебра",
    "Интеграл": "Алгебра",
    "Ряды": "Алгебра",
    "Последовательности и ряды функций": "Алгебра",
    "Функции нескольких переменных": "Алгебра",
    "Математический анализ (прочее)": "Алгебра",
    "Индукция": "Комбинаторика",
    "Принцип Дирихле": "Комбинаторика",
    "Принцип крайнего": "Комбинаторика",
    "Инварианты и полуинварианты": "Комбинаторика",
    "Вспомогательная раскраска": "Комбинаторика",
    "Алгебраические методы": "Алгебра",
    "Геометрические методы": "Геометрия",
    "Методы математического анализа": "Алгебра",
    "Доказательство от противного": None,
    "Примеры и контрпримеры. Конструкции": None,
    "Методы решения задач с параметром": "Алгебра",
    "Оценка + пример": "Комбинаторика",
}


# --> ПАРСЕР ТЕМ <--
def parse_theme_root(url):  # парсит корень по themes_renamer
    soup = get_soup(f"https://problems.ru{url}")
    tmp = soup.findAll("a")
    for a in tmp:
        if a.get("href", 0) != url:
            continue
        while a is not None:
            if a.name == "a":
                root = stripper(a.text)
                if root in themes_renamer:
                    break
            a = a.previousSibling
        break

    return themes_renamer.get(root, None)


def parse_theme_preroot(url):  # парсит корень из second_themes_renamer
    soup = get_soup(f"https://problems.ru{url}")
    tmp = soup.findAll("a")
    for a in tmp:
        if a.get("href", 0) != url:
            continue
        while a is not None:
            if a.name == "a":
                root = stripper(a.text)
                if root in second_themes_renamer:
                    break
            a = a.previousSibling
        break
    return second_themes_renamer.get(root, None)


def parse_latex(RESP):
    latex_statement = ""
    latex_solution = ""

    images = {}
    link_to_image_name = {}

    statement_source: list = RESP["statement"]
    statement_source.remove({"type": "header", "content": "Условие"})
    for block in statement_source:
        if block["type"] == "text":
            block["content"] = block["content"].replace("\n", " ")
            block["content"] = block["content"].replace("\\n", " ")
            block["content"] = block["content"].replace("\r", " ")
            block["content"] = block["content"].replace("\\r", " ")
            latex_statement += block["content"] + "\n\n"
        elif block["type"] == "header":
            block["content"] = block["content"].replace("\n", " ")
            block["content"] = block["content"].replace("\\n", " ")
            block["content"] = block["content"].replace("\r", " ")
            block["content"] = block["content"].replace("\\r", " ")
            latex_statement += f'\\textbf{{{block["content"]}}}' + "\n\n"
        elif block["type"] == "img":
            if link_to_image_name.get(block["content"], None) is None:
                name = f"Рис. {len(link_to_image_name) + 1}"
                link_to_image_name[block["content"]] = name
                images[name] = {"url": block["content"], "is_public": True}
            else:
                name = link_to_image_name[block["content"]]
            latex_statement += f"\\img[{name}]{{{name}}}" + "\n\n"

    solution_source: list = RESP["solution"]
    solution_source.remove({"type": "header", "content": "Решение"})
    for block in solution_source:
        if block["type"] == "text":
            block["content"] = block["content"].replace("\n", " ")
            block["content"] = block["content"].replace("\\n", " ")
            block["content"] = block["content"].replace("\r", " ")
            block["content"] = block["content"].replace("\\r", " ")
            latex_solution += block["content"] + "\n\n"
        elif block["type"] == "header":
            block["content"] = block["content"].replace("\n", " ")
            block["content"] = block["content"].replace("\\n", " ")
            block["content"] = block["content"].replace("\r", " ")
            block["content"] = block["content"].replace("\\r", " ")
            latex_solution += f'\\textbf{{{block["content"]}}}' + "\n\n"
        elif block["type"] == "img":
            if link_to_image_name.get(block["content"], None) is None:
                name = f"Рис. {len(link_to_image_name) + 1}"
                link_to_image_name[block["content"]] = name
                images[name] = {"url": block["content"], "is_public": False}
            else:
                name = link_to_image_name[block["content"]]
            latex_solution += f"\\img[{name}]{{{name}}}" + "\n\n"

    return {"statement": latex_statement, "solution": latex_solution, "images": images}


# --> ПАРСЕР ИСТОЧНИКОВ <--
def parse_source_tags(table):
    res = []
    """
    List of:
    "Олимпиада": str (Всероссийская олимпиада школьников)
    "Год": str (2022/23)
    "Класс": str (9)
    "Номер": str (1)
    "Вариант": str (Региональный этап)
    """

    # TODO: БАГИ С 'Олимпиада Эйлера' (на сайте нет деления на отборочный и заключительный)

    tr_header = ""
    for tr in table.findChildren(recursive=False):  # считываем таблицу построчно
        if len(tr.findChildren("td")) == 1:
            tr_header = clearing(tr.findChild().text.lower())
            # пометка про заочный тур Шарыгина
            if (
                len(res)
                and res[-1]["Олимпиада"] == "Олимпиада по геометрии имени И.Ф. Шарыгина"
                and tr_header == "заочный тур"
            ):
                res[-1]["Вариант"] = "Заочный тур"
        elif len(tr.findChildren("td")) == 0:
            continue
        else:
            param, value = (
                clearing(tr.findChildren("td")[0].text.lower()),
                clearing(tr.findChildren("td")[1].text),
            )

            # AND добавляется из-за некрасивого формата 'Белорусских олимпиад'
            if tr_header == "олимпиада" and not (
                len(res)
                and res[-1]["Олимпиада"]
                == "Белорусские республиканские математические олимпиады"
            ):
                # новый источник
                res.append(
                    {"Олимпиада": value, "Год": None, "Класс": None, "Номер": None}
                )
            if len(res) == 0:
                continue

            # определяем, в какой контест нужно положить задачу (если есть несколько вариантов)
            olimp = res[-1]["Олимпиада"]
            if olimp == "Московская математическая олимпиада":  # 1 и 2 тур
                if param == "тур":
                    res[-1]["Вариант"] = f"{value} тур"
            elif (
                olimp == "Турнир городов"
            ):  # Осенний тур, базовый вариант (обрезали класс)
                if param == "вариант":
                    res[-1]["Вариант"] = ",".join(value.split(",")[:2]).capitalize()
                if (
                    tr_header == "тур"
                    and param == "тур"
                    and value.lower() == "устный тур"
                ):
                    res[-1]["Вариант"] = "Устный тур"
            elif olimp == "Турнир им.Ломоносова":
                pass
            elif olimp == "Математический праздник":
                pass
            elif olimp == 'Турнир журнала "Квант"':
                pass
            elif olimp == "Белорусские республиканские математические олимпиады":
                pass
            elif olimp == "Олимпиада по геометрии имени И.Ф. Шарыгина":
                pass
            elif olimp == "Московская устная олимпиада по геометрии":
                pass
            elif olimp == "Московская математическая регата":
                pass
            elif olimp == "Московская устная олимпиада для 6-7 классов":
                pass
            elif olimp == "Окружная олимпиада (Москва)":
                pass
            elif olimp == "Всероссийская олимпиада по математике":  # 4 - рег, 5 - закл
                if tr_header == "этап" and param == "вариант":
                    if value == "4":
                        res[-1]["Вариант"] = "Региональный этап"
                    elif value == "5":
                        res[-1]["Вариант"] = "Заключительный этап"
            elif olimp == "Международная математическая олимпиада":
                pass
            elif olimp == "Олимпиада имени Леонарда Эйлера (для 8 классов)":
                pass
            elif olimp == "Заочная олимпиада по теории вероятностей и статистике":
                pass
            if res[-1].get("Вариант") is None:  # если всё лежит в одном комплекте задач
                res[-1]["Вариант"] = "Задачи олимпиады"

            if tr_header == "задача":  # парсим номер задачи
                _value = ""
                it = 0
                # Хотим преобразовать строку "Задача 7.2" или "1 [8 кл]" к виду "7.2" или "1"
                while it < len(value) and (not value[it].isdigit()):
                    it += 1
                while (it < len(value)) and (value[it].isdigit() or value[it] == "."):
                    _value += value[it]
                    it += 1
                if "." in _value:  # значит, заодно с номером указан класс
                    # Хотим обработать также случаи "1.3." -> 1,3 и "4.06.10.7" -> 10,7
                    _value = [el for el in _value.split(".") if el != ""][-2:]
                    grade, num = _value
                    res[-1]["Класс"] = get_all_numbers(grade)
                    res[-1]["Номер"] = num
                else:  # значит, указан просто номер
                    res[-1]["Номер"] = _value
            if param == "класс":  # здесь без фокусов
                res[-1]["Класс"] = get_all_numbers(value)
            if (
                "класс" in value or "кл]" in value
            ):  # иногда класс спрятан в названии олимпиады или в номере задачи
                sp = value.split()
                for i in range(len(sp)):
                    if sp[i].startswith("класс") or sp[i].startswith("кл]"):
                        res[-1]["Класс"] = get_all_numbers(sp[i - 1])
                        break

            # парсим год олимпиады, используя библиотеку re
            # хотим обрабатывать "2022" -> "2021/22", "2010/11" -> "2010/11", "2005/2006" -> "2005/06"
            for i in range(len(value) - 4, -1, -1):
                if re.match("[1-2][0-9]{3}/[0-9]{2}", value[i : i + 7]):  # паттерн с /
                    res[-1]["Год"] = fix_year(int(value[i : i + 4]) + 1)
                    break
                # паттерн без /
                if re.match("[1-2][0-9]{3}", value[i : i + 4]):
                    res[-1]["Год"] = fix_year(int(value[i : i + 4]))
                    break

    # Сейчас несколько классов лежит в одной карточке (например, 8 и 9)
    # Давайте сделаем для каждого класса свою карточку источника
    res2 = []
    for el in res:
        if el.get("Класс") is None:
            el["Класс"] = [None]
        for grade in el["Класс"]:
            res2.append(dict(el))
            res2[-1]["Класс"] = grade
    return res2


# --> ОСНОВНОЙ ПАРСЕР <--
def parse_func(id):
    soup = get_soup(f"https://problems.ru/view_problem_details_new.php?id={id}", True)

    RESP = dict()
    """
    "name": str
    "statement": str with actual statement in ge0math format
    "solution": str with actual solution in ge0math format
    "images": dict from name (str) to dict with "url": str and "is_public": bool
    "tags": list of
        "topic": str
        "tag": str
    "source": list of
        "Олимпиада": str
        "Год": str
        "Класс": str
        "Номер": str
        "Вариант": str
    """
    RESP["name"] = f"#{id} problems.ru"
    RESP["statement"] = []
    RESP["solution"] = []
    RESP["tags"] = []
    RESP["source"] = []

    themes = soup.findAll("tr", class_="problemdetailssubjecttablecell")
    for tr in themes:
        a = tr.find("a")
        root = parse_theme_preroot(a["href"])
        if root is None:
            root = parse_theme_root(a["href"])
        theme = stripper(a.text)
        RESP["tags"].append({"topic": root, "tag": theme})

    # remove block with author info
    author_div = soup.find("div", class_="catalogueproblemauthorold")
    if author_div is not None:
        authors = [a.text for a in author_div.findAll("a")]
        author_div.decompose()
    else:
        authors = []

    # remove block with source info
    tmp = soup.findAll("h3")
    for i in range(len(tmp)):
        if tmp[i].text == "Источники и прецеденты использования":
            tmp[i].decompose()

    # process source info
    source_table = soup.find("table", class_="problemdetailssourcetable")
    RESP["source"] = parse_source_tags(source_table)
    source_table.decompose()
    soup.find("div", class_="problemdetailssourcetablecontainer").decompose()

    box = soup.find("div", class_="componentboxcontents")
    topics_table = box.find("table", class_="problemdetailscaptiontable")
    topics_table.decompose()

    # parse contents
    tmp = box.findAll("h3")
    for i in range(len(tmp)):
        if i == 0:
            area = "statement"
        else:
            area = "solution"
        RESP[area].append({"type": "header", "content": tmp[i].text})
        ch = tmp[i].nextSibling
        # Check if ch is 'h3' (so we need to break)
        while (ch is not None) and (ch.name != "h3"):
            img = None

            # check if ch contains image
            if ch.name == "img":
                img = ch
            elif not isinstance(ch, bs4.NavigableString):
                img = ch.findChild("img", recursive=True)
            if img is not None:
                RESP[area].append({"type": "img", "content": img["src"]})

            else:
                RESP[area].append({"type": "text", "content": ch.text})

            # cycle over all siblings of tmp[i]
            ch = ch.nextSibling

    if authors is not None:
        for author in authors:
            RESP["tags"].append({"topic": "Автор", "tag": author})

    latex = parse_latex(RESP)
    RESP["statement"] = latex["statement"]
    RESP["solution"] = latex["solution"]
    RESP["images"] = latex["images"]

    return RESP


@parse.route("/parse", methods=["GET"])
def parse_problems():
    id = request.args.get("id")
    return parse_func(id)

@parse.route("/remove_tags", methods=["GET"])
@admin_required
def remove_tags():
    for tag in Tag.query.all():
        db.session.delete(tag)
    for tag_relation in Tag_Relation.query.all():
        db.session.delete(tag_relation)
    db.session.commit()
    return "OK"

@parse.route("/init_topics")
@admin_required
def init_topics():
    for topic in Topic.query.all():
        topic.remove()
    topics = ["Алгебра", "Геометрия", "Комбинаторика", "Теория чисел", "Автор"]
    colors = ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd", "#8c564b"]
    for name, color in zip(topics, colors):
        Topic(name=name, color=color).add()
    db.session.commit()
    return "OK"


def add_tags(problem, tags: [(str, str)]):
    for topic, tag in tags:
        problem.act_add_tag(Tag.add_by_name_and_topic(tag, topic))

def process_tags(problem, tags):
    for tag in tags:
        topic = tag["topic"]
        tagname = tag["tag"]
        add_tags(problem, [topic, tagname])


def process_sources(problem, sources):
    for source in sources:
        variant = source["Вариант"]
        olimpiad_name = source["Олимпиада"]
        year = source["Год"]
        grade = source["Класс"]
        num = int(source["Номер"])

        olimpiad = Olimpiad.query.filter_by(name=olimpiad_name).first()
        if olimpiad is None:
            olimpiad = Olimpiad(name=olimpiad_name)
            olimpiad.short_name = olimpiad_name
            olimpiad.category = ""
            olimpiad.add()
        ov = Olimpiad_Variant.query.filter_by(variant=variant, olimpiad=olimpiad, year=year, grade=grade).first()
        if ov is None:
            ov = Olimpiad_Variant(variant=variant, olimpiad=olimpiad, year=year, grade=grade)
            ov.add()

        contest = None
        if len(ov.contests):
            contest = ov.contests[0]
        else:
            contest = Contest()
            contest.olimpiad_variant = ov
            contest.name = ov.variant
            contest.description = f"""\\textbf{{Контест по задачам прошедшей олимпиады}}\n
            {ov.olimpipad.name}, {ov.year}, {ov.grade}"""
            contest.start_date = datetime.now()
            contest.end_date = contest.start_date
            contest.is_public = True
            contest.rating = "public"
            contest.pool = problem.pool
            contest.add()
        cp = Contest_Problem.query.filter_by(contest=contest, list_index=num).first()
        if cp is None:
            cp = Contest_Problem(contest=contest, problem=problem, list_index=num)
            cp.add()
            print("added contest problem")
            print(cp.list_index)





def process_images(problem, images):
    for key,val in images.items():
        directory = "app/database/attachments/problems"
        src = val["url"]
        is_public = val["is_public"]
        file = requests.get(src).content
        filenames = safe_image_upload([file], directory, 5 * 1024 * 1024)
        filename = filenames[0]
        if filename is None:
            continue
        attachment = Attachment(
            db_folder=directory,
            db_filename=filename,
            short_name=key,
            parent_type=DbParent.fromType(type(problem)),
            parent_id=problem.id,
            other_data={"is_secret": not is_public},
        )
        attachment.add()
        print("added attachment")
        print(attachment.db_filename)


def main_processer(content, pool_hashed_id="I65Y2znSQACd0ki4qvRp"):
    pool = Pool.get_by_hashed_id(pool_hashed_id)
    if pool is None:
        return None
    problem = Problem().add()
    problem.name = content["name"]
    problem.statement = content["statement"]
    problem.solution = content["solution"]
    problem.pool = pool
    problem.save()
    process_tags(problem, content["tags"])
    process_sources(problem, content["source"])
    process_images(problem, content["images"])
