from .imports import *
from .model_imports import *

nav = Blueprint('nav', __name__)

@nav.route("/")
@go_to_login("/")
def index():
    return render_template("base.html", current_user=current_user)


@nav.route("/feed")
@go_to_login("/feed")
def feed():
    return render_template("feed.html", current_user=current_user)


@nav.route("/contests")
@go_to_login("/contests")
def contests():
    return render_template("contests.html", current_user=current_user)


@nav.route("/collections")
@go_to_login("/collections")
def collections():
    return render_template("collections.html", current_user=current_user)


@nav.route("/editor")
@go_to_login("/editor")
def editor():
    return render_template("editor.html", current_user=current_user)















