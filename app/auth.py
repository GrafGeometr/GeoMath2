from .imports import *
from .model_imports import *

auth = Blueprint('auth', __name__)


@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        login = request.form.get("login")
        password = request.form.get("password")
        next_url = request.form.get("next")

        user = User.query.filter_by(name = login).first()
        if user and user.check_password(password):
            login_user(user, remember=True, duration=datetime.timedelta(days=5))
            confirm_login()
            if next_url:
                return redirect(next_url)
            return redirect("/myprofile")
        else:
            flash("Неверный логин или пароль", "error")
    
    return render_template("auth/login.html", title="GeoMath - авторизация")



@auth.route("/register", methods=["POST", "GET"])
def register():
    if request.method == "POST":
        login = request.form.get("login", "").strip()
        email_name = request.form.get("email")
        password = request.form.get("password")
        repeat_password = request.form.get("repeat_password")
        next_url = request.form.get("next")

        possible_characters = string.ascii_letters + string.digits + "_-."
        if (login=="") or (not all(c in possible_characters for c in login)):
            flash("Некорректный логин, допустимые символы: A-Z a-z 0-9 _ - .", "error")
            return redirect("/register")
        
        if len(login) < 4:
            flash("Длина логина должна быть не менее 4 символов", "error")
            return redirect("/register")
        
        if login.lower() in [user.name.lower() for user in User.query.all()]:
            flash("Пользователь с таким именем уже существует", "error")
            return redirect("/register")

        if not email_validity_checker(email_name):
            flash("Некорректный email", "error")
            return redirect("/register")

        if password != repeat_password:
            # passwords don't match
            flash("Пароли не совпадают", "error")
            return redirect("/register")
        
        if len(password) < 6:
            flash("Длина пароля должна быть не менее 6 символов", "error")
            return redirect("/register")

        

        user = User(name=login)
        email = Email(name=email_name, user=user)


        email_token_stuff(email)

        user.set_password(password)

        db.session.add(user)
        db.session.add(email)
        db.session.commit()

        login_user(user, remember=True, duration=datetime.timedelta(days=5))
        confirm_login()

        # print(f"Login: {login}\nEmail: {email}\nPassword: {password}\nRepeat password: {repeat_password}")
        if next_url:
            return redirect(next_url)
        return redirect("/myprofile")
    
    return render_template("auth/register.html", current_user=current_user, title="GeoMath - регистрация")

@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))