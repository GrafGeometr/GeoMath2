from flask import Flask
from flask_login import LoginManager
from data import db_session
from data.user import User

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
app.config['UPLOAD_EXTENSIONS'] = ['.txt', '.pdf', '.doc', '.docx', '.png', '.jpeg', '.jpg', '.gif']
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)