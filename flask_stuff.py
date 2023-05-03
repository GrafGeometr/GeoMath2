from flask import Flask, render_template, redirect, request, make_response
import os
#from flask_login import LoginManager, login_user, login_required, logout_user, current_user
#from flask_restful import abort

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
app.config['UPLOAD_EXTENSIONS'] = ['.txt', '.pdf', '.doc', '.docx', '.png', '.jpeg', '.jpg', '.gif']
#login_manager = LoginManager()
#login_manager.init_app(app)


@app.route('/')
def index():
    return render_template('base.html')

@app.route('/feed')
def feed():
    return render_template('feed.html')

@app.route('/contests')
def contests():
    return render_template('contests.html')

@app.route('/collections')
def collections():
    return render_template('collections.html')

@app.route('/editor')
def editor():
    return render_template('editor.html')

def main():
    port = int(os.environ.get("PORT", 5000))
    #app.run(host='0.0.0.0', port=port)
    app.run(port=8000, host='127.0.0.1')

if __name__ == '__main__':
    main()