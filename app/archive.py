from .imports import *
from .model_imports import *

arch = Blueprint('arch', __name__)


@arch.route("/archive/problem/<problem_id>/<filename>")
def show_problem_attachment(problem_id, filename):
    print("TEST", problem_id, filename)
    if not current_user.is_authenticated:
        print("not authenticated")
        return
    problem = Problem.query.filter_by(id = problem_id).first()
    if problem is None:
        print("problem none")
        return
    attachment = ProblemAttachment.query.filter_by(problem_id = problem_id, db_filename = filename).first()
    if attachment is None:
        print("attachment none")
        return
    if (problem.user != current_user) and attachment.locked:
        print("attachment locked")
        return
    try:
        return send_from_directory(os.path.join(basedir, 'database/attachments/problems'), filename, as_attachment=True)
    except Exception as e:
        print(e)

@arch.route("/archive/publish/<int:problem_id>", methods=["POST"])
@login_required
def publish(problem_id):
    problem = Problem.query.filter_by(id = problem_id).first()
    if problem is None:
        return redirect(f"/myprofile")
    pool_hashed_id = problem.pool.hashed_id
    if not current_user.get_pool_relation(problem.pool_id).role.isOwner():
        return redirect(f"/pool/{pool_hashed_id}/problems")
    
    problem.is_public = True

    db.session.commit()

    return redirect(f"/pool/{pool_hashed_id}/problems")



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

@arch.route("/archive/<string:mode>", methods=["POST", "GET"])
@login_required
def archive_search(mode):
    if request.method == "POST":
        tags = request.form.get("tags")
        if tags is not None:
            return redirect(url_for("arch.archive_search", tags=tags, page=1, mode=mode))
        
    
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
    problems = [(p, len([tag for tag in tags if tag in p.get_tag_names()]), len(tags)) for p in problems]
    problems.sort(key = lambda p: p[1], reverse=True)
    

    if mode == "all":
        problems = [problem for problem in problems if problem[0].moderated]
    elif mode == "my":
        problems = [problem for problem in problems if problem[0].user_id == current_user.id]

    print(problems)

    num_of_pages = (len(problems)+problems_per_page-1) // problems_per_page
    problems = problems[(page-1)*problems_per_page : page*problems_per_page]


    pages_to_show = get_correct_page_slice(num_of_pages, 7, page)
    

    return render_template("archive/archive_search.html", mode=mode, problems=problems, pages_to_show=pages_to_show, current_page=page, tags="; ".join(tags), all_tags=sorted(Tag.query.all(), key = lambda t:(t.name).lower()))




@arch.route("/archive/problem/<int:problem_id>", methods=["GET", "POST"])
@login_required
def my_arch(problem_id):
    problem = Problem.query.filter_by(id = problem_id).first()
    if problem is None:
        return redirect("/archive/all")
    if request.method == "POST":
        if problem.user_id == current_user.id:
            if request.form.get("switch_solution_access") is not None:
                problem.show_solution = not problem.show_solution
                db.session.commit()
                return redirect(f"/archive/problem/{problem_id}")
            if request.form.get("add_tag") is not None:
                tag_name = request.form["tag_name"]
                tag = Tag.query.filter_by(name=tag_name).first()
                if (tag is None) and (current_user.admin):
                    tag = Tag(name=tag_name)
                    db.session.add(tag)
                    db.session.commit()
                if Problem_Tag.query.filter_by(problem=problem, tag=tag).first() is None:
                    problem_tag = Problem_Tag(problem=problem, tag=tag)
                    db.session.add(problem_tag)
                    db.session.commit()
                return redirect(f"/archive/problem/{problem_id}")
            if request.form.get("remove_tag") is not None:
                tag_id = request.form.get("remove_tag")
                tag = Tag.query.filter_by(id=tag_id).first()
                if tag is None:
                    return redirect(f"/archive/problem/{problem_id}")
                if Problem_Tag.query.filter_by(problem=problem, tag=tag).first() is not None:
                    db.session.delete(Problem_Tag.query.filter_by(problem=problem, tag=tag).first())
                    db.session.commit()
                return redirect(f"/archive/problem/{problem_id}")
            if request.form.get("delete_problem") is not None:
                db.session.delete(problem)
                db.session.commit()
                return redirect("/archive/my")
            if request.form.get("switch_attachment_access") is not None:
                attachment_id = request.form.get("switch_attachment_access")
                attachment = ProblemAttachment.query.filter_by(id=attachment_id).first()
                if attachment is None:
                    return redirect(f"/archive/problem/{problem_id}")
                if attachment.problem_id != problem_id:
                    return redirect(f"/archive/problem/{problem_id}")
                if Problem_Tag.query.filter_by(problem=problem, tag=tag).first() is not None:
                    db.session.delete(Problem_Tag.query.filter_by(problem=problem, tag=tag).first())
                    db.session.commit()
                return redirect(f"/archive/problem/{problem_id}")
            if request.form.get("delete_problem") is not None:
                db.session.delete(problem)
                db.session.commit()
                return redirect("/archive/my")

    return render_template("archive/archive_problem_template.html", problem=problem, all_tags=sorted(Tag.query.all(), key = lambda t:(t.name).lower()))