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


    return render_template("profile.html", current_user=user)