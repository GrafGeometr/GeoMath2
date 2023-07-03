from .imports import *
from .model_imports import *

pool = Blueprint("pool", __name__)


# --> Pools access checking


# check if user is in pool
def check_user_in_pool(user, pool):
    if user.get_pool_relation(pool.id) is None:
        flash("Вы не можете просматривать этот пул", "danger")
        return "/myprofile"
    if user.get_pool_relation(pool.id).role.isInvited():
        flash("Вы не приняли приглашение в этот пул", "danger")
        return f"/profile/{user.name}/pools"
    return None


# -----------------------------------------------------------------------------------------------------------------------------


# check if user is allowed to manage pool (owner)
def check_management_access(user, pool):
    if user.get_pool_relation(pool.id).role.isOwner():
        return None
    flash("Вы не можете управлять этим пулом", "danger")
    return url_for("pool.pool_participants", pool_hashed_id=pool.hashed_id)


# =============================================================================================================================


# --> Pool problems


# list of problems in pool
@pool.route("/pool/<pool_hashed_id>/problems", methods=["GET", "POST"])
@login_required
def pool_problems(pool_hashed_id):
    pool = Pool.query.filter_by(hashed_id=pool_hashed_id).first()

    if pool is None:
        flash("Пул с таким id не найден", "danger")
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
        flash("Пул с таким id не найден", "danger")
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
        flash("Пул с таким id не найден", "danger")
        return redirect("/myprofile")

    user_checked = check_user_in_pool(current_user, pool)
    if user_checked is not None:
        return redirect(user_checked)

    problem = Problem.query.filter_by(hashed_id=problem_hashed_id).first()

    if problem is None:
        flash("Задача не найдена", "danger")
        return redirect(f"/pool/{pool_hashed_id}/problems")

    db.session.delete(problem)
    db.session.commit()
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
        flash("Пул с таким id не найден", "danger")
        return redirect("/myprofile")

    user_checked = check_user_in_pool(current_user, pool)
    if user_checked is not None:
        return redirect(user_checked)

    problem = Problem.query.filter_by(hashed_id=problem_hashed_id).first()
    if problem is None:
        flash("Задача не найдена", "danger")
        return redirect(f"/pool/{pool_hashed_id}/problems")

    file = request.files.get("file")
    if file is None:
        flash("Файл не был загружен", "danger")
        return redirect(f"/pool/{pool_hashed_id}/problem/{problem_hashed_id}")
    
    if not problem.is_public:
        directory = "app/database/attachments/problems"
        filenames = safe_image_upload(
            [file], directory, 5 * 1024 * 1024
        )

        filename = filenames[0]

        if filename is None:
            flash("Ошибка при загрузке", "danger")
            return redirect(f"/pool/{pool_hashed_id}/problem/{problem_hashed_id}")
        
        attachment = Attachment(
            db_folder=directory,
            db_filename=filename,
            short_name="Рисунок",
            parent_type="Problem",
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
        flash("Пул с таким id не найден", "danger")
        return redirect("/myprofile")

    user_checked = check_user_in_pool(current_user, pool)
    if user_checked is not None:
        return redirect(user_checked)

    problem = Problem.query.filter_by(hashed_id=problem_hashed_id).first()

    if problem is None:
        flash("Задача не найдена", "danger")
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

            for key, value in form.items():
                if key[:4] == "tag ":
                    print(key, value)
                    tag = Tag.query.filter_by(name=value).first()
                    print(1)
                    if tag is None:
                        tag = Tag(name=value)
                        db.session.add(tag)
                        db.session.commit()
                    if (Tag_Relation.query.filter_by(parent_type="Problem", parent_id=problem.id, tag_id=tag.id).first() is None):
                        tag_relation = Tag_Relation(parent_type="Problem", parent_id=problem.id, tag_id=tag.id)
                        db.session.add(tag_relation)
                        db.session.commit()

            for tag in problem.get_tags():
                if form.get(f"tag {tag.name}", None) is None:
                    db.session.delete(Tag_Relation.query.filter_by(parent_type="Problem", parent_id=problem.id, tag_id=tag.id).first())
                    db.session.commit()

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
def get_problem_content(problem_hashed_id):
    print(problem_hashed_id)
    problem = Problem.query.filter_by(hashed_id=problem_hashed_id).first()
    if problem is None:
        print("problem none")
        return
    
    # if problem is archived
    if problem.is_public and problem.moderated:
        return json.dumps(
            { 'name': problem.name
            , 'statement': problem.statement
            , 'solution': problem.solution if problem.show_solution else "Решение скрыто"
            , 'files': [[file.preview_name, file.db_filename] for file in problem.get_attachments() if file.other_data.get("is_secret", False)]
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
        , 'files': [[file.short_name, file.db_filename] for file in problem.get_attachments()]
        , 'tags': [tag.name for tag in problem.get_tags()]
        }
    )


# -----------------------------------------------------------------------------------------------------------------------------


# get problem image
@pool.route("/get_image/<db_filename>", methods=["GET", "POST"])
def get_image(db_filename):
    if not current_user.is_authenticated:
        print("not authenticated")
        return
    attachment = Attachment.query.filter_by(db_filename=db_filename).first()
    if attachment is None:
        print("attachment none")
        return
    parent = attachment.get_parent()
    if parent is None:
        print("parent none")
        return
    if parent.pool is not None:
        relation = current_user.get_pool_relation(parent.pool_id)
        if not parent.is_archived() and relation is None:
            print("user not in pool")
            return
    try:
        print(attachment.db_folder.split("app/")[1], db_filename)
        return send_from_directory(
            os.path.join(basedir, attachment.db_folder.split("app/")[1]),
            db_filename,
            as_attachment=True,
        )
    except Exception as e:
        print(e)


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
    attachment = Attachment.query.filter_by(
        parent_type="problem", parent_id=problem.id, db_filename=filename
    ).first()
    if attachment is None:
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
        flash("Пул с таким id не найден", "danger")
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
        flash("Пул с таким id не найден", "danger")
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
        flash("Пул с таким id не найден", "danger")
        return redirect("/myprofile")

    user_checked = check_user_in_pool(current_user, pool)
    if user_checked is not None:
        return redirect(user_checked)

    sheet = Sheet.query.filter_by(id=sheet_id).first()

    if sheet is None:
        flash("Подборка не найдена", "danger")
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
        flash("Пул с таким id не найден", "danger")
        return redirect("/myprofile")

    user_checked = check_user_in_pool(current_user, pool)
    if user_checked is not None:
        return redirect(user_checked)

    sheet = Sheet.query.filter_by(id=sheet_id).first()

    if sheet is None:
        flash("Подборка не найдена", "danger")
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

            for key, value in form.items():
                if key[:4] == "tag ":
                    print(key, value)
                    tag = Tag.query.filter_by(name=value).first()
                    print(1)
                    if tag is None:
                        tag = Tag(name=value)
                        db.session.add(tag)
                        db.session.commit()
                    if (Tag_Relation.query.filter_by(parent_type="Sheet", parent_id=sheet.id, tag_id=tag.id).first() is None):
                        tag_relation = Tag_Relation(parent_type="Sheet", parent_id=sheet.id, tag_id=tag.id)
                        db.session.add(tag_relation)
                        db.session.commit()

            for tag in sheet.get_tags():
                if form.get(f"tag {tag.name}", None) is None:
                    db.session.delete(Tag_Relation.query.filter_by(parent_type="Sheet", parent_id=sheet.id, tag_id=tag.id).first())
                    db.session.commit()

            for attachment in sheet.get_attachments():
                print(attachment.db_filename)
                short_name = request.form.get("attachment_name " + str(attachment.db_filename))
                if not sheet.is_public:
                    if short_name is None:
                        attachment.remove()
                        continue

                if not sheet.is_public:
                    attachment.short_name = short_name
                show = request.form.get("secret_attachment " + str(attachment.db_filename))
                if show == "on":
                    attachment.other_data["is_secret"] = True
                else:
                    attachment.other_data["is_secret"] = False
                print(attachment.id, show)

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
        flash("Пул с таким id не найден", "danger")
        return redirect("/myprofile")

    user_checked = check_user_in_pool(current_user, pool)
    if user_checked is not None:
        return redirect(user_checked)

    sheet = Sheet.query.filter_by(id=sheet_id).first()
    if sheet is None:
        flash("Подборка не найдена", "danger")
        return redirect(f"/pool/{pool_hashed_id}/sheets")

    file = request.files.get("file")
    if file is None:
        flash("Файл не был загружен", "danger")
        return redirect(f"/pool/{pool_hashed_id}/sheet/{sheet_id}")
    
    if not sheet.is_public:
        directory = "app/database/attachments/problems"
        filenames = safe_image_upload(
            [file], directory, 5 * 1024 * 1024
        )

        filename = filenames[0]

        if filename is None:
            flash("Ошибка при загрузке", "danger")
            return redirect(f"/pool/{pool_hashed_id}/sheet/{sheet_id}")
        
        attachment = Attachment(
            db_folder=directory,
            db_filename=filename,
            short_name="Рисунок",
            parent_type="Sheet",
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
        flash("Пул с таким id не найден", "danger")
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
        flash("Пул с таким id не найден", "danger")
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
        flash("Пул с таким id не найден", "danger")
        return redirect("/myprofile")

    user_checked = check_user_in_pool(current_user, pool)
    if user_checked is not None:
        return redirect(user_checked)

    contest = Contest.query.filter_by(id=contest_id).first()

    if contest is None:
        flash("Контест не найден", "danger")
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
            
            if start_date:
                contest.start_date = start_date
            if end_date:
                contest.end_date = end_date

            db.session.commit()


            form = request.form.to_dict()
            print(form)

            for key, value in form.items():
                if len(key) >= 4 and key[:4] == "tag ":
                    print(key, value)
                    tag = Tag.query.filter_by(name=value).first()
                    print(1)
                    if tag is None:
                        tag = Tag(name=value)
                        db.session.add(tag)
                        db.session.commit()
                    if (Tag_Relation.query.filter_by(parent_type="Contest", parent_id=contest.id, tag_id=tag.id).first() is None):
                        tag_relation = Tag_Relation(parent_type="Contest", parent_id=contest.id, tag_id=tag.id)
                        db.session.add(tag_relation)
                        db.session.commit()
            for tag in contest.get_tags():
                if form.get(f"tag {tag.name}", None) is None:
                    db.session.delete(Tag_Relation.query.filter_by(parent_type="Contest", parent_id=contest.id, tag_id=tag.id).first())
                    db.session.commit()

            hashes = request.form.getlist("problem_hash")
            problems = [Problem.query.filter_by(hashed_id=hashed_id).first() for hashed_id in hashes]
            for problem in problems:
                if problem is None:
                    continue
                if Contest_Problem.query.filter_by(contest_id=contest.id, problem_id=problem.id).first() is None:
                    db.session.add(Contest_Problem(contest_id=contest.id, problem_id=problem.id))
                    db.session.commit()
            for problem in contest.get_problems():
                if problem.hashed_id not in hashes:
                    db.session.delete(Contest_Problem.query.filter_by(contest_id=contest.id, problem_id=problem.id).first())
                    db.session.commit()



            db.session.commit()

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
        flash("Пул с таким id не найден", "danger")
        return redirect("/myprofile")

    user_checked = check_user_in_pool(current_user, pool)
    if user_checked is not None:
        return redirect(user_checked)

    contest = Contest.query.filter_by(id=contest_id).first()

    if contest is None:
        flash("Контест не найден", "danger")
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
        flash("Пул с таким id не найден", "danger")
        return redirect("/myprofile")

    relation = User_Pool.query.filter_by(
        user_id=current_user.id, pool_id=pool.id
    ).first()

    if relation is None:
        return "user not invited"

    relation.role = Participant

    db.session.commit()
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
        flash("Пул с таким id не найден", "danger")
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
        name = request.form.get("name")
        print(name)
        hashed_id = current_user.create_new_pool(name)
        return redirect(f"/pool/{hashed_id}/problems")

    return render_template("pool/pool_create.html", title=f"Создание пула")


# =============================================================================================================================


# --> Pool participants


# show pool participants (for everyone)
@pool.route("/pool/<pool_hashed_id>/participants", methods=["GET", "POST"])
@login_required
def pool_participants(pool_hashed_id):
    pool = Pool.query.filter_by(hashed_id=pool_hashed_id).first()
    if pool is None:
        flash("Пул с таким id не найден", "danger")
        return redirect("/myprofile")

    user_checked = check_user_in_pool(current_user, pool)
    if user_checked is not None:
        return redirect(user_checked)

    if request.method == "POST":
        if request.form.get("leave_pool") is not None:
            user_relation = current_user.get_pool_relation(pool.id)
            if user_relation is None:
                flash("Такого пользователя нет в пуле", "danger")
                return redirect(
                    url_for("pool.pool_participants", pool_hashed_id=pool_hashed_id)
                )
            if user_relation.role.isOwner() and pool.count_owners() == 1:
                flash(
                    "Вы не можете выходить из пула, так как являетесь единственным владельцем",
                    "danger",
                )
                return redirect(
                    url_for("pool.pool_participants", pool_hashed_id=pool_hashed_id)
                )
            db.session.delete(user_relation)
            db.session.commit()
            flash(f"Пользователь {current_user.name} успешно удалён", "success")
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
        flash("Пул с таким id не найден", "danger")
        return redirect("/myprofile")

    user_checked = check_user_in_pool(current_user, pool)
    if user_checked is not None:
        return redirect(user_checked)

    management_access_checked = check_management_access(current_user, pool)
    if management_access_checked is not None:
        return redirect(management_access_checked)

    if request.method == "POST":
        print(request.form.get("pool_name"))
        if not current_user.get_pool_relation(pool.id).role.isOwner():
            print("OOPS")
            flash("Вы не имеете доступа к этой странице", "danger")
            return redirect(
                url_for("pool.pool_manager_general", pool_hashed_id=pool_hashed_id)
            )
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
        flash("Пул с таким id не найден", "danger")
        return redirect("/myprofile")

    user_checked = check_user_in_pool(current_user, pool)
    if user_checked is not None:
        return redirect(user_checked)

    management_access_checked = check_management_access(current_user, pool)
    if management_access_checked is not None:
        return redirect(management_access_checked)

    if request.method == "POST":
        if not current_user.get_pool_relation(pool.id).role.isOwner():
            flash("Вы не имеете доступа к этой странице", "danger")
            return redirect(
                url_for("pool.pool_collaborators", pool_hashed_id=pool_hashed_id)
            )
        if request.form.get("upgrade_to_owner") is not None:
            user_id = request.form.get("upgrade_to_owner")
            user = User.query.filter_by(id=user_id).first()
            if user is None:
                flash("Пользователь не найден", "danger")
                return redirect(
                    url_for("pool.pool_collaborators", pool_hashed_id=pool_hashed_id)
                )
            user_relation = user.get_pool_relation(pool.id)
            if user_relation is None:
                flash("Такого пользователя нет в пуле", "danger")
                return redirect(
                    url_for("pool.pool_collaborators", pool_hashed_id=pool_hashed_id)
                )
            if user_relation.role.isOwner():
                flash("Пользователь уже владелец пула", "warning")
                return redirect(
                    url_for("pool.pool_collaborators", pool_hashed_id=pool_hashed_id)
                )
            if user_relation.role.isInvited():
                flash("Передать права владельца можно только участнику", "warning")
                return redirect(
                    url_for("pool.pool_collaborators", pool_hashed_id=pool_hashed_id)
                )
            user_relation.role = Owner
            # current_user.get_pool_relation(pool.id).role = Participant
            db.session.commit()
            flash(
                f"Права владельца успешно переданы пользователю {user.name}", "success"
            )
            return redirect(
                url_for("pool.pool_participants", pool_hashed_id=pool_hashed_id)
            )

        elif request.form.get("downgrade_to_participant") is not None:
            user_id = request.form.get("downgrade_to_participant")
            user = User.query.filter_by(id=user_id).first()
            if user is None:
                flash("Пользователь не найден", "danger")
                return redirect(
                    url_for("pool.pool_collaborators", pool_hashed_id=pool_hashed_id)
                )
            user_relation = user.get_pool_relation(pool.id)
            if user_relation is None:
                flash("Такого пользователя нет в пуле", "danger")
                return redirect(
                    url_for("pool.pool_collaborators", pool_hashed_id=pool_hashed_id)
                )
            if user_relation.role.isParticipant():
                flash("Пользователь уже участник пула", "warning")
                return redirect(
                    url_for("pool.pool_collaborators", pool_hashed_id=pool_hashed_id)
                )
            if user_relation.role.isInvited():
                flash("Понизить до участника можно только владельца", "warning")
                return redirect(
                    url_for("pool.pool_collaborators", pool_hashed_id=pool_hashed_id)
                )
            if user.id == current_user.id and pool.count_owners() == 1:
                flash(
                    "Вы являетесь единственным владельцем пула, понижение невозможно",
                    "warning",
                )
                return redirect(
                    url_for("pool.pool_collaborators", pool_hashed_id=pool_hashed_id)
                )
            user_relation.role = Participant
            db.session.commit()
            flash(f"Пользователь {user.name} успешно понижен до участника", "success")
            return redirect(
                url_for("pool.pool_participants", pool_hashed_id=pool_hashed_id)
            )

        elif request.form.get("remove_participant") is not None:
            user_id = request.form.get("remove_participant")
            user = User.query.filter_by(id=user_id).first()
            if user is None:
                flash("Пользователь не найден", "danger")
                return redirect(
                    url_for("pool.pool_collaborators", pool_hashed_id=pool_hashed_id)
                )
            user_relation = user.get_pool_relation(pool.id)
            if user_relation is None:
                flash("Такого пользователя нет в пуле", "danger")
                return redirect(
                    url_for("pool.pool_collaborators", pool_hashed_id=pool_hashed_id)
                )
            if user_id == current_user.id:
                flash("Вы не можете удалить себя из пула на этой странице", "danger")
                return redirect(
                    url_for("pool.pool_collaborators", pool_hashed_id=pool_hashed_id)
                )
            if user_relation.role.isOwner():
                flash("Удалить владельца невозможно, сначала понизьте его до участника")
                return redirect(
                    url_for("pool.pool_collaborators", pool_hashed_id=pool_hashed_id)
                )
            db.session.delete(user_relation)
            db.session.commit()
            flash(f"Пользователь {user.name} успешно удалён", "success")
            return redirect(
                url_for("pool.pool_collaborators", pool_hashed_id=pool_hashed_id)
            )
        elif request.form.get("login1") is not None:
            print(request.form.get("login1"))

            user_name = request.form.get("login1")
            user = User.query.filter_by(name=user_name).first()

            if user is None:
                flash(f"Пользователь {user_name} не найден", "danger")
                print("Пользователь не найден")
                return redirect(
                    url_for("pool.pool_collaborators", pool_hashed_id=pool_hashed_id)
                )
            user_relation = user.get_pool_relation(pool.id)
            if user_relation is not None:
                flash(
                    f"Пользователь {user.name} уже приглашен или состоит в пуле",
                    "danger",
                )
                return redirect(
                    url_for("pool.pool_collaborators", pool_hashed_id=pool_hashed_id)
                )
            # add this user to the pool

            relation = User_Pool(user=user, pool=pool, role=Invited)
            db.session.add(relation)
            db.session.commit()
            flash(f"Пользователь {user.name} успешно приглашен", "success")
            return redirect(
                url_for("pool.pool_collaborators", pool_hashed_id=pool_hashed_id)
            )

    return render_template(
        "pool/pool_management_collaborators.html",
        current_pool=pool,
        title=f"{pool.name} - участники",
    )
