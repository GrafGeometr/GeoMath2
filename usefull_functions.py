from flask import redirect
from flask_login import current_user, login_required
from data.user import User
from send_letter import send_email
from token_gen import generate_token
from init_app import website_link
import re


from flask import redirect
from flask_login import current_user
from functools import wraps


def check_if_email_is_correct(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email)

def get_current_user(db_sess):
    return db_sess.query(User).filter(User.name == current_user.name).first()

def email_token_stuff(email_obj):
    token = generate_token(30)
    email_obj.token = token

    send_email(email_obj.name, f"{website_link}/verify/{email_obj.name}/{token}")

