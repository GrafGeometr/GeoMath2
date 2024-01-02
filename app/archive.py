from .imports import *
from .model_imports import *

arch = Blueprint("arch", __name__)


@arch.route("/archive/problem/<problem_hashed_id>/<filename>")
def show_problem_attachment(problem_hashed_id, filename):
    print("TEST", problem_hashed_id, filename)
    if not current_user.is_authenticated:
        print("not authenticated")
        return
    problem = Problem.get.by_hashed_id(problem_hashed_id).first()
    if problem.is_null():
        print("problem none")
        return
    attachment = Attachment.get.by_db_filename(filename).first()
    if not attachment.is_from_parent(problem):
        print("attachment none")
        return
    if attachment.locked:
        print("attachment locked")
        return
    try:
        return send_from_directory(
            os.path.join(basedir, "database/attachments/problems"),
            filename,
            as_attachment=True,
        )
    except Exception as e:
        print(e)


@arch.route("/archive/publish/problem/<problem_hashed_id>", methods=["POST"])
@login_required
def publish_problem(problem_hashed_id):
    problem = Problem.get.by_hashed_id(problem_hashed_id).first()
    if problem.is_null():
        return redirect(f"/myprofile")
    pool_hashed_id = problem.pool.hashed_id
    if not current_user.get_pool_relation(problem.pool_id).role.is_owner():
        return redirect(f"/pool/{pool_hashed_id}/problems")

    if not problem.name:
        flash("Не указано название задачи", "error")
        return redirect(f"/pool/{pool_hashed_id}/problem/{problem.hashed_id}")
    if not problem.statement:
        flash("Не указано условие задачи", "error")
        return redirect(f"/pool/{pool_hashed_id}/problem/{problem.hashed_id}")
    if not problem.solution:
        flash("Не указано решение задачи", "error")
        return redirect(f"/pool/{pool_hashed_id}/problem/{problem.hashed_id}")

    problem.is_public = True

    db.session.commit()
    for user in problem.pool.get_owners():
        Notification.send_to_friends(
            user.name,
            "опубликовал новую задачу",
            f"/archive/problem/{problem.hashed_id}",
            user,
        )

    return redirect(f"/pool/{pool_hashed_id}/problem/{problem.hashed_id}")


@arch.route("/archive/publish/sheet/<sheet_id>", methods=["POST"])
@login_required
def publish_sheet(sheet_id):
    sheet = Sheet.get.by_id(sheet_id).first()
    if sheet.is_null():
        return redirect(f"/myprofile")
    pool_hashed_id = sheet.pool.hashed_id
    if not current_user.get_pool_relation(sheet.pool_id).role.is_owner():
        return redirect(f"/pool/{pool_hashed_id}/sheets")

    if not sheet.name:
        flash("Не указано название подборки", "error")
        return redirect(f"/pool/{pool_hashed_id}/sheet/{sheet.id}")
    if not sheet.text:
        flash("Не указан текст подборки", "error")
        return redirect(f"/pool/{pool_hashed_id}/sheet/{sheet.id}")

    sheet.is_public = True

    db.session.commit()
    for user in sheet.pool.get_owners():
        Notification.send_to_friends(
            user.name, "опубликовал новую подборку", f"/archive/sheet/{sheet.id}", user
        )

    return redirect(f"/pool/{pool_hashed_id}/sheet/{sheet.id}")


@arch.route("/archive/publish/contest/<contest_id>", methods=["POST"])
@login_required
def publish_contest(contest_id):
    contest = Contest.get.by_id(contest_id).first()
    if contest.is_null():
        return redirect(f"/myprofile")
    pool_hashed_id = contest.pool.hashed_id
    if not current_user.get_pool_relation(contest.pool_id).role.is_owner():
        return redirect(f"/pool/{pool_hashed_id}/contests")

    if not contest.name:
        flash("Не указано название контеста", "error")
        return redirect(f"/pool/{pool_hashed_id}/contest/{contest.id}")

    if not contest.description:
        flash("Не указано описание контеста", "error")
        return redirect(f"/pool/{pool_hashed_id}/contest/{contest.id}")

    if contest.start_date > contest.end_date:
        flash("Контест должен начаться раньше, чем закончиться", "error")
        return redirect(f"/pool/{pool_hashed_id}/contest/{contest.id}")

    contest.is_public = True

    db.session.commit()
    for user in contest.pool.get_owners():
        Notification.send_to_friends(
            user.name, "опубликовал новый контест", f"/contest/{contest.id}", user
        )

    return redirect(f"/pool/{pool_hashed_id}/contest/{contest.id}")


def get_correct_page_slice(num_of_pages, len_of_slice, index_of_current_page):
    n = num_of_pages
    k = len_of_slice
    i = index_of_current_page
    print(n, k, i)
    # look how google search works to understand
    # in a nutshell, it returns a slice with len = k, where i is in the middle (except for when i is close to the borders)
    # everything is 1-indexed

    if k >= n:
        return [x for x in range(1, n + 1)]
    half = k // 2
    if i <= half + 1:
        return [x for x in range(1, k + 1)]
    elif n - (i - 1) <= (k - half):
        return [x for x in range(n - k + 1, n + 1)]
    else:
        return [x for x in range(i - half, i + (k - half))]


