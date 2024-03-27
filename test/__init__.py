import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_socketio import SocketIO


from app import db

basedir = os.path.abspath(os.path.dirname(__file__))


def create_test_app():
    app = Flask(__name__)
    # app.config['SERVER_NAME'] = 'ge0math.ru'
    app.config["SECRET_KEY"] = "yandexlyceum_secret_key_2"
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(
        basedir, "database/test.sqlite"
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    migrate = Migrate(app, db, compare_type=True)

    login_manager = LoginManager()
    login_manager.init_app(app)

    from app.dbc import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    with app.app_context():
        db.create_all()

    return app
