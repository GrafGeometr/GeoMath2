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
            return f(*args, **kwargs)
        return decorated_function
    return decorator


