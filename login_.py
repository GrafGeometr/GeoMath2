from all_imports_ import *


@app.route("/login/<href>")
def login(href):
    print(href)
    return render_template(
        "login.html", current_user=current_user, togo=f"/test_login/{href}"
    )


@app.route("/test_login/<href>", methods=["POST"])
def login_processing(href):
    data = request.get_json()
    login = data["login"]
    password = data["password"]
    print(login, password)
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.name == login).first()
    print(user)
    if user and user.check_password(password):
        login_user(user)
        print("Login successful")
        return href.replace("$", "/")

    return href.replace("$", "/")
