from .imports import *
from .model_imports import *

arch = Blueprint('arch', __name__)

@arch.route("/archive/publish/<int:problem_id>", methods=["POST"])
def publish(problem_id):
    problem = Problem.query.filter_by(id = problem_id).first()
    if problem is None:
        return redirect(f"/myprofile")
    pool_hashed_id = problem.pool.hashed_id
    if not current_user.get_pool_relation(problem.pool_id).role.isOwner():
        return redirect(f"/pool/{pool_hashed_id}/problems")
    

    pool_hashed_id = problem.pool.hashed_id
    arch = ArchivedProblem(name=problem.name, statement=problem.statement, solution=problem.solution, user=current_user)
    db.session.add(arch)
    db.session.commit()

    db.session.delete(problem)
    db.session.commit()
    return redirect(f"/pool/{pool_hashed_id}/problems")

# @arch.route("/archive/all", methods=["GET"])
# def all():
#     print(Arch.query.filter_by(moderated=True))
#     return render_template("archive/archive_all.html", archs=Arch.query.filter_by(moderated=True).all())

@arch.route("/archive/all", methods=["POST", "GET"])
def archive_search():
    if request.method == "POST":
        tags = request.form.get("tags")
        if tags is not None:
            return redirect(url_for("arch.archive_search", tags=tags, page=0))
        
    
    tags = request.args.get("tags")
    page = request.args.get("page")

    if page is None:
        page = 0
    else:
        page = int(page)
    
    if tags is None or tags == "":
        tags = []
    else:
        tags = list(map(lambda x: x.strip() , tags.split(";")))

    print(tags)
    print(page)

    problems_per_page = 10

    if len(tags) == 0:
        # no tags, show all
        problems = ArchivedProblem.query.filter_by(moderated=True).all()
    else:
        problems = [problem for problem in ArchivedProblem.query.filter_by(moderated=True).all() if any(tag.name in tags for tag in problem.get_tags())]
    
    total_pages = (len(problems)+problems_per_page-1) // problems_per_page
    problems = problems[page*problems_per_page:(page+1)*problems_per_page]

    pages_to_show1 = [x for x in range(0, total_pages) if x < 3 or x >= total_pages - 3 or abs(x - page) <= 3]
    pages_to_show = []
    for i in range(len(pages_to_show1)):
        pages_to_show.append(pages_to_show1[i])
        if i>=1 and pages_to_show1[i] != pages_to_show1[i-1] + 1:
            pages_to_show.append("...")

    return render_template("archive/archive_search.html", archs=problems, pages_to_show=pages_to_show, current_page=page, tags=";".join(tags), all_tags=sorted(Tag.query.all(), key = lambda t:(t.name).lower()))



@arch.route("/archive/my", methods=["GET"])
def my():
    return render_template("archive/archive_my.html", archs=ArchivedProblem.query.filter_by(user=current_user))

@arch.route("/archive/my/<int:arch_id>", methods=["GET", "POST"])
def my_arch(arch_id):
    arch = ArchivedProblem.query.filter_by(id = arch_id).first()
    if arch is None:
        return redirect("/archive/my")
    if arch.user != current_user:
        return redirect("/archive/my")
    if request.method == "POST":
        if request.form.get("switch_solution_access") is not None:
            arch.show_solution = not arch.show_solution
            db.session.commit()
            return redirect(f"/archive/my/{arch_id}")
        if request.form.get("add_tag") is not None:
            tag_name = request.form["tag_name"]
            tag = Tag.query.filter_by(name=tag_name).first()
            if (tag is None) and (current_user.admin):
                tag = Tag(name=tag_name)
                db.session.add(tag)
                db.session.commit()
            if ArchivedProblem_Tag.query.filter_by(arch=arch, tag=tag).first() is None:
                archtag = ArchivedProblem_Tag(arch=arch, tag=tag)
                db.session.add(archtag)
                db.session.commit()
            return redirect(f"/archive/my/{arch_id}")
        if request.form.get("remove_tag") is not None:
            tag_id = request.form.get("remove_tag")
            tag = Tag.query.filter_by(id=tag_id).first()
            if tag is None:
                return redirect(f"/archive/my/{arch_id}")
            if ArchivedProblem_Tag.query.filter_by(arch=arch, tag=tag).first() is not None:
                db.session.delete(ArchivedProblem_Tag.query.filter_by(arch=arch, tag=tag).first())
                db.session.commit()
            return redirect(f"/archive/my/{arch_id}")
        if request.form.get("delete_arch") is not None:
            db.session.delete(arch)
            db.session.commit()
            return redirect("/archive/my")

    return render_template("archive/archive_1arch.html", arch=arch, all_tags=sorted(Tag.query.all(), key = lambda t:(t.name).lower()))