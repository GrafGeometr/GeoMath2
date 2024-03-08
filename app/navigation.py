from .imports import *
from .model_imports import *

nav = Blueprint("nav", __name__)


@nav.route("/")
@login_required
def index():
    return redirect("/myprofile")


@nav.route("/feed")
@login_required
def feed():
    return render_template("wip/feed.html", current_user=current_user, title="Лента")


@nav.route("/contests")
@login_required
def contests():
    return render_template(
        "wip/contests.html", current_user=current_user, title="Соревнования"
    )


@nav.route("/sheets")
@login_required
def sheets():
    return render_template(
        "wip/sheets.html", current_user=current_user, title="Подборки"
    )


@nav.route("/editor")
@login_required
def editor():
    return render_template(
        "wip/editor.html", current_user=current_user, title="Редактор"
    )
