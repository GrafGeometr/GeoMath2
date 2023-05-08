from flask import Flask, render_template, redirect, request, make_response
import os
from data.user import User
from init_app import app, load_user
from decorators import go_to_login
from data import db_session


from flask_login import LoginManager, login_user, logout_user, current_user, login_required
#from flask_restful import abort



@login_required
@app.route('/')
@go_to_login('/')
def index():
    return render_template('base.html', username = "EvgenyUtkin")


@login_required
@app.route('/feed')
@go_to_login('/feed')
def feed():
    return render_template('feed.html')

@login_required
@app.route('/contests')
@go_to_login('/contests')
def contests():
    return render_template('contests.html')

@login_required
@app.route('/collections')
@go_to_login('/collections')
def collections():
    return render_template('collections.html')

@login_required
@app.route('/editor')
@go_to_login('/editor')
def editor():
    return render_template('editor.html')

@login_required
@app.route('/profile/<username>')
@go_to_login('/profile/<username>')
def profile(username):
    return render_template('profile.html', username = username)


@app.route('/register')
def register():
    return render_template('register.html')


@app.route('/login/<href>')
def login(href):
    return "Ooops!"


@app.route('/test_registration', methods=['POST', 'GET'])
def test_registration():
    data = request.get_json()
    login = data['login']
    email = data['email']
    password = data['password']
    repeat_password = data['repeat_password']

    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.email == email).first()
    if user:
        return "Такой пользователь уже есть"
    
    if password != repeat_password:
        return "Пароли не совпадают"
    
    user = User(name=login, email=email)

    user.set_password(password)

    login_user(user)

    db_sess.add(user)
    db_sess.commit()
    db_sess.close()



    # print(f"Login: {login}\nEmail: {email}\nPassword: {password}\nRepeat password: {repeat_password}")

    return "/feed"

def main():

    db_session.global_init("database/blogs.db")

    port = int(os.environ.get("PORT", 5000))
    #app.run(host='0.0.0.0', port=port)
    app.run(port=8000, host='127.0.0.1')

if __name__ == '__main__':
    main()