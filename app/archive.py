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
    arch = Arch(name=problem.name, statement=problem.statement, solution=problem.solution, user=current_user)
    db.session.add(arch)
    db.session.commit()

    db.session.delete(problem)
    db.session.commit()
    return redirect(f"/pool/{pool_hashed_id}/problems")

@arch.route("/archive/all", methods=["GET"])
def all():
    print(Arch.query.filter_by(moderated=True))
    return render_template("archive/archive_all.html", archs=Arch.query.filter_by(moderated=True).all())

@arch.route("/archive/my", methods=["GET"])
def my():
    return render_template("archive/archive_my.html", archs=Arch.query.filter_by(user=current_user))

@arch.route("/archive/my/<int:arch_id>", methods=["GET", "POST"])
def my_arch(arch_id):
    arch = Arch.query.filter_by(id = arch_id).first()
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
            if ArchTag.query.filter_by(arch=arch, tag=tag).first() is None:
                archtag = ArchTag(arch=arch, tag=tag)
                db.session.add(archtag)
                db.session.commit()
            return redirect(f"/archive/my/{arch_id}")
        if request.form.get("remove_tag") is not None:
            tag_id = request.form.get("remove_tag")
            tag = Tag.query.filter_by(id=tag_id).first()
            if tag is None:
                return redirect(f"/archive/my/{arch_id}")
            if ArchTag.query.filter_by(arch=arch, tag=tag).first() is not None:
                db.session.delete(ArchTag.query.filter_by(arch=arch, tag=tag).first())
                db.session.commit()
            return redirect(f"/archive/my/{arch_id}")
        if request.form.get("delete_arch") is not None:
            db.session.delete(arch)
            db.session.commit()
            return redirect("/archive/my")

    return render_template("archive/archive_1arch.html", arch=arch, all_tags=sorted(Tag.query.all(), key = lambda t:(t.name).lower()))