from flask import redirect
from flask_login import current_user, login_required
from data.user import User
from utils_and_functions.send_letter import send_email
from utils_and_functions.token_gen import generate_token
from init_app import website_link
import re


from flask_login import current_user



def email_validity_checker(email):
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
    return (bool(re.fullmatch(regex, email)))

def get_current_user(db_sess):
    return db_sess.query(User).filter(User.name == current_user.name).first()

def email_token_stuff(email_obj):
    token = generate_token(30)
    email_obj.token = token

    send_email(email_obj.name, f"{website_link}/verify/{email_obj.user.name}/{email_obj.name}/{token}")

