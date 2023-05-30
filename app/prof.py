# -*- coding: utf-8 -*-
from .imports import *
from .model_imports import *

prof = Blueprint('prof', __name__)

@prof.route("/myprofile")
@login_required
def to_profile():
    return redirect(f"/profile/{current_user.name}")
    


@prof.route("/profile/<username>")
@login_required
def profile(username):
    return render_template("profile/profile_about.html", title="Мой профиль")


@prof.route("/profile/<username>/pools")
@login_required
def profile_pools(username):
    return render_template("profile/profile_pools.html", title="Мои пулы")


@prof.route("/profile/<username>/groups")
@login_required
def profile_groups(username):
    return render_template("profile/profile_groups.html", title="Мои кружки")

@prof.route("/profile/<username>/settings")
@login_required
def profile_settings(username):
    return render_template("profile/profile_settings.html", title="Настройки")