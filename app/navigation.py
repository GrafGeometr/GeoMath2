from .imports import *
from .model_imports import *

nav = Blueprint('nav', __name__)

@nav.route("/")
@login_required
def index():
    return render_template("base.html", current_user=current_user)


@nav.route("/feed")
@login_required
def feed():
    return render_template("feed.html", current_user=current_user)


@nav.route("/contests")
@login_required
def contests():
    return render_template("contests.html", current_user=current_user)


@nav.route("/collections")
@login_required
def collections():
    return render_template("collections.html", current_user=current_user)


@nav.route("/editor")
@login_required
def editor():
    return render_template("editor.html", current_user=current_user)















