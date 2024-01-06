from flask import redirect
from flask_login import current_user, login_required

from flask import redirect, request, url_for, flash
from flask_login import current_user
from functools import wraps
from app.logger_classes.exception import CustomException


def login_required(f):
    @wraps(f)
    def secure_function(*args, **kwargs):
        print("login_required")
        print(current_user.is_authenticated)
        if not current_user.is_authenticated:
            return redirect(url_for("auth.login", next=request.url))
        return f(*args, **kwargs)

    return secure_function


def admin_required(f):
    @wraps(f)
    def secure_function(*args, **kwargs):
        if (not current_user.is_authenticated) or (not current_user.admin):
            return redirect("/admin/enter")
        return f(*args, **kwargs)

    return secure_function


def post_request_exception_handler(f):
    @wraps(f)
    def secure_function(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except CustomException as e:
            e.flash()
        except Exception as e:
            flash(f"Unexpected error: {str(e)}", "error")
            raise

    return secure_function


# TODO : write GET request exception handler
