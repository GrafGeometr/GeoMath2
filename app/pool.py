from .imports import *
from .model_imports import *

pool = Blueprint("pool", __name__)


# --> Pools access checking


# check if user is in pool
def check_user_in_pool(user, pool):
    if user.get_pool_relation(pool.id) is None:
        flash("Вы не можете просматривать этот пул", "error")
        return "/myprofile"
    if user.get_pool_relation(pool.id).role.isInvited():
        flash("Вы не приняли приглашение в этот пул", "error")
        return f"/profile/user/{user.name}/pools"
    return None


# -----------------------------------------------------------------------------------------------------------------------------


# check if user is allowed to manage pool (owner)
def check_management_access(user, pool):
    if user.get_pool_relation(pool.id).role.isOwner():
        return None
    flash("Вы не можете управлять этим пулом", "error")
    return url_for("pool.pool_participants", pool_hashed_id=pool.hashed_id)


# =============================================================================================================================


# --> Pool problems


# list of problems in pool
@pool.route("/pool/<pool_hashed_id>/problems", methods=["GET", "POST"])
@login_required
def pool_problems(pool_hashed_id):
    pool = Pool.query.filter_by(hashed_id=pool_hashed_id).first()

    if pool is None:
        flash("Пул с таким id не найден", "error")
        return redirect("/myprofile")

    user_checked = check_user_in_pool(current_user, pool)
    if user_checked is not None:
        return redirect(user_checked)

    if request.method == "POST":
        if request.form.get("back_to_pool") is not None:
            problem_hashed_id = request.form.get("problem_hashed_id")
            problem = Problem.query.filter_by(hashed_id=problem_hashed_id).first()
            problem.is_public = problem.moderated = False
            db.session.commit()
            return redirect(f"/pool/{pool_hashed_id}/problem/{problem_hashed_id}")
    return render_template(
        "pool/pool_problems.html", current_pool=pool, title=f"{pool.name} - задачи"
    )


# create new problem in pool
@pool.route("/pool/<pool_hashed_id>/new_problem", methods=["POST"])
@login_required
def new_problem(pool_hashed_id):
    pool = Pool.query.filter_by(hashed_id=pool_hashed_id).first()

    if pool is None:
        flash("Пул с таким id не найден", "error")
        return redirect("/myprofile")

    user_checked = check_user_in_pool(current_user, pool)
    if user_checked is not None:
        return redirect(user_checked)

    problem = pool.new_problem()

    return redirect(f"/pool/{pool_hashed_id}/problem/{problem.hashed_id}")


# -----------------------------------------------------------------------------------------------------------------------------


# delete problem from pool
@pool.route("/remove_problem_from_pool", methods=["POST"])
@login_required
def remove_problem_from_pool():
    data = request.get_json()
    pool_hashed_id = data["pool"]
    problem_hashed_id = data["problem"]
    pool = Pool.query.filter_by(hashed_id=pool_hashed_id).first()

    if pool is None:
        flash("Пул с таким id не найден", "error")
        return redirect("/myprofile")

    user_checked = check_user_in_pool(current_user, pool)
    if user_checked is not None:
        return redirect(user_checked)

    problem = Problem.query.filter_by(hashed_id=problem_hashed_id).first()

    if problem is None:
        flash("Задача не найдена", "error")
        return redirect(f"/pool/{pool_hashed_id}/problems")

    problem.remove()
    return render_template(
        "pool/pool_problemlist.html", current_pool=pool, title=f"{pool.name} - задачи"
    )


# -----------------------------------------------------------------------------------------------------------------------------


