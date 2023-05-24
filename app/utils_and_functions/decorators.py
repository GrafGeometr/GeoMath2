from flask import redirect
from flask_login import current_user, login_required


from flask import redirect, request, url_for, flash
from flask_login import current_user
from functools import wraps

def go_to_login(href):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                return redirect(f"/login/{href.replace('/', '$')}")
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

def login_required(f):
    @wraps(f)
    def secure_function(*args, **kwargs):
        if not current_user.is_authenticated:
            flash("Войдите в аккаунт для доступа к сайту", "warning")
            return redirect(url_for("auth.login", next=request.url))
        return f(*args, **kwargs)

    return secure_function