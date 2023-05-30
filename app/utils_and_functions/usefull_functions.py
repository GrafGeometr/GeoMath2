# -*- coding: utf-8 -*-
from app.imports import *
from app.model_imports import *
from app.utils_and_functions.token_gen import generate_token
from app.utils_and_functions.send_letter import send_email




def email_validity_checker(email):
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
    return (bool(re.fullmatch(regex, email)))

def get_current_user():
    return User.query.filter_by(name = current_user.name).first()

def email_token_stuff(email_obj):
    print(email_obj)

    token = generate_token(30)
    email_obj.token = token
    try:
        send_email(email_obj.name, url_for("emv.verify", username=email_obj.user.name, email_name=email_obj.name, email_token=token, _external=True))
    except Exception as e:
        print(e)
        

