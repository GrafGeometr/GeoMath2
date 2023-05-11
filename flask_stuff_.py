from all_imports_ import *


print("hello")

@route("/")
def index():
    return render_template("base.html", current_user=current_user)


@route("/feed")
def feed():
    return render_template("feed.html", current_user=current_user)


@route("/contests")
def contests():
    return render_template("contests.html", current_user=current_user)


@route("/collections")
def collections():
    return render_template("collections.html", current_user=current_user)


@route("/editor")
def editor():
    return render_template("editor.html", current_user=current_user)















