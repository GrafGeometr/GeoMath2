from .imports import *
from .model_imports import *

arch = Blueprint('arch', __name__)


@arch.route("/archive/problem/<problem_hashed_id>/<filename>")
def show_problem_attachment(problem_hashed_id, filename):
    print("TEST", problem_hashed_id, filename)
    if not current_user.is_authenticated:
        print("not authenticated")
        return
    problem = Problem.query.filter_by(hashed_id = problem_hashed_id).first()
    if problem is None:
        print("problem none")
        return
    attachment = Attachment.get_by_db_filename(filename)
    if not attachment.is_from_parent(problem):
        print("attachment none")
        return
    if attachment.locked:
        print("attachment locked")
        return
    try:
        return send_from_directory(os.path.join(basedir, 'database/attachments/problems'), filename, as_attachment=True)
    except Exception as e:
        print(e)

@arch.route("/archive/publish/problem/<problem_hashed_id>", methods=["POST"])
@login_required
def publish_problem(problem_hashed_id):
    problem = Problem.query.filter_by(hashed_id = problem_hashed_id).first()
    if problem is None:
        return redirect(f"/myprofile")
    pool_hashed_id = problem.pool.hashed_id
    if not current_user.get_pool_relation(problem.pool_id).role.isOwner():
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

    return redirect(f"/pool/{pool_hashed_id}/problem/{problem.hashed_id}")

@arch.route("/archive/publish/sheet/<sheet_id>", methods=["POST"])
@login_required
def publish_sheet(sheet_id):
    sheet = Sheet.query.filter_by(id = sheet_id).first()
    if sheet is None:
        return redirect(f"/myprofile")
    pool_hashed_id = sheet.pool.hashed_id
    if not current_user.get_pool_relation(sheet.pool_id).role.isOwner():
        return redirect(f"/pool/{pool_hashed_id}/sheets")
    
    if not sheet.name:
        flash("Не указано название подборки", "error")
        return redirect(f"/pool/{pool_hashed_id}/sheet/{sheet.id}")
    if not sheet.text:
        flash("Не указан текст подборки", "error")
        return redirect(f"/pool/{pool_hashed_id}/sheet/{sheet.id}")

    sheet.is_public = True

    db.session.commit()

    return redirect(f"/pool/{pool_hashed_id}/sheet/{sheet.id}")

@arch.route("/archive/publish/contest/<contest_id>", methods=["POST"])
@login_required
def publish_contest(contest_id):
    contest = Contest.query.filter_by(id = contest_id).first()
    if contest is None:
        return redirect(f"/myprofile")
    pool_hashed_id = contest.pool.hashed_id
    if not current_user.get_pool_relation(contest.pool_id).role.isOwner():
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
        return [x for x in range(1, n+1)]
    half = k // 2
    if i <= half + 1:
        return [x for x in range(1, k+1)]
    elif n - (i-1) <= (k-half):
        return [x for x in range(n-k+1, n+1)]
    else:
        return [x for x in range(i-half, i+(k-half))]

@arch.route("/archive/problems/<string:username>", methods=["POST", "GET"])
@login_required
def archive_problem_search(username):
    if request.method == "POST":
        tags = request.form.get("tags")
        if tags is not None:
            return redirect(url_for("arch.archive_problem_search", tags=tags, page=1, username=username))
        
    
    tags = request.args.get("tags")
    page = request.args.get("page")

    if page is None:
        page = 1
    else:
        page = int(page)
    
    if tags is None or tags == "":
        tags = []
    else:
        tags = list(map(lambda x: x.strip() , tags.split(";")))

    from app.utils_and_functions.usefull_functions import get_string_hash

    tags_hashes = sorted([get_string_hash(tag.lower()) for tag in tags])
    tags_count = len(tags)

    problems_per_page = 10

    tag_id_to_hash = {}
    for t in Tag.query.all():
        tag_id_to_hash[t.id] = t.get_hash()

    problem_id_to_cnt = {}
    for tr in Tag_Relation.query.all():
        problem_id = tr.parent_id
        tag_hash = tag_id_to_hash[tr.tag_id]
        idx = bisect.bisect_left(tags_hashes, tag_hash)
        if idx != len(tags_hashes) and tags_hashes[idx] == tag_hash:
            problem_id_to_cnt[problem_id] = problem_id_to_cnt.get(problem_id, 0) + 1


    problems = Problem.query.all()
    user = User.query.filter_by(name=username).first()
    if user is not None:
        problems = [problem for problem in problems if problem.is_my(user)]

    resulting_problems = []

    for problem in problems:
        if not problem.is_statement_available():
            continue
        cnt = problem_id_to_cnt[problem.id]
        resulting_problems.append((problem, cnt, tags_count, problem.total_likes))

    resulting_problems.sort(key = lambda p: (p[1], p[3]), reverse=True)

    # problems = [(p, len([tag for tag in tags if tag in p.get_tag_names()]), len(tags), p.total_likes) for p in problems if p.is_statement_available()]
    # problems.sort(key = lambda p: (p[1], p[3]), reverse=True)
    

    #if username == "all":
        #problems = [problem for problem in problems if problem[0].usernamerated]
    


    num_of_pages = (len(problems)+problems_per_page-1) // problems_per_page
    problems = resulting_problems[(page-1)*problems_per_page : page*problems_per_page]


    pages_to_show = get_correct_page_slice(num_of_pages, 7, page)
    

    return render_template("archive/archive_search_problems.html", title="Поиск задач", username=username, problems=problems, pages_to_show=pages_to_show, current_page=page, tags="; ".join(tags), all_tags=sorted(Tag.query.all(), key = lambda t:(t.name).lower()))

