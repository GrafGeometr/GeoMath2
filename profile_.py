from all_imports_ import *


@login_required
@app.route("/myprofile")
def to_profile():
    if not current_user.is_authenticated:
        return redirect("/login/$myprofile")
    return redirect(f"/profile/{current_user.name}")
    

@login_required
@app.route("/profile/<username>")
def profile(username):
    if not current_user.is_authenticated:
        return redirect("/login/$myprofile")
    
    db_sess = db_session.create_session()

    user = get_current_user(db_sess)


    return render_template("profile_about.html", current_user=user)

@login_required
@app.route("/profile/<username>/pools")
def profile_pools(username):
    if not current_user.is_authenticated:
        return redirect("/login/$myprofile")
    
    db_sess = db_session.create_session()

    user = get_current_user(db_sess)


    return render_template("profile_pools.html", current_user=user)

@login_required
@app.route("/profile/<username>/groups")
def profile_groups(username):
    if not current_user.is_authenticated:
        return redirect("/login/$myprofile")
    
    db_sess = db_session.create_session()

    user = get_current_user(db_sess)


    return render_template("profile_groups.html", current_user=user)

@login_required
@app.route("/profile/<username>/settings")
def profile_settings(username):
    if not current_user.is_authenticated:
        return redirect("/login/$myprofile")
    
    db_sess = db_session.create_session()

    user = get_current_user(db_sess)


    return render_template("profile_settings.html", current_user=user)