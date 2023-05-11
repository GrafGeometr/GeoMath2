from all_imports_ import *


@login_required
@app.route("/add_email", methods=["POST"])
def add_email():
    if not current_user.is_authenticated:
        return redirect("/login/$myprofile")

    data = request.get_json()
    email_name = data["email"]
    username = current_user.name

    db_sess = db_session.create_session()
    user = get_current_user(db_sess)

    err = "OK"
    # CHECK: USER DOESN'T EXIST
    if not user:
        # user doesn't exist
        # TODO say something about this
        err = "Error: User doesn't exist"

    # CHECK: INVALID EMAIL NAME
    if not email_validity_checker(email_name):
        err = "Error: Invalid email name"
        return render_template("emails_list.html", current_user=user, error_msg=err)
    # CHECK: EMAIL ALREADY EXISTS (CURRENT USER)
    if email_name in [em.name for em in user.emails]:
        err = "Error: Email already exists"
        return render_template("emails_list.html", current_user=user, error_msg=err)
    # CHECK: EMAIL ALREADY VERIFIED (OTHER USER)
    verified_emails = []
    for us in db_sess.query(User).filter().all():
        if us.id == user.id:
            continue
        for em in us.emails:
            if em.verified:
                verified_emails.append(em.name)
    if email_name in verified_emails:
        err = "Error: Email already verified (other user)"
        return render_template("emails_list.html", current_user=user, error_msg=err)

    # OK
    email = Email(name=email_name)
    user.emails.append(email)
    db_sess.add(email)

    email_token_stuff(email)

    db_sess.commit()

    db_sess.refresh(user)

    return render_template("emails_list.html", current_user=user, error_msg=err)


@login_required
@app.route("/remove_email", methods=["POST"])
def remove_email():
    if not current_user.is_authenticated:
        return redirect("/login/$myprofile")

    data = request.get_json()
    email_name = data["email"]
    username = current_user.name
    db_sess = db_session.create_session()

    user = get_current_user(db_sess)

    err = "OK"
    # CHECK: USER DOESN'T EXIST
    if not user:
        err = "Error: User doesn't exist"
        return render_template("emails_list.html", current_user=user, error_msg=err)
    # CHECK: INVALID EMAIL NAME
    if not email_validity_checker(email_name):
        err = "Error: Invalid email name"
        return render_template("emails_list.html", current_user=user, error_msg=err)

    # CHECK: USER HASN'T EMAIL
    email = (
        db_sess.query(Email)
        .filter((Email.name == email_name) & (Email.user_id == user.id))
        .first()
    )
    if not email:
        # email doesn't exist
        # TODO say something about this
        err = "Error: Email doesn't exist"
        return render_template("emails_list.html", current_user=user, error_msg=err)

    # OK
    for em in db_sess.query(Email).filter().all():
        print(em.name, em.user_id, bool(em.verified))
    user.emails.remove(email)
    db_sess.delete(email)
    db_sess.commit()

    db_sess.refresh(user)

    return render_template("emails_list.html", current_user=user, error_msg=err)


@login_required
@app.route("/send_verifying_link", methods=["POST"])
def send_verifying_link():
    if not current_user.is_authenticated:
        return redirect("/login/$myprofile")

    data = request.get_json()
    email_name = data["email"]

    db_sess = db_session.create_session()

    user = get_current_user(db_sess)

    err = "OK"
    # CHECK: USER DOESN'T EXIST
    if not user:
        err = "Error: User doesn't exist"
        return render_template("emails_list.html", current_user=user, error_msg=err)
    # CHECK: INVALID EMAIL NAME
    if not email_validity_checker(email_name):
        err = "Error: Invalid email name"
        return render_template("emails_list.html", current_user=user, error_msg=err)

    # CHECK: USER HASN'T EMAIL
    email = (
        db_sess.query(Email)
        .filter((Email.name == email_name) & (Email.user_id == user.id))
        .first()
    )
    if not email:
        err = "Error: Email doesn't exist"
        return render_template("emails_list.html", current_user=user, error_msg=err)

    # CHECK: EMAIL ALREADY VERIFIED
    verified_emails = []
    for us in db_sess.query(User).filter().all():
        for em in us.emails:
            if em.verified:
                verified_emails.append(em.name)
    if email_name in verified_emails:
        print("YES")
        err = "Error: Email already verified"
        print(err)
        print(render_template("emails_list.html", current_user=user, error_msg=err))
        return render_template("emails_list.html", current_user=user, error_msg=err)

    # OK

    email_token_stuff(email)

    db_sess.commit()

    db_sess.refresh(user)

    return render_template("emails_list.html", current_user=user, error_msg=err)


@app.route("/verify/<username>/<email_name>/<email_token>")
def verify(username, email_name, email_token):
    db_sess = db_session.create_session()

    user = get_current_user(db_sess)

    if not user:
        return redirect("/myprofile")

    email = (
        db_sess.query(Email)
        .filter((Email.name == email_name) & (Email.user_id == user.id))
        .first()
    )
    if not email:
        return redirect("/myprofile")

    if email.verified:
        return redirect("/myprofile")

    if email.token != email_token:
        return redirect("/myprofile")

    email.verified = True
    db_sess.commit()
    db_sess.close()

    return redirect("/myprofile")