# add attachment to problem
@pool.route(
    "/pool/<pool_hashed_id>/problem/<problem_hashed_id>/upload_file", methods=["POST"]
)
@login_required
def upload_file_to_problem(pool_hashed_id, problem_hashed_id):
    pool = Pool.query.filter_by(hashed_id=pool_hashed_id).first()

    if pool is None:
        flash("Пул с таким id не найден", "error")
        return redirect("/myprofile")

    user_checked = check_user_in_pool(current_user, pool)
    if user_checked is not None:
        return redirect(user_checked)

    problem = Problem.query.filter_by(hashed_id=problem_hashed_id).first()
    if problem is None:
        flash("Задача не найдена", "error")
        return redirect(f"/pool/{pool_hashed_id}/problems")

    file = request.files.get("file")
    if file is None:
        flash("Файл не был загружен", "error")
        return redirect(f"/pool/{pool_hashed_id}/problem/{problem_hashed_id}")
    
    if not problem.is_public:
        directory = "app/database/attachments/problems"
        filenames = safe_image_upload(
            [file], directory, 5 * 1024 * 1024
        )

        filename = filenames[0]

        if filename is None:
            flash("Ошибка при загрузке", "error")
            return redirect(f"/pool/{pool_hashed_id}/problem/{problem_hashed_id}")
        
        attachment = Attachment(
            db_folder=directory,
            db_filename=filename,
            short_name="Рисунок",
            parent_type=DbParent.fromType(type(problem)),
            parent_id=problem.id,
            other_data={"is_secret": True}
        )
        db.session.add(attachment)

        db.session.commit()

        return f"OK {attachment.db_filename}"
    
    return redirect(f"/pool/{pool_hashed_id}/problem/{problem_hashed_id}")


# -----------------------------------------------------------------------------------------------------------------------------


# show and edit problem in pool
@pool.route("/pool/<pool_hashed_id>/problem/<problem_hashed_id>", methods=["GET", "POST"])
@login_required
def problem(pool_hashed_id, problem_hashed_id):
    pool = Pool.query.filter_by(hashed_id=pool_hashed_id).first()

    if pool is None:
        flash("Пул с таким id не найден", "error")
        return redirect("/myprofile")

    user_checked = check_user_in_pool(current_user, pool)
    if user_checked is not None:
        return redirect(user_checked)

    problem = Problem.query.filter_by(hashed_id=problem_hashed_id).first()

    if problem is None:
        flash("Задача не найдена", "error")
        return redirect(f"/pool/{pool_hashed_id}/problems")

    if request.method == "POST":
        if request.form.get("save_problem") is not None:
            name = request.form.get("name")
            statement = request.form.get("statement")
            solution = request.form.get("solution")

            if not problem.is_public:
                problem.name = name
                problem.statement = statement
                problem.solution = solution

            problem.show_solution = request.form.get("show_solution") == "on"
            db.session.commit()


            form = request.form.to_dict()
            print(form)

            new_tags_names = []
            for key, value in form.items():
                if key[:4] == "tag ":
                    new_tags_names.append(value)
            
            problem.act_set_tags(new_tags_names)


            for attachment in problem.get_attachments():
                print(attachment.db_filename)
                short_name = request.form.get("attachment_name " + str(attachment.db_filename))
                if not problem.is_public:
                    if short_name is None:
                        attachment.remove()
                        continue

                if not problem.is_public:
                    attachment.short_name = short_name
                is_secret = request.form.get("attachment_is_secret " + str(attachment.db_filename))
                if is_secret == "on":
                    attachment.other_data["is_secret"] = True
                else:
                    attachment.other_data["is_secret"] = False
                flag_modified(attachment, "other_data")
            db.session.commit()
            flash("Задача успешно сохранена", "success")
            return redirect(f"/pool/{pool_hashed_id}/problem/{problem_hashed_id}")
    return render_template(
        "pool/pool_1problem.html",
        current_pool=pool,
        current_problem=problem,
        title=f"Редактор - {problem.name}",
        all_tags=sorted(Tag.query.all(), key=lambda x: x.name.lower()),
    )


# -----------------------------------------------------------------------------------------------------------------------------

import json

