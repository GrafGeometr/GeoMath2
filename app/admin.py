from .imports import *
from .model_imports import *

admin = Blueprint('admin', __name__)

@admin.route("/admin", methods=["GET", "POST"])
@admin.route("/admin/enter", methods=["GET", "POST"])
@login_required
def enter():
    if AdminPassword.query.first() is None:
        db.session.add(AdminPassword())
        db.session.commit()
    if request.method == "POST":
        password = request.form.get("password")
        if check_password_hash(AdminPassword.query.first().password, password):
            current_user.admin = True
            db.session.commit()
            print("OKadm")
            return redirect("/admin/settings")
        else:
            flash("Неверный админ-пароль", "danger")
            return redirect("/admin/enter")
    return render_template("admin/admin_enter.html", title="GeoMath - админка")

@admin.route("/admin/settings", methods=["GET", "POST"])
@admin_required
def settings():
    if request.method == "POST":
        old_password = request.form.get("old_password")
        new_password = request.form.get("new_password")
        if check_password_hash(AdminPassword.query.first().password, old_password):
            AdminPassword.query.first().password = generate_password_hash(new_password)
            db.session.commit()

            for user in User.query.all():
                user.admin = False
            db.session.commit()

            flash("Пароль успешно изменен", "success")
            return redirect("/admin/enter")
        else:
            flash("Неверный старый пароль", "danger")
            return redirect("/admin/settings")

    return render_template("admin/admin_settings.html", title="GeoMath - настройки")

@admin.route("/admin/moderation", methods=["GET", "POST"])
@admin_required
def moderation():
    if request.method == "POST":
        if request.form.get("accept arch_id") is not None:
            arch_id = request.form.get("accept arch_id")
            arch = Arch.query.filter_by(id = arch_id).first()
            arch.moderated = True
            db.session.commit()
        if request.form.get("reject arch_id") is not None:
            arch_id = request.form.get("reject arch_id")
            arch = Arch.query.filter_by(id = arch_id).first()
            db.session.delete(arch)
            db.session.commit()
    need_to_moderate = Arch.query.filter_by(moderated = False).all()
    return render_template("admin/admin_moderation.html", title="GeoMath - модерация", need_to_moderate = need_to_moderate)