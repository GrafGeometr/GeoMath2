from .imports import *
from .model_imports import *

emv = Blueprint('emv', __name__)


@login_required
@emv.route("/add_email", methods=["POST"])
def add_email():
    if not current_user.is_authenticated:
        return redirect("/login")

    data = request.get_json()
    email_name = data["email"]

    err = "OK"
    # CHECK: USER DOESN'T EXIST
    if not current_user:
        # user doesn't exist
        # TODO say something about this
        err = "Error: User doesn't exist"

    # CHECK: INVALID EMAIL NAME
    if not email_validity_checker(email_name):
        err = "Error: Invalid email name"
        flash("Некорректный email", "danger")
        return render_template("profile/emails_list.html")
    # CHECK: EMAIL ALREADY EXISTS (CURRENT USER)
    if email_name in [em.name for em in current_user.emails]:
        err = "Error: Email already exists"
        flash("Этот email уже используется Вами", "warning")
        return render_template("profile/emails_list.html")
    # CHECK: EMAIL ALREADY VERIFIED (OTHER USER)
    verified_emails = []
    for us in User.query.all():
        if us.id == current_user.id:
            continue
        for em in us.emails:
            if em.verified:
                verified_emails.append(em.name)
    if email_name in verified_emails:
        err = "Error: Email already verified (other user)"
        flash("Этот email уже используется другим пользователем", "warning")
        return render_template("profile/emails_list.html")

    # OK
    email = Email(name=email_name, user=current_user)
    email_token_stuff(email)
    db.session.add(email)
    db.session.commit()

    flash("Email успешно добавлен, подтвердите его", "success")
    return render_template("profile/emails_list.html")


@login_required
@emv.route("/remove_email", methods=["POST"])
def remove_email():
    if not current_user.is_authenticated:
        return redirect("/login")

    data = request.get_json()
    email_name = data["email"]

    err = "OK"
    # CHECK: USER DOESN'T EXIST
    if not current_user:
        err = "Error: User doesn't exist"
        return render_template("profile/emails_list.html")
    # CHECK: INVALID EMAIL NAME
    if not email_validity_checker(email_name):
        err = "Error: Invalid email name"
        flash("Некорректный email", "danger")
        return render_template("profile/emails_list.html")

    # CHECK: USER HASN'T EMAIL
    email = Email.query.filter_by(name = email_name, user_id = current_user.id).first()
    if not email:
        # email doesn't exist
        # TODO say something about this
        err = "Error: Email doesn't exist"
        flash("Этот email не используется Вами", "danger")
        return render_template("profile/emails_list.html")

    # OK
    for em in Email.query.all():
        print(em.name, em.user_id, bool(em.verified))
    
    db.session.delete(email)
    db.session.commit()
    flash("Email успешно удален", "success")
    return render_template("profile/emails_list.html")


@login_required
@emv.route("/send_verifying_link", methods=["POST"])
def send_verifying_link():
    if not current_user.is_authenticated:
        return redirect("/login")

    data = request.get_json()
    email_name = data["email"]

    err = "OK"
    # CHECK: USER DOESN'T EXIST
    if not current_user:
        err = "Error: User doesn't exist"
        return render_template("profile/emails_list.html")
    # CHECK: INVALID EMAIL NAME
    if not email_validity_checker(email_name):
        err = "Error: Invalid email name"
        flash("Некорректный email", "danger")
        return render_template("profile/emails_list.html")

    # CHECK: USER HASN'T EMAIL
    email = Email.query.filter_by(name = email_name, user_id = current_user.id).first()
    if not email:
        err = "Error: Email doesn't exist"
        flash("Этот email не используется Вами", "danger")
        return render_template("profile/emails_list.html")

    # CHECK: EMAIL ALREADY VERIFIED
    verified_emails = []
    for us in User.query.all():
        for em in us.emails:
            if em.verified:
                verified_emails.append(em.name)
    if email_name in verified_emails:
        err = "Error: Email already verified"
        flash("Email уже подтверждён", "warnings")
        return render_template("profile/emails_list.html")

    # OK
    email_token_stuff(email)
    db.session.commit()
    flash("Письмо с подтверждением успешно отправлено", "success")
    return render_template("profile/emails_list.html")


@emv.route("/verify/<username>/<email_name>/<email_token>")
def verify(username, email_name, email_token):
    print(username, email_name, email_token)
    if not current_user:
        print(1)
        return redirect("/myprofile")

    email = Email.query.filter_by(name = email_name, user_id = current_user.id).first()
    if not email:
        print(2)
        return redirect("/myprofile")

    if email.verified:
        print(3)
        return redirect("/myprofile")

    if email.token != email_token:
        print(4)
        return redirect("/myprofile")

    print(6)
    email.verified = True
    db.session.commit()
    print(5)
    return redirect("/myprofile")