@arch.route("/archive/problems/<string:username>", methods=["POST", "GET"])
@login_required
def archive_problem_search(username):
    if request.method == "POST":
        tags = request.form.get("tags")
        if tags is not None:
            return redirect(
                url_for(
                    "arch.archive_problem_search", tags=tags, page=1, username=username
                )
            )

    tags = request.args.get("tags")
    page = request.args.get("page")

    if page is None:
        page = 1
    else:
        page = int(page)

    if tags is None or tags == "":
        tags = []
    else:
        tmp = tags.split(";")
        tags = []
        for t in tmp:
            if t.strip() != "":
                tags.append(t.strip())

    from app.utils_and_functions.usefull_functions import get_string_hash

    tags_hashes = sorted([get_string_hash(tag.lower()) for tag in tags])
    tags_count = len(tags)

    objs_per_page = 10

    tag_id_to_hash = {}
    for t in Tag.get.all():
        tag_id_to_hash[t.id] = t.get_hash()

    obj_id_to_cnt = {}
    for tr in TagRelation.get.all():
        obj_id = tr.parent_id
        tag_hash = tag_id_to_hash[tr.tag_id]
        idx = bisect.bisect_left(tags_hashes, tag_hash)
        if idx != len(tags_hashes) and tags_hashes[idx] == tag_hash:
            obj_id_to_cnt[obj_id] = obj_id_to_cnt.get(obj_id, 0) + 1

    objs = Problem.get.all()  # Problem | Sheet | Contest
    user = User.get.by_name(username).first()
    if user.is_not_null():
        objs = [obj for obj in objs if obj.is_my(user)]

    resulting_objs = []

    for obj in objs:
        if not obj.is_archived():
            continue
        cnt = obj_id_to_cnt.get(obj.id, 0)
        resulting_objs.append(
            (obj, cnt, tags_count, (obj.total_likes + 1) / (obj.total_dislikes + 1))
        )

    resulting_objs.sort(key=lambda o: (o[1], o[3]), reverse=True)

    # problems = [(p, len([tag for tag in tags if tag in p.get_tag_names()]), len(tags), p.total_likes) for p in problems if p.is_statement_available()]
    # problems.sort(key = lambda p: (p[1], p[3]), reverse=True)

    # if username == "all":
    # problems = [problem for problem in problems if problem[0].usernamerated]
    num_of_pages = (len(resulting_objs) + objs_per_page - 1) // objs_per_page
    objs = resulting_objs[(page - 1) * objs_per_page : page * objs_per_page]

    pages_to_show = get_correct_page_slice(num_of_pages, 7, page)

    return render_template(
        "archive/archive_search_problems.html",
        title="Поиск задач",
        username=username,
        problems=objs,
        pages_to_show=pages_to_show,
        current_page=page,
        tags="; ".join(tags),
        all_tags=sorted(Tag.get.all(), key=lambda t: (t.name).lower()),
    )


@arch.route("/archive/sheets/<string:username>", methods=["POST", "GET"])
@login_required
def archive_sheet_search(username):
    if request.method == "POST":
        tags = request.form.get("tags")
        if tags is not None:
            return redirect(
                url_for(
                    "arch.archive_sheet_search", tags=tags, page=1, username=username
                )
            )

    tags = request.args.get("tags")
    page = request.args.get("page")

    if page is None:
        page = 1
    else:
        page = int(page)

    if tags is None or tags == "":
        tags = []
    else:
        tmp = tags.split(";")
        tags = []
        for t in tmp:
            if t.strip() != "":
                tags.append(t.strip())

    from app.utils_and_functions.usefull_functions import get_string_hash

    tags_hashes = sorted([get_string_hash(tag.lower()) for tag in tags])
    tags_count = len(tags)

    objs_per_page = 10

    tag_id_to_hash = {}
    for t in Tag.get.all():
        tag_id_to_hash[t.id] = t.get_hash()

    obj_id_to_cnt = {}
    for tr in TagRelation.get.all():
        obj_id = tr.parent_id
        tag_hash = tag_id_to_hash[tr.tag_id]
        idx = bisect.bisect_left(tags_hashes, tag_hash)
        if idx != len(tags_hashes) and tags_hashes[idx] == tag_hash:
            obj_id_to_cnt[obj_id] = obj_id_to_cnt.get(obj_id, 0) + 1

    objs = Sheet.get.all()  # Problem | Sheet | Contest
    user = User.get.by_name(username).first()
    if user.is_not_null():
        objs = [obj for obj in objs if obj.is_my(user)]

    resulting_objs = []

    for obj in objs:
        if not obj.is_archived():
            continue
        cnt = obj_id_to_cnt.get(obj.id, 0)
        resulting_objs.append(
            (obj, cnt, tags_count, (obj.total_likes + 1) / (obj.total_dislikes + 1))
        )

    resulting_objs.sort(key=lambda o: (o[1], o[3]), reverse=True)

    # problems = [(p, len([tag for tag in tags if tag in p.get_tag_names()]), len(tags), p.total_likes) for p in problems if p.is_statement_available()]
    # problems.sort(key = lambda p: (p[1], p[3]), reverse=True)

    # if username == "all":
    # problems = [problem for problem in problems if problem[0].usernamerated]

    num_of_pages = (len(resulting_objs) + objs_per_page - 1) // objs_per_page
    objs = resulting_objs[(page - 1) * objs_per_page : page * objs_per_page]

    pages_to_show = get_correct_page_slice(num_of_pages, 7, page)

    return render_template(
        "archive/archive_search_sheets.html",
        title="Поиск подборок",
        username=username,
        sheets=objs,
        pages_to_show=pages_to_show,
        current_page=page,
        tags="; ".join(tags),
        all_tags=sorted(Tag.get.all(), key=lambda t: (t.name).lower()),
    )


