from .imports import *
from .logger_classes.login_exception import LoginException
from .logger_classes.register_exception import RegisterException
from .model_imports import *

auth = Blueprint("auth", __name__)


@auth.route("/login", methods=["POST"])
def login():
    login = request.form.get("login")
    password = request.form.get("password")
    next_url = request.form.get("next")

    try:
        User.login(login=login, password=password).act()
        return redirect(next_url if next_url else "/myprofile")
    except LoginException as e:
        e.flash()
        return redirect("/login")


@auth.route("/login", methods=["GET"])
def login_page():
    return render_template("auth/login.html", title="GeoMath - авторизация")


@auth.route("/register", methods=["POST"])
def register():
    login = request.form.get("login", "").strip()
    email_name = request.form.get("email")
    password = request.form.get("password")
    repeat_password = request.form.get("repeat_password")
    next_url = request.form.get("next")

    try:
        User.register(
            login=login,
            email_name=email_name,
            password=password,
            repeat_password=repeat_password,
        ).act()

        return redirect(next_url if next_url else "/myprofile")
    except RegisterException as e:
        e.flash()
        return redirect("/register")


@auth.route("/register", methods=["GET"])
def register_page():
    return render_template(
        "auth/register.html", current_user=current_user, title="GeoMath - регистрация"
    )


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))
