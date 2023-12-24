import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_socketio import SocketIO

db = SQLAlchemy()
basedir = os.path.abspath(os.path.dirname(__file__))
socketio = SocketIO()

from .logger_classes.logger import Logger

logger = Logger()


def create_app():
    app = Flask(__name__)
    # app.config['SERVER_NAME'] = 'ge0math.ru'
    app.config['SECRET_KEY'] = 'yandexlyceum_secret_key_2'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'database/data.sqlite')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    socketio.init_app(app)

    db.init_app(app)
    migrate = Migrate(app, db, compare_type=True)

    login_manager = LoginManager()
    login_manager.init_app(app)

    from .dbc import User
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    @app.after_request
    def add_header(response):
        response.cache_control.private = True
        response.cache_control.public = False
        return response

    from .general import general as general_blueprint
    app.register_blueprint(general_blueprint)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from .archive import arch as arch_blueprint
    app.register_blueprint(arch_blueprint)

    from .admin import admin as admin_blueprint
    app.register_blueprint(admin_blueprint)

    from .prof import prof as prof_blueprint
    app.register_blueprint(prof_blueprint)

    from .pool import pool as pool_blueprint
    app.register_blueprint(pool_blueprint)

    from .navigation import nav as nav_blueprint
    app.register_blueprint(nav_blueprint)

    from .email_verifying import emv as emv_blueprint
    app.register_blueprint(emv_blueprint)

    from .latex import latex as latex_blueprint
    app.register_blueprint(latex_blueprint)

    from .contest import contest as contest_blueprint
    app.register_blueprint(contest_blueprint)

    from .chat import chat as chat_blueprint
    app.register_blueprint(chat_blueprint)

    from .club import club as club_blueprint
    app.register_blueprint(club_blueprint)

    from .olimpiad import olimpiad as olimpiad_blueprint
    app.register_blueprint(olimpiad_blueprint)

    from .errorhandlers import err as err_blueprint
    app.register_blueprint(err_blueprint)

    with app.app_context():
        db.create_all()

    return app