# get problem content
@pool.route("/get_problem_content/<problem_hashed_id>", methods=["GET", "POST"])
def get_problem_content(problem_hashed_id): # TODO fix access
    print(problem_hashed_id)
    problem = Problem.query.filter_by(hashed_id=problem_hashed_id).first()
    if problem is None:
        print("problem none")
        return
    
    # if problem is archived
    if problem.is_archived():
        return json.dumps(
            { 'name': problem.name
            , 'statement': problem.statement
            , 'solution': problem.solution if problem.is_solution_available() else "Решение скрыто"
            , 'files': [[file.preview_name, file.db_filename] for file in problem.get_nonsecret_attachments() if file.other_data.get("is_secret", False)]
            , 'tags': [tag.name for tag in problem.get_tags()]
            }
        )

    # if user is in problem pool
    if problem.pool is None:
        print("pool none")
        return
    relation = current_user.get_pool_relation(problem.pool_id)
    if relation is None:
        print("user not in pool")
        return
    return json.dumps(
        { 'name': problem.name
        , 'statement': problem.statement
        , 'solution': problem.solution
        , 'files': [[file.short_name, file.db_filename] for file in problem.get_nonsecret_attachments()]
        , 'tags': [tag.name for tag in problem.get_tags()]
        }
    )


# -----------------------------------------------------------------------------------------------------------------------------





# send problem attachment
@pool.route("/pool/<pool_hashed_id>/problem/<problem_hashed_id>/<filename>")
def show_problem_attachment(pool_hashed_id, problem_hashed_id, filename):
    print(pool_hashed_id, problem_hashed_id, filename)
    if not current_user.is_authenticated:
        print("not authenticated")
        return
    pool = Pool.query.filter_by(hashed_id=pool_hashed_id).first()
    if pool is None:
        print("pool none")
        return
    relation = current_user.get_pool_relation(pool.id)
    if relation is None:
        print("user not in pool")
        return
    if relation.role.isInvited():
        print("user is invited")
        return
    problem = Problem.query.filter_by(hashed_id=problem_hashed_id).first()
    if problem is None:
        print("problem none")
        return
    attachment = Attachment.get_by_db_filename(filename)
    if not attachment.is_from_parent(problem):
        print("attachment none")
        return
    try:
        return send_from_directory(
            os.path.join(basedir, "database/attachments/problems"),
            filename,
            as_attachment=True,
        )
    except Exception as e:
        print(e)


# =============================================================================================================================


# --> Pool sheets


# list all sheets in pool
@pool.route("/pool/<pool_hashed_id>/sheets", methods=["GET", "POST"])
@login_required
def pool_sheets(pool_hashed_id):
    pool = Pool.query.filter_by(hashed_id=pool_hashed_id).first()

    if pool is None:
        flash("Пул с таким id не найден", "error")
        return redirect("/myprofile")

    user_checked = check_user_in_pool(current_user, pool)
    if user_checked is not None:
        return redirect(user_checked)

    if request.method == "POST":
        if request.form.get("back_to_pool") is not None:
            sheet_id = request.form.get("sheet_id")
            sheet = Sheet.query.filter_by(id=sheet_id).first()
            sheet.is_public = False
            db.session.commit()
            return redirect(f"/pool/{pool_hashed_id}/sheet/{sheet_id}")
    return render_template(
        "pool/pool_sheets.html", current_pool=pool, title=f"{pool.name} - подборки"
    )


# -----------------------------------------------------------------------------------------------------------------------------


# create new sheet in pool
@pool.route("/pool/<pool_hashed_id>/new_sheet", methods=["POST"])
@login_required
def new_sheet(pool_hashed_id):
    pool = Pool.query.filter_by(hashed_id=pool_hashed_id).first()

    if pool is None:
        flash("Пул с таким id не найден", "error")
        return redirect("/myprofile")

    user_checked = check_user_in_pool(current_user, pool)
    if user_checked is not None:
        return redirect(user_checked)

    sheet = pool.new_sheet()

    return redirect(f"/pool/{pool_hashed_id}/sheet/{sheet.id}")


# -----------------------------------------------------------------------------------------------------------------------------


