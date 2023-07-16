from .imports import *
from .model_imports import *

prof = Blueprint('prof', __name__)



@prof.route("/show_profile_pic/<path:filename>")
def show_profile_pic(filename):
    print(filename)
    try:
        return send_from_directory(os.path.join(basedir, 'database/profile_pics'), filename, as_attachment=True)
    except Exception as e:
        print(e)

@prof.route("/myprofile")
@login_required
def to_profile():
    return redirect(f"/profile/user/{current_user.name}")
    

def squarify(d, f):
    path = os.path.join(d, f)
    img = Image.open(path)
    x, y = img.size
    if x > y:
        img = img.crop(((x-y)//2, 0, (x+y)//2, y))
    else:
        img = img.crop((0, (y-x)//2, x, (y+x)//2))
    img.save(path)


@prof.route("/profile/user/<username>", methods=["GET", "POST"])
def profile(username):
    user = User.query.filter_by(name = username).first()
    if user is None:
        flash("Пользователь не найден", "error")
        return redirect("/myprofile")
    if request.method == "POST":
        if user.name != current_user.name:
            return redirect(f"/profile/user/{user.name}")
        if request.form.get("update_profile_pic") is not None:
            directory = 'app/database/profile_pics'
            file = request.files.get("profile_pic")
            if file is None:
                flash("Файл не был загружен", "error")
                return redirect(f"/myprofile")
            filenames = safe_image_upload([file], directory, 5*1024*1024)
            if filenames and filenames[0] is not None:
                filename = filenames[0]
                try:
                    os.remove(os.path.join(directory, current_user.profile_pic))
                except:
                    pass
                squarify(directory, filename)
                current_user.profile_pic = filename
                db.session.commit()
                return redirect(f"/profile/user/{user.name}")
        if request.form.get("delete_profile_pic") is not None:
            directory = 'app/database/profile_pics'
            try:
                os.remove(os.path.join(directory, current_user.profile_pic))
            except:
                pass
            current_user.profile_pic = None
            db.session.commit()
            return redirect(f"/profile/user/{user.name}")




    return render_template("profile/profile_about.html", title="Мой профиль", user=user)


@prof.route("/profile/pools")
@login_required
def profile_pools():
    return render_template("profile/profile_pools.html", title="Мои пулы", user=current_user, str_from_dt = str_from_dt)


@prof.route("/profile/clubs")
@login_required
def profile_clubs():
    return render_template("profile/profile_clubs.html", title="Мои кружки", user=current_user)

@prof.route("/profile/settings")
@login_required
def profile_settings():
    return render_template("profile/profile_settings.html", title="Настройки", user=current_user)