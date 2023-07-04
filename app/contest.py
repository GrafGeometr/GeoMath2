from .imports import *
from .model_imports import *

contest = Blueprint('contest', __name__)

@contest.route("/contest/<contest_id>", methods=["GET", "POST"])
@login_required
def contest_mainpage(contest_id):
    contest = Contest.query.filter_by(id=contest_id).first()
    if contest is None:
        flash("Контест с таким id не найден", "danger")
        return redirect("/myprofile")
    if request.method == "POST":
        if request.form.get("register_default") is not None:
            if not (contest.is_public or contest.is_my()):
                flash("Контест не публичный", "danger")
                return redirect(f"/contest/{contest_id}")
            if contest.get_active_cu():
                flash("Вы уже участвуете в контесте", "warning")
                return redirect(f"/contest/{contest_id}")
            cu = Contest_User(contest_id=contest.id, user_id=current_user.id)
    return render_template("contest/contest_mainpage.html", current_contest=contest, title=f"Контест - {contest.name}")