# delete sheet from pool
@pool.route("/remove_sheet_from_pool", methods=["POST"])
@login_required
def remove_sheet_from_pool():
    data = request.get_json()
    pool_hashed_id = data["pool"]
    sheet_id = data["sheet"]
    pool = Pool.query.filter_by(hashed_id=pool_hashed_id).first()

    if pool is None:
        flash("Пул с таким id не найден", "error")
        return redirect("/myprofile")

    user_checked = check_user_in_pool(current_user, pool)
    if user_checked is not None:
        return redirect(user_checked)

    sheet = Sheet.query.filter_by(id=sheet_id).first()

    if sheet is None:
        flash("Подборка не найдена", "error")
        return redirect(f"/pool/{pool_hashed_id}/sheets")

    db.session.delete(sheet)
    db.session.commit()
    return render_template(
        "pool/pool_sheetlist.html",
        current_pool=pool,
        title=f"{pool.name} - подборки",
    )


# -----------------------------------------------------------------------------------------------------------------------------


# show and edit sheet in pool
@pool.route("/pool/<pool_hashed_id>/sheet/<sheet_id>", methods=["GET", "POST"])
@login_required
def sheet(pool_hashed_id, sheet_id):
    pool = Pool.query.filter_by(hashed_id=pool_hashed_id).first()

    if pool is None:
        flash("Пул с таким id не найден", "error")
        return redirect("/myprofile")

    user_checked = check_user_in_pool(current_user, pool)
    if user_checked is not None:
        return redirect(user_checked)

    sheet = Sheet.query.filter_by(id=sheet_id).first()

    if sheet is None:
        flash("Подборка не найдена", "error")
        return redirect(f"/pool/{pool_hashed_id}/sheets")

    if request.method == "POST":
        if request.form.get("save_sheet") is not None:
            name = request.form.get("name")
            text = request.form.get("text")

            if not sheet.is_public:
                sheet.name = name
                sheet.text = text

            db.session.commit()


            form = request.form.to_dict()
            print(form)

            new_tags_names = []
            for key, value in form.items():
                if key[:4] == "tag ":
                    new_tags_names.append(value)
            
            sheet.act_set_tags(new_tags_names)

            for attachment in sheet.get_attachments():
                print(attachment.db_filename)
                short_name = request.form.get("attachment_name " + str(attachment.db_filename))
                if not sheet.is_public:
                    if short_name is None:
                        attachment.remove()
                        continue

                if not sheet.is_public:
                    attachment.short_name = short_name

            db.session.commit()

            print(sheet.get_attachments())

            flash("Подборка успешно сохранена", "success")
            return redirect(f"/pool/{pool_hashed_id}/sheet/{sheet_id}")
    return render_template(
        "pool/pool_1sheet.html",
        current_pool=pool,
        current_sheet=sheet,
        title=f"Редактор - {sheet.name}",
        all_tags=sorted(Tag.query.all(), key=lambda x: x.name.lower()),
    )


# add attachment to sheet
@pool.route(
    "/pool/<pool_hashed_id>/sheet/<sheet_id>/upload_file", methods=["POST"]
)
@login_required
def upload_file_to_sheet(pool_hashed_id, sheet_id):
    pool = Pool.query.filter_by(hashed_id=pool_hashed_id).first()

    if pool is None:
        flash("Пул с таким id не найден", "error")
        return redirect("/myprofile")

    user_checked = check_user_in_pool(current_user, pool)
    if user_checked is not None:
        return redirect(user_checked)

    sheet = Sheet.query.filter_by(id=sheet_id).first()
    if sheet is None:
        flash("Подборка не найдена", "error")
        return redirect(f"/pool/{pool_hashed_id}/sheets")

    file = request.files.get("file")
    if file is None:
        flash("Файл не был загружен", "error")
        return redirect(f"/pool/{pool_hashed_id}/sheet/{sheet_id}")
    
    if not sheet.is_public:
        directory = "app/database/attachments/problems"
        filenames = safe_image_upload(
            [file], directory, 5 * 1024 * 1024
        )

        filename = filenames[0]

        if filename is None:
            flash("Ошибка при загрузке", "error")
            return redirect(f"/pool/{pool_hashed_id}/sheet/{sheet_id}")
        
        attachment = Attachment(
            db_folder=directory,
            db_filename=filename,
            short_name="Рисунок",
            parent_type=DbParent.fromType(type(sheet)),
            parent_id=sheet.id,
            other_data={}
        )
        db.session.add(attachment)

        db.session.commit()

        return f"OK {attachment.db_filename}"
    
    return redirect(f"/pool/{pool_hashed_id}/sheet/{sheet_id}")

