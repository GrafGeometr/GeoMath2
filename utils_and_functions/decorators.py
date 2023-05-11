from flask import redirect
from flask_login import current_user, login_required
from init_app import app


from flask import redirect
from flask_login import current_user
from functools import wraps

def go_to_login(href):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                return redirect(f"/login/{href.replace('/', '$')}")
            print("OK")
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def email_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.get_verified_emails_count() == 0:
            # TODO redirect to verification page
            return redirect("/myprofile")
        return f(*args, **kwargs)
    return decorated_function

def route(href):
    def decorator(f):
        return app.route(href)(go_to_login(href)(email_required(login_required(f))))
    return decorator
