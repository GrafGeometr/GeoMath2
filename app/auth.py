from .imports import *
from .model_imports import *

auth = Blueprint('auth', __name__)

@auth.route("/login/<href>")
def login(href):
    print(href)
    return render_template("login.html", togo=f"/test_login/{href}")

@auth.route("/test_login/<href>", methods=["POST"])
def login_processing(href):
    data = request.get_json()
    login = data["login"]
    password = data["password"]
    print(login, password)
    user = User.query.filter_by(name = login).first()
    print(user)
    if user and user.check_password(password):
        login_user(user)
        print("Login successful")
        return href.replace("$", "/")
    print("UnAuth")
    return "/login/"+href


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
    return redirect("/")