# maybe something else with sheets


# =============================================================================================================================

# --> Contests
# list all contests in pool
@pool.route("/pool/<pool_hashed_id>/contests", methods=["GET", "POST"])
@login_required
def pool_contests(pool_hashed_id):
    pool = Pool.query.filter_by(hashed_id=pool_hashed_id).first()

    if pool is None:
        flash("Пул с таким id не найден", "error")
        return redirect("/myprofile")

    user_checked = check_user_in_pool(current_user, pool)
    if user_checked is not None:
        return redirect(user_checked)

    if request.method == "POST":
        if request.form.get("back_to_pool") is not None:
            contest_id = request.form.get("contest_id")
            contest = Contest.query.filter_by(id=contest_id).first()
            contest.is_public = False
            db.session.commit()
            return redirect(f"/pool/{pool_hashed_id}/contest/{contest_id}")
    print("OK")
    return render_template(
        "pool/pool_contests.html", current_pool=pool, title=f"{pool.name} - контесты"
    )

# create new contest in pool
@pool.route("/pool/<pool_hashed_id>/new_contest", methods=["POST"])
@login_required
def new_contest(pool_hashed_id):
    pool = Pool.query.filter_by(hashed_id=pool_hashed_id).first()

    if pool is None:
        flash("Пул с таким id не найден", "error")
        return redirect("/myprofile")

    user_checked = check_user_in_pool(current_user, pool)
    if user_checked is not None:
        return redirect(user_checked)

    
    contest = pool.new_contest()

    return redirect(f"/pool/{pool_hashed_id}/contest/{contest.id}")


# show and edit contest in pool
@pool.route("/pool/<pool_hashed_id>/contest/<contest_id>", methods=["GET", "POST"])
@login_required
def contest(pool_hashed_id, contest_id):
    pool = Pool.query.filter_by(hashed_id=pool_hashed_id).first()

    if pool is None:
        flash("Пул с таким id не найден", "error")
        return redirect("/myprofile")

    user_checked = check_user_in_pool(current_user, pool)
    if user_checked is not None:
        return redirect(user_checked)

    contest = Contest.query.filter_by(id=contest_id).first()

    if contest is None:
        flash("Контест не найден", "error")
        return redirect(f"/pool/{pool_hashed_id}/contests")

    if request.method == "POST":
        if request.form.get("save_contest") is not None:
            name = request.form.get("name")
            description = request.form.get("description")
            try:
                start_date = datetime.datetime.strptime(request.form.get("start_date"), '%Y-%m-%dT%H:%M')
            except:
                start_date = None
            try:
                end_date = datetime.datetime.strptime(request.form.get("end_date"), '%Y-%m-%dT%H:%M')
            except:
                end_date = None
            print(start_date.isoformat())

            if not contest.is_public:
                contest.name = name
                contest.description = description
            
            if start_date and end_date and start_date <= end_date:
                contest.start_date = start_date
                contest.end_date = end_date

            db.session.commit()


            form = request.form.to_dict()
            print(form)

            new_tags_names = []
            for key, value in form.items():
                if key[:4] == "tag ":
                    new_tags_names.append(value)
            
            contest.act_set_tags(new_tags_names)

            hashes = request.form.getlist("problem_hash")
            scores = request.form.getlist("max_score")
            contest.act_set_problems(hashes, scores)

            judge_names = request.form.getlist("judge_name")
            contest.act_set_judges(judge_names)

            is_rating_public = request.form.get("is_rating_public")
            contest.act_toggle_rating(is_rating_public)
            

            flash("Контест успешно сохранён", "success")
            return redirect(f"/pool/{pool_hashed_id}/contest/{contest_id}")
    print(contest.start_date.isoformat())
    return render_template(
        "pool/pool_1contest.html",
        current_pool=pool,
        current_contest=contest,
        title=f"Редактор - {contest.name}",
        all_tags=sorted(Tag.query.all(), key=lambda x: x.name.lower()),
    )


