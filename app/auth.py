from .imports import *
from .model_imports import *

auth = Blueprint('auth', __name__)

@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        login = request.form.get("login")
        password = request.form.get("password")
        next_url = request.form.get("next")

        user = User.query.filter_by(name = login).first()
        if user and user.check_password(password):
            login_user(user)
            if next_url:
                return redirect(next_url)
            return redirect("/myprofile")
        else:
            flash("Неверный логин или пароль", "danger")
    
    return render_template("login.html")

@auth.route("/register")
def register():
    print("REG")
    return render_template("register.html", current_user=current_user)


@auth.route("/test_registration", methods=["POST", "GET"])
def test_registration():
    data = request.get_json()
    login = data["login"]
    email_name = data["email"]
    password = data["password"]
    repeat_password = data["repeat_password"]


    if password != repeat_password:
        # passwords don't match
        return "/register"

    user = User(name=login)
    email = Email(name=email_name, user=user)

    email_token_stuff(email)

    user.set_password(password)

    db.session.add(user)
    db.session.add(email)
    db.session.commit()

    login_user(user)

    # print(f"Login: {login}\nEmail: {email}\nPassword: {password}\nRepeat password: {repeat_password}")

    return "/feed"

@auth.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("auth.login"))