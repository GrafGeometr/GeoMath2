from flask import Flask, render_template, redirect, request, make_response
import os
from data.user import User
from data.email import Email
from init_app import app, load_user, website_link
from decorators import route
from data import db_session
from token_gen import generate_token
from send_letter import send_email



from flask_login import (
    LoginManager,
    login_user,
    logout_user,
    current_user,
    login_required,
)

# from flask_restful import abort


@route("/")
def index():
    return render_template("base.html", current_user=current_user)


@route("/feed")
def feed():
    return render_template("feed.html", current_user=current_user)


@route("/contests")
def contests():
    return render_template("contests.html", current_user=current_user)


@route("/collections")
def collections():
    return render_template("collections.html", current_user=current_user)


@route("/editor")
def editor():
    return render_template("editor.html", current_user=current_user)


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
    return render_template("profile.html", current_user=current_user)


@app.route("/register")
def register():
    return render_template("register.html", current_user=current_user)


@app.route("/login/<href>")
def login(href):
    print(href)
    return render_template(
        "login.html", current_user=current_user, togo=f"/test_login/{href}"
    )


@app.route("/logout")
def logout():
    logout_user()
    return redirect("/")


@app.route("/test_login/<href>", methods=["POST"])
def test_login(href):
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


@app.route("/add_email", methods=["POST"])
def add_email():
    data = request.get_json()
    email = data["email"]
    username = data["username"]
    db_sess = db_session.create_session()
    email = Email(name=email)
    db_sess.add(email)

    user = db_sess.query(User).filter(User.name == username).first()
    if not user:
        # user doesn't exist
        # TODO say something about this
        return "Error"

    if user.name != current_user.name:
        # this is other user
        # TODO say something about this
        return "Error"

    user.emails.append(email)

    db_sess.commit()

    db_sess.refresh(user)

    return render_template("emails_list.html", current_user=user)


@app.route("/remove_email", methods=["POST"])
def remove_email():
    data = request.get_json()
    email = data["email"]
    username = data["username"]
    db_sess = db_session.create_session()
    email = db_sess.query(Email).filter(Email.name == email).first()
    if not email:
        # email doesn't exist
        # TODO say something about this
        return "Error"

    user = db_sess.query(User).filter(User.name == username).first()
    if not user:
        # user doesn't exist
        # TODO say something about this
        return "Error1"

    if user.name != current_user.name:
        # this is other user
        # TODO say something about this
        return "Error2"

    verified_emails_count = 0
    for email in user.emails:
        if email.verified:
            verified_emails_count += 1

    if verified_emails_count <= 1 and email.verified:
        # not enough verified emails
        # TODO say something about this
        return "Error3"

    user.emails.remove(email)
    db_sess.delete(email)
    db_sess.commit()

    db_sess.refresh(user)

    return render_template("emails_list.html", current_user=user)


@login_required
@app.route("/send_verifying_link", methods=["POST"])
def send_verifying_link():
    if not current_user.is_authenticated:
        return redirect("/login/$myprofile")
    data = request.get_json()
    email_name = data["email"]
    db_sess = db_session.create_session()
    email = db_sess.query(Email).filter(Email.name == email_name).first()
    if not email:
        # email doesn't exist
        # TODO say something about this
        return "Error"
    
    user = db_sess.query(User).filter(User.name == current_user.name).first()
    if not user:
        # user doesn't exist
        # TODO say something about this
        return "Error1"
    
    if user.name != current_user.name:
        # this is other user
        # TODO say something about this
        return "Error2"
    
    if email.user_id != current_user.id:
        # this is other's user email
        # TODO say something about this
        return "Error3"
    
    email_token = generate_token(30)

    email.token = email_token

    db_sess.commit()

    db_sess.refresh(user)

    send_email(email_name, f"{website_link}/verify/{email_name}/{email_token}")

    return render_template("emails_list.html", current_user=user)


@app.route("/verify/<email_name>/<email_token>")
def verify(email_name, email_token):
    db_sess = db_session.create_session()
    email = db_sess.query(Email).filter(Email.name == email_name).first()
    if not email:
        # email doesn't exist
        # TODO say something about this
        return "Error"
    
    user = db_sess.query(User).filter(User.name == current_user.name).first()
    if not user:
        # user doesn't exist
        # TODO say something about this
        return "Error1"
    
    if user.name != current_user.name:
        # this is other user
        # TODO say something about this
        return "Error2"
    
    if email.user_id != current_user.id:
        # this is other's user email
        # TODO say something about this
        return "Error3"
    
    if email.token != email_token:
        # wrong token
        # TODO say something about this
        return "Error4"
    
    email.verified = True
    db_sess.commit()
    db_sess.close()

    return redirect("/myprofile")




@app.route("/test_registration", methods=["POST", "GET"])
def test_registration():
    data = request.get_json()
    login = data["login"]
    email_name = data["email"]
    password = data["password"]
    repeat_password = data["repeat_password"]

    db_sess = db_session.create_session()

    email = db_sess.query(Email).filter(Email.name == email_name).first()
    if email:
        # email already exists
        return "/register"

    if password != repeat_password:
        # passwords don't match
        return "/register"

    email = Email(name=email_name)

    user = User(name=login)

    user.emails.append(email)

    user.set_password(password)

    db_sess.add(user)
    db_sess.add(email)
    db_sess.commit()

    # login_user(user)

    db_sess.close()

    # print(f"Login: {login}\nEmail: {email}\nPassword: {password}\nRepeat password: {repeat_password}")

    return "/feed"


def main():
    db_session.global_init("database/blogs.db")

    port = int(os.environ.get("PORT", 5000))
    # app.run(host='0.0.0.0', port=port)
    app.run(port=8000, host="127.0.0.1")


if __name__ == "__main__":
    main()