@arch.route("/archive/contests/<string:username>", methods=["POST", "GET"])
@login_required
def archive_contest_search(username):
    if request.method == "POST":
        tags = request.form.get("tags")
        if tags is not None:
            return redirect(
                url_for(
                    "arch.archive_contest_search", tags=tags, page=1, username=username
                )
            )

    tags = request.args.get("tags")
    page = request.args.get("page")

    if page is None:
        page = 1
    else:
        page = int(page)

    if tags is None or tags == "":
        tags = []
    else:
        tmp = tags.split(";")
        tags = []
        for t in tmp:
            if t.strip() != "":
                tags.append(t.strip())

    from app.utils_and_functions.usefull_functions import get_string_hash

    tags_hashes = sorted([get_string_hash(tag.lower()) for tag in tags])
    tags_count = len(tags)

    objs_per_page = 10

    tag_id_to_hash = {}
    for t in Tag.get.all():
        tag_id_to_hash[t.id] = t.get_hash()

    obj_id_to_cnt = {}
    for tr in TagRelation.get.all():
        obj_id = tr.parent_id
        tag_hash = tag_id_to_hash[tr.tag_id]
        idx = bisect.bisect_left(tags_hashes, tag_hash)
        if idx != len(tags_hashes) and tags_hashes[idx] == tag_hash:
            obj_id_to_cnt[obj_id] = obj_id_to_cnt.get(obj_id, 0) + 1

    objs = Contest.get.all()  # Problem | Sheet | Contest
    user = User.get.by_name(username).first()
    if user.is_not_null():
        objs = [obj for obj in objs if obj.is_my(user)]

    resulting_objs = []

    for obj in objs:
        if not obj.is_archived():
            continue
        cnt = obj_id_to_cnt.get(obj.id, 0)
        resulting_objs.append(
            (obj, cnt, tags_count, (obj.total_likes + 1) / (obj.total_dislikes + 1))
        )

    resulting_objs.sort(key=lambda o: (o[1], o[3]), reverse=True)

    # problems = [(p, len([tag for tag in tags if tag in p.get_tag_names()]), len(tags), p.total_likes) for p in problems if p.is_statement_available()]
    # problems.sort(key = lambda p: (p[1], p[3]), reverse=True)

    # if username == "all":
    # problems = [problem for problem in problems if problem[0].usernamerated]

    num_of_pages = (len(resulting_objs) + objs_per_page - 1) // objs_per_page
    objs = resulting_objs[(page - 1) * objs_per_page : page * objs_per_page]

    pages_to_show = get_correct_page_slice(num_of_pages, 7, page)

    return render_template(
        "archive/archive_search_contests.html",
        title="Поиск контестов",
        username=username,
        contests=objs,
        pages_to_show=pages_to_show,
        current_page=page,
        tags="; ".join(tags),
        all_tags=sorted(Tag.get.all(), key=lambda t: (t.name).lower()),
    )


@arch.route("/archive/problem/<problem_hashed_id>")
@login_required
def arch_problem(problem_hashed_id):
    problem = Problem.get.by_hashed_id(problem_hashed_id).first()
    if (problem.is_null()) or (not problem.is_statement_available()):
        return redirect("/archive/problems/all")
    return render_template(
        "archive/archive_problem_template.html",
        current_problem=problem,
        title=f"Архив - {problem.name}",
    )


@arch.route("/archive/sheet/<sheet_id>")
@login_required
def arch_sheet(sheet_id):
    sheet = Sheet.get.by_id(sheet_id).first()
    if (sheet.is_null()) or (not sheet.is_text_available()):
        return redirect("/archive/sheets/all")
    return render_template(
        "archive/archive_sheet_template.html",
        current_sheet=sheet,
        title=f"Архив - {sheet.name}",
    )