# delete contest from pool
@pool.route("/remove_contest_from_pool", methods=["POST"])
@login_required
def remove_contest_from_pool():
    data = request.get_json()
    pool_hashed_id = data["pool"]
    contest_id = data["contest"]
    pool = Pool.query.filter_by(hashed_id=pool_hashed_id).first()

    if pool is None:
        flash("Пул с таким id не найден", "error")
        return redirect("/myprofile")

    user_checked = check_user_in_pool(current_user, pool)
    if user_checked is not None:
        return redirect(user_checked)

    contest = Contest.query.filter_by(id=contest_id).first()

    if contest is None:
        flash("Контест не найден", "error")
        return redirect(f"/pool/{pool_hashed_id}/contests")

    db.session.delete(contest)
    db.session.commit()
    return render_template(
        "pool/pool_contestlist.html",
        current_pool=pool,
        title=f"{pool.name} - контесты",
    )

# =============================================================================================================================



# --> Pool invitations


# accept pool invitation (answer to JS request)
@pool.route("/accept_pool_invitation", methods=["POST"])
@login_required
def accept_pool_invitation():
    data = request.get_json()
    pool_hashed_id = data["pool_hashed_id"]

    pool = Pool.query.filter_by(hashed_id=pool_hashed_id).first()

    if pool is None:
        flash("Пул с таким id не найден", "error")
        return redirect("/myprofile")

    relation = User_Pool.query.filter_by(
        user_id=current_user.id, pool_id=pool.id
    ).first()

    if relation is None:
        return "user not invited"

    relation.act_accept_invitation()
    
    print("DONE")

    return render_template("profile/profile_pools_table.html")


# -----------------------------------------------------------------------------------------------------------------------------


# decline pool invitation (answer to JS request)
@pool.route("/decline_pool_invitation", methods=["POST"])
@login_required
def decline_pool_invitation():
    data = request.get_json()
    pool_hashed_id = data["pool_hashed_id"]

    pool = Pool.query.filter_by(hashed_id=pool_hashed_id).first()

    if pool is None:
        flash("Пул с таким id не найден", "error")
        return redirect("/myprofile")

    relation = User_Pool.query.filter_by(
        user_id=current_user.id, pool_id=pool.id
    ).first()

    if relation is None:
        return "user not invited"

    db.session.delete(relation)
    db.session.commit()

    return render_template("profile/profile_pools_table.html")


# =============================================================================================================================


# --> Pool create


# create new pool
@pool.route("/pool/create", methods=["POST", "GET"])
@login_required
def create_new_pool():
    if request.method == "POST":
        create = request.form.get("create", False)
        join = request.form.get("join", False)
        name = request.form.get("name", "")
        code = request.form.get("code", "").strip()
        if (create):
            if name is None or name == "":
                flash("Необходимо указать название пула", "warning")
                return render_template("pool/pool_create.html", title=f"Создание пула", name=name, code=code)
            pool = Pool(name=name)
            pool.add()
            pool.act_add_user(user=current_user, role=Owner)
            flash("Пул успешно создан", "success")
            return redirect(f"/pool/{pool.hashed_id}/problems")
        elif (join):
            Invite.act_refresh_all()
            if code is None or code == "":
                flash("Необходимо указать код-приглашение", "warning")
                return render_template("pool/pool_create.html", title=f"Создание пула", name=name, code=code)
            i = Invite.query.filter_by(code=code).first()
            if i is None:
                flash("Код-приглашение не действителен", "error")
                return render_template("pool/pool_create.html", title=f"Создание пула", name=name, code=code)
            pool = i.get_parent()
            if type(pool) != Pool:
                flash("Код-приглашение не действителен", "error")
                return render_template("pool/pool_create.html", title=f"Создание пула", name=name, code=code)
            pool.act_add_user_by_invite(current_user, i)
            flash("Вы присоединились к пулу", "success")
            return redirect(f"/pool/{pool.hashed_id}/problems")

        

    return render_template("pool/pool_create.html", title=f"Создание пула")


