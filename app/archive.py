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
    attachment = Attachment.query.filter_by(parent_type="Problem", parent_id = problem.id, db_filename = filename).first()
    if attachment is None:
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
        flash("Не указано название задачи", "danger")
        return redirect(f"/pool/{pool_hashed_id}/problem/{problem.hashed_id}")
    if not problem.statement:
        flash("Не указано условие задачи", "danger")
        return redirect(f"/pool/{pool_hashed_id}/problem/{problem.hashed_id}")
    if not problem.solution:
        flash("Не указано решение задачи", "danger")
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
        return redirect(f"/pool/{pool_hashed_id}/problems")
    
    if not sheet.name:
        flash("Не указано название подборки", "danger")
        return redirect(f"/pool/{pool_hashed_id}/sheet/{sheet.id}")
    if not sheet.text:
        flash("Не указан текст подборки", "danger")
        return redirect(f"/pool/{pool_hashed_id}/sheet/{sheet.id}")

    sheet.is_public = True

    db.session.commit()

    return redirect(f"/pool/{pool_hashed_id}/sheet/{sheet.id}")



def get_correct_page_slice(num_of_pages, len_of_slice, index_of_current_page):
    n = num_of_pages
    k = len_of_slice
    i = index_of_current_page
    print(n, k, i)
    # look how google search works to understand
    # in a nutshell, it returns a slice with len = k, where i is the middle (except for when i is close to the borders)
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

@arch.route("/archive/problems/<string:mode>", methods=["POST", "GET"])
@login_required
def archive_problem_search(mode):
    if request.method == "POST":
        tags = request.form.get("tags")
        if tags is not None:
            return redirect(url_for("arch.archive_problem_search", tags=tags, page=1, mode=mode))
        
    
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

    problems_per_page = 10


    problems = Problem.query.all()
    problems = [(p, len([tag for tag in tags if tag in p.get_tag_names()]), len(tags)) for p in problems if p.is_statement_available()]
    problems.sort(key = lambda p: p[1], reverse=True)
    

    #if mode == "all":
        #problems = [problem for problem in problems if problem[0].moderated]
    if mode == "my":
        problems = [problem for problem in problems if problem[0].is_my()]


    num_of_pages = (len(problems)+problems_per_page-1) // problems_per_page
    problems = problems[(page-1)*problems_per_page : page*problems_per_page]


    pages_to_show = get_correct_page_slice(num_of_pages, 7, page)
    

    return render_template("archive/archive_search_problems.html", mode=mode, problems=problems, pages_to_show=pages_to_show, current_page=page, tags="; ".join(tags), all_tags=sorted(Tag.query.all(), key = lambda t:(t.name).lower()))

@arch.route("/archive/sheets/<string:mode>", methods=["POST", "GET"])
@login_required
def archive_sheet_search(mode):
    if request.method == "POST":
        tags = request.form.get("tags")
        if tags is not None:
            return redirect(url_for("arch.archive_sheet_search", tags=tags, page=1, mode=mode))
        
    
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
    sheets = [(s, len([tag for tag in tags if tag in s.get_tag_names()]), len(tags)) for s in sheets if s.is_text_available()]
    sheets.sort(key = lambda s: s[1], reverse=True)
    

    #if mode == "all":
        #problems = [problem for problem in problems if problem[0].moderated]
    if mode == "my":
        sheets = [sheet for sheet in sheets if sheet[0].is_my()]


    num_of_pages = (len(sheets)+sheets_per_page-1) // sheets_per_page
    sheets = sheets[(page-1)*sheets_per_page : page*sheets_per_page]


    pages_to_show = get_correct_page_slice(num_of_pages, 7, page)
    
    print(sheets)

    return render_template("archive/archive_search_sheets.html", mode=mode, sheets=sheets, pages_to_show=pages_to_show, current_page=page, tags="; ".join(tags), all_tags=sorted(Tag.query.all(), key = lambda t:(t.name).lower()))



@arch.route("/archive/problem/<problem_hashed_id>")
@login_required
def arch_problem(problem_hashed_id):
    problem = Problem.query.filter_by(hashed_id = problem_hashed_id).first()
    if problem is None:
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
    if sheet is None:
        return redirect("/archive/sheets/all")
    return render_template(
        "archive/archive_sheet_template.html",
        current_sheet=sheet,
        title=f"Архив - {sheet.name}",
    )