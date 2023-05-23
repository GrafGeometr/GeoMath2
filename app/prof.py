from .imports import *
from .model_imports import *

prof = Blueprint('prof', __name__)

@prof.route("/myprofile")
def to_profile():
    if not current_user.is_authenticated:
        return redirect("/login/$myprofile")
    return redirect(f"/profile/{current_user.name}")
    


@prof.route("/profile/<username>")
def profile(username):
    if not current_user.is_authenticated:
        return redirect("/login/$myprofile")
    return render_template("profile_about.html", current_user=current_user)


@prof.route("/profile/<username>/pools")
def profile_pools(username):
    if not current_user.is_authenticated:
        return redirect("/login/$myprofile")
    return render_template("profile_pools.html", current_user=current_user)


@prof.route("/profile/<username>/groups")
def profile_groups(username):
    if not current_user.is_authenticated:
        return redirect("/login/$myprofile")
    return render_template("profile_groups.html", current_user=current_user)

@prof.route("/profile/<username>/settings")
def profile_settings(username):
    if not current_user.is_authenticated:
        return redirect("/login/$myprofile")
    return render_template("profile_settings.html", current_user=current_user)