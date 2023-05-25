from app.imports import *
from app.model_imports import *
from app.utils_and_functions.token_gen import generate_token
from app.utils_and_functions.send_letter import send_email
from app import website_link



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
        send_email(email_obj.name, f"{website_link}/verify/{email_obj.user.name}/{email_obj.name}/{token}")
    except:
        pass

