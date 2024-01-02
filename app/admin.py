from .imports import *
from .model_imports import *

admin = Blueprint("admin", __name__)


@admin.route("/admin", methods=["GET", "POST"])
@admin.route("/admin/enter", methods=["GET", "POST"])
@login_required
def enter():
    if AdminPassword.get.first().is_null():
        AdminPassword().add()
    if request.method == "POST":
        password = request.form.get("password")
        if check_password_hash(AdminPassword.get.first().password, password):
            current_user.admin = True
            print("OKadm")
            return redirect("/admin/settings")
        else:
            flash("Неверный админ-пароль", "error")
            return redirect("/admin/enter")
    return render_template("admin/admin_enter.html", title="GeoMath - админка")


@admin.route("/admin/settings", methods=["GET", "POST"])
@admin_required
def settings():
    if request.method == "POST":
        old_password = request.form.get("old_password")
        new_password = request.form.get("new_password")
        confirm_password = request.form.get("confirm_password")
        if confirm_password != new_password:
            flash("Пароли не совпадают", "error")
            return redirect("/admin/settings")
        if check_password_hash(AdminPassword.get.first().password, old_password):
            AdminPassword.get.first().password = generate_password_hash(new_password)

            for user in User.get.all():
                user.admin = False

            flash("Пароль успешно изменен", "success")
            return redirect("/admin/enter")
        else:
            flash("Неверный старый пароль", "error")
            return redirect("/admin/settings")

    return render_template("admin/admin_settings.html", title="GeoMath - настройки")


@admin.route("/admin/problem_moderation", methods=["GET", "POST"])
@admin_required
def moderation():
    if request.method == "POST":
        if request.form.get("accept problem_hashed_id") is not None:
            problem_hashed_id = request.form.get("accept problem_hashed_id")
            problem = Problem.get.by_hashed_id(problem_hashed_id).first()
            problem.moderated = True
        if request.form.get("reject problem_hashed_id") is not None:
            problem_hashed_id = request.form.get("reject problem_hashed_id")
            problem = Problem.get.by_hashed_id(problem_hashed_id).first()
            # db.session.delete(arch)
            problem.is_public = False
    need_to_moderate = Problem.get.by_public(True).by_moderated(False).all()
    return render_template(
        "admin/admin_moderation.html",
        title="GeoMath - модерация",
        need_to_moderate=need_to_moderate,
    )


@admin_required
def show_db(obj):
    result = []
    d = dict()
    d["class_name"] = str(obj)
    result.append(list(d.items()))
    for o in obj.get.all():
        variables = vars(o)
        for var in variables:
            d[var] = variables[var]
        d.pop("_sa_instance_state")
        result.append(
            sorted(
                list(d.items()),
                key=lambda x: 0 if x[0] == "class_name" else 1 if x[0] == "id" else 2,
            )
        )
    return result


@admin_required
def get_class(s):
    if s == "<class 'app.models.User'>":
        return User
    if s == "<class 'app.models.AdminPassword'>":
        return AdminPassword
    if s == "<class 'app.models.Email'>":
        return Email
    if s == "<class 'app.models.Pool'>":
        return Pool
    if s == "<class 'app.models.User_Pool'>":
        return User_Pool
    if s == "<class 'app.models.Problem'>":
        return Problem
    if s == "<class 'app.models.Tag'>":
        return Tag
    if s == "<class 'app.models.Problem_Tag'>":
        return Problem_Tag
    if s == "<class 'app.models.ProblemAttachment'>":
        return ProblemAttachment


@admin.route("/admin/database", methods=["GET", "POST"])
@admin_required
def database():
    if request.method == "POST":
        class_obj = get_class(request.form.get("class_name"))
        id = int(request.form.get("id"))
        obj = class_obj.get.by_id(id).first()
        db.session.delete(obj)
        db.session.commit()
    return render_template(
        "admin/admin_database.html",
        title="GeoMath - top secret",
        tables=[
            show_db(User),
            show_db(AdminPassword),
            show_db(Email),
            show_db(Pool),
            show_db(User_Pool),
            show_db(Problem),
            show_db(Tag),
            show_db(Problem_Tag),
            show_db(ProblemAttachment),
        ],
    )