# =============================================================================================================================


# --> Pool participants


# show pool participants (for everyone)
@pool.route("/pool/<pool_hashed_id>/participants", methods=["GET", "POST"])
@login_required
def pool_participants(pool_hashed_id):
    pool = Pool.query.filter_by(hashed_id=pool_hashed_id).first()
    if pool is None:
        flash("Пул с таким id не найден", "error")
        return redirect("/myprofile")

    user_checked = check_user_in_pool(current_user, pool)
    if user_checked is not None:
        return redirect(user_checked)

    if request.method == "POST":
        if request.form.get("leave_pool") is not None:
            user_relation = current_user.get_pool_relation(pool.id)
            if user_relation is None:
                flash("Такого пользователя нет в пуле", "error")
                return redirect(
                    url_for("pool.pool_participants", pool_hashed_id=pool_hashed_id)
                )
            if user_relation.role.isOwner() and pool.count_owners() == 1:
                flash(
                    "Вы единственный владелец, сначала удалите пул",
                    "error",
                )
                return redirect(
                    url_for("pool.pool_participants", pool_hashed_id=pool_hashed_id)
                )
            db.session.delete(user_relation)
            db.session.commit()
            flash(f"Вы вышли из пула", "success")
            return redirect("/myprofile")

    return render_template(
        "pool/pool_participants.html",
        current_pool=pool,
        title=f"{pool.name} - участники",
    )


# =============================================================================================================================


# --> Pool management


# redirect to pool/management/general
@pool.route("/pool/<pool_hashed_id>/management")
@login_required
def pool_manager(pool_hashed_id):  # ok
    return redirect(f"/pool/{pool_hashed_id}/management/general")


# -----------------------------------------------------------------------------------------------------------------------------


# Pool management - general
@pool.route("/pool/<pool_hashed_id>/management/general", methods=["GET", "POST"])
@login_required
def pool_manager_general(pool_hashed_id):
    pool = Pool.query.filter_by(hashed_id=pool_hashed_id).first()
    if pool is None:
        flash("Пул с таким id не найден", "error")
        return redirect("/myprofile")
    if not pool.is_my():
        flash("Вы не состоите в этом пуле", "error")
        return redirect("/profile/pools")
    if not current_user.get_pool_relation(pool.id).role.isOwner():
        flash("Недостаточно прав", "error")
        return redirect(f"/pool/{pool_hashed_id}/chats")

    if request.method == "POST":
        if request.form.get("pool_name") is not None:
            print(type(request.form.get("pool_name")))
            pool.name = request.form.get("pool_name")
            db.session.commit()
            print(pool.name)
            flash("Имя пула успешно изменено", "success")
            return redirect(
                url_for("pool.pool_manager_general", pool_hashed_id=pool_hashed_id)
            )
        if request.form.get("delete_pool") is not None:
            for relation in User_Pool.query.filter_by(pool_id=pool.id).all():
                db.session.delete(relation)
            for problem in Problem.query.filter_by(pool_id=pool.id).all():
                db.session.delete(problem)
            db.session.delete(pool)
            db.session.commit()
            flash("Пул успешно удален", "success")
            return redirect("/myprofile")

    return render_template(
        "pool/pool_management_general.html",
        current_pool=pool,
        title=f"{pool.name} - управление",
    )


# -----------------------------------------------------------------------------------------------------------------------------


