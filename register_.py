from all_imports_ import *


@app.route("/register")
def register():
    return render_template("register.html", current_user=current_user)


@app.route("/test_registration", methods=["POST", "GET"])
def test_registration():
    data = request.get_json()
    login = data["login"]
    email_name = data["email"]
    password = data["password"]
    repeat_password = data["repeat_password"]

    db_sess = db_session.create_session()

    if password != repeat_password:
        # passwords don't match
        return "/register"

    email = Email(name=email_name)

    user = User(name=login)

    user.emails.append(email)

    email_token_stuff(email)

    user.set_password(password)

    db_sess.add(user)
    db_sess.add(email)
    db_sess.commit()

    login_user(user)

    db_sess.close()

    # print(f"Login: {login}\nEmail: {email}\nPassword: {password}\nRepeat password: {repeat_password}")

    return "/feed"