@arch.route("/archive/sheets/<string:username>", methods=["POST", "GET"])
@login_required
def archive_sheet_search(username):
    if request.method == "POST":
        tags = request.form.get("tags")
        if tags is not None:
            return redirect(url_for("arch.archive_sheet_search", tags=tags, page=1, username=username))
        
    
    tags = request.args.get("tags")
    page = request.args.get("page")

    if page is None:
        page = 1
    else:
        page = int(page)
    
    if tags is None or tags == "":
        tags = []
    else:
        tags = list(map(lambda x: x.strip() , tags.split(";")))


    tags = list(set(tags))
    print(tags)
    print(page)

    sheets_per_page = 10


    sheets = Sheet.query.all()
    sheets = [(s, len([tag for tag in tags if tag in s.get_tag_names()]), len(tags), s.total_likes) for s in sheets if s.is_text_available()]
    sheets.sort(key = lambda s: (s[1], s[3]), reverse=True)
    

    #if username == "all":
        #problems = [problem for problem in problems if problem[0].usernamerated]
    user = User.query.filter_by(name=username).first()
    if user is not None:
        sheets = [sheet for sheet in sheets if sheet[0].is_my(user)]


    num_of_pages = (len(sheets)+sheets_per_page-1) // sheets_per_page
    sheets = sheets[(page-1)*sheets_per_page : page*sheets_per_page]


    pages_to_show = get_correct_page_slice(num_of_pages, 7, page)
    
    print(sheets)

    return render_template("archive/archive_search_sheets.html", title="Поиск подборок", username=username, sheets=sheets, pages_to_show=pages_to_show, current_page=page, tags="; ".join(tags), all_tags=sorted(Tag.query.all(), key = lambda t:(t.name).lower()))



@arch.route("/archive/contests/<string:username>", methods=["POST", "GET"])
@login_required
def archive_contest_search(username):
    if request.method == "POST":
        tags = request.form.get("tags")
        if tags is not None:
            return redirect(url_for("arch.archive_contest_search", tags=tags, page=1, username=username))
        
    
    tags = request.args.get("tags")
    page = request.args.get("page")

    if page is None:
        page = 1
    else:
        page = int(page)
    
    if tags is None or tags == "":
        tags = []
    else:
        tags = list(map(lambda x: x.strip() , tags.split(";")))


    tags = list(set(tags))
    print(tags)
    print(page)

    contests_per_page = 10


    contests = Contest.query.all()
    contests = [(c, len([tag for tag in tags if tag in c.get_tag_names()]), len(tags), c.total_likes) for c in contests if c.is_description_available()]
    contests.sort(key = lambda c: (c[1], c[3]), reverse=True)
    

    #if username == "all":
        #problems = [problem for problem in problems if problem[0].usernamerated]
    user = User.query.filter_by(name=username).first()
    if user is not None:
        contests = [contest for contest in contests if contest[0].is_my(user)]


    num_of_pages = (len(contests)+contests_per_page-1) // contests_per_page
    contests = contests[(page-1)*contests_per_page : page*contests_per_page]


    pages_to_show = get_correct_page_slice(num_of_pages, 7, page)
    

    return render_template("archive/archive_search_contests.html", title="Поиск контестов", username=username, contests=contests, pages_to_show=pages_to_show, current_page=page, tags="; ".join(tags), all_tags=sorted(Tag.query.all(), key = lambda t:(t.name).lower()))

@arch.route("/archive/problem/<problem_hashed_id>")
@login_required
def arch_problem(problem_hashed_id):
    problem = Problem.query.filter_by(hashed_id = problem_hashed_id).first()
    if (problem is None) or (not problem.is_statement_available()):
        return redirect("/archive/problems/all")
    return render_template(
        "archive/archive_problem_template.html",
        current_problem=problem,
        title=f"Архив - {problem.name}",
    )

@arch.route("/archive/sheet/<sheet_id>")
@login_required
def arch_sheet(sheet_id):
    sheet = Sheet.query.filter_by(id = sheet_id).first()
    if (sheet is None) or (not sheet.is_text_available()):
        return redirect("/archive/sheets/all")
    return render_template(
        "archive/archive_sheet_template.html",
        current_sheet=sheet,
        title=f"Архив - {sheet.name}",
    )