# Pool management - collaborators
@pool.route("/pool/<pool_hashed_id>/management/collaborators", methods=["GET", "POST"])
@login_required
def pool_collaborators(pool_hashed_id):
    pool = Pool.query.filter_by(hashed_id=pool_hashed_id).first()
    if pool is None:
        flash("Пул с таким id не найден", "error")
        return redirect("/myprofile")
    if not pool.is_my():
        flash("Вы не состоите в этом пуле", "error")
        return redirect("/profile/pools")
    if not current_user.get_pool_relation(pool.id).role.isOwner():
        flash("Недостаточно прав", "error")
        return redirect(f"/pool/{pool_hashed_id}/chats")
    

    if request.method == "POST":
        if request.form.get("upgrade_to_owner") is not None:
            user_id = request.form.get("upgrade_to_owner")
            user = User.query.filter_by(id=user_id).first()
            if user is None:
                flash("Пользователь не найден", "error")
                return redirect(url_for("pool.pool_collaborators", pool_hashed_id=pool_hashed_id))
            user_relation = user.get_pool_relation(pool.id)
            if user_relation is None:
                flash("Такого пользователя нет в пуле", "error")
                return redirect(url_for("pool.pool_collaborators", pool_hashed_id=pool_hashed_id))
            if user_relation.role.isOwner():
                flash("Пользователь уже владелец пула", "warning")
                return redirect(url_for("pool.pool_collaborators", pool_hashed_id=pool_hashed_id))
            if user_relation.role.isInvited():
                flash("Передать права владельца можно только участнику", "warning")
                return redirect(url_for("pool.pool_collaborators", pool_hashed_id=pool_hashed_id))
            user_relation.role = Owner
            db.session.commit()
            flash(f"Права владельца успешно выданы пользователю {user.name}", "success")
            return redirect(url_for("pool.pool_collaborators", pool_hashed_id=pool_hashed_id))

        elif request.form.get("downgrade_to_participant") is not None:
            user_id = request.form.get("downgrade_to_participant")
            user = User.query.filter_by(id=user_id).first()
            if user is None:
                flash("Пользователь не найден", "error")
                return redirect(url_for("pool.pool_collaborators", pool_hashed_id=pool_hashed_id))
            user_relation = user.get_pool_relation(pool.id)
            if user_relation is None:
                flash("Такого пользователя нет в пуле", "error")
                return redirect(url_for("pool.pool_collaborators", pool_hashed_id=pool_hashed_id))
            if user_relation.role.isParticipant():
                flash("Пользователь уже участник пула", "warning")
                return redirect(url_for("pool.pool_collaborators", pool_hashed_id=pool_hashed_id))
            if user_relation.role.isInvited():
                flash("Понизить до участника можно только владельца", "warning")
                return redirect(url_for("pool.pool_collaborators", pool_hashed_id=pool_hashed_id))
            if user.id == current_user.id and pool.count_owners() == 1:
                flash("Вы единственный владелец пула, понижение невозможно", "warning")
                return redirect(url_for("pool.pool_collaborators", pool_hashed_id=pool_hashed_id))
            user_relation.role = Participant
            db.session.commit()
            flash(f"Пользователь {user.name} успешно понижен до участника", "success")
            return redirect(url_for("pool.pool_collaborators", pool_hashed_id=pool_hashed_id))

        elif request.form.get("remove_participant") is not None:
            user_id = request.form.get("remove_participant")
            user = User.query.filter_by(id=user_id).first()
            if user is None:
                flash("Пользователь не найден", "error")
                return redirect(url_for("pool.pool_collaborators", pool_hashed_id=pool_hashed_id))
            user_relation = user.get_pool_relation(pool.id)
            if user_relation is None:
                flash("Такого пользователя нет в пуле", "error")
                return redirect(url_for("pool.pool_collaborators", pool_hashed_id=pool_hashed_id))
            if user_id == current_user.id:
                flash("Вы не можете удалить себя из пула на этой странице", "error")
                return redirect(url_for("pool.pool_collaborators", pool_hashed_id=pool_hashed_id))
            if user_relation.role.isOwner():
                flash("Удалить владельца невозможно, сначала понизьте его до участника")
                return redirect(url_for("pool.pool_collaborators", pool_hashed_id=pool_hashed_id))
            db.session.delete(user_relation)
            db.session.commit()
            flash(f"Пользователь {user.name} успешно удалён", "success")
            return redirect(url_for("pool.pool_collaborators", pool_hashed_id=pool_hashed_id))
        elif request.form.get("new_invite_code") is not None:
            pool.act_generate_new_invite_code()
            return redirect(url_for("pool.pool_collaborators", pool_hashed_id=pool_hashed_id))

    return render_template("pool/pool_management_collaborators.html", current_pool=pool, title=f"{pool.name} - управление участниками")
