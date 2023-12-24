from flask import redirect
from flask_login import current_user, login_required

from flask import redirect, request, url_for, flash
from flask_login import current_user
from functools import wraps


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
