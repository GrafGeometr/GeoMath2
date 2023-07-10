from .imports import *
from .model_imports import *

contest = Blueprint('contest', __name__)

@contest.route("/contest/<contest_id>", methods=["GET", "POST"])
@login_required
def contest_mainpage(contest_id):
    contest = Contest.get_by_id(contest_id)
    if (contest is None) or (not contest.is_description_available()):
        return redirect("/myprofile")
    if request.method == "POST":
        if request.form.get("register") is not None:
            mode = request.form.get("register")
            start_date = request.form.get("start_date")
            end_date = request.form.get("end_date")
            contest.act_register(mode=mode, start_date=start_date, end_date=end_date)
            if mode == "virtual":
                return f"/contest/{contest_id}"
        if request.form.get("stop") is not None:
            contest.act_stop()
        return redirect(f"/contest/{contest_id}")
    return render_template("contest/contest_mainpage.html", current_contest=contest, title=f"Контест - {contest.name}")

@contest.route("/contest/<contest_id>/problem/<problem_hashed_id>", methods=["GET", "POST"])
@login_required
def contest_problem(contest_id, problem_hashed_id):
    contest = Contest.get_by_id(contest_id)
    problem = Problem.get_by_hashed_id(problem_hashed_id)
    if (contest is None) or (not contest.is_description_available()):
        return redirect("/myprofile")

    cp = Contest_Problem.get_by_contest_and_problem(contest, problem)
    if (cp is None) or (not cp.is_accessible()):
        print("cp is none")
        return redirect(f"/contest/{contest_id}")

    idx = contest.get_idx_by_contest_problem(cp)
    if idx is None:
        print("idx is none")
        return redirect(f"/contest/{contest_id}")
    
    cus = cp.get_active_contest_user_solution()

    if request.method == "POST":
        if cus is None:
            return redirect(f"/contest/{contest_id}/problem/{problem_hashed_id}")
        if request.form.get("save_solution") is not None:
            content = request.form.get("content")
            cus.act_set_content(content)

            for attachment in cus.get_attachments():
                short_name = request.form.get("attachment_name " + str(attachment.db_filename))
                if short_name is None:
                    attachment.remove()
                    continue

                attachment.short_name = short_name

            db.session.commit()

            flash("Решение успешно сохранено", "success")
            return redirect(f"/contest/{contest_id}/problem/{problem_hashed_id}")

    return render_template("contest/contest_problem.html", current_contest=contest, current_cp=cp, current_cus=cus, title=f"{contest.name} - №{idx}")


@contest.route("/contest/<contest_id>/problem/<problem_hashed_id>/upload_file", methods=["POST"])
@login_required
def upload_file_to_cus(contest_id, problem_hashed_id):
    contest = Contest.get_by_id(contest_id)
    problem = Problem.get_by_hashed_id(problem_hashed_id)
    if (contest is None) or (not contest.is_description_available()):
        return redirect("/myprofile")

    cp = Contest_Problem.get_by_contest_and_problem(contest, problem)
    if (cp is None) or (not cp.is_accessible()):
        return redirect(f"/contest/{contest_id}")

    idx = contest.get_idx_by_contest_problem(cp)
    if idx is None:
        return redirect(f"/contest/{contest_id}")
    
    cus = cp.get_active_contest_user_solution()
    if cus is None:
        return redirect(f"/contest/{contest_id}/problem/{problem_hashed_id}")

    file = request.files.get("file")
    if file is None:
        flash("Файл не был загружен", "error")
        return redirect(f"/contest/{contest_id}/problem/{problem_hashed_id}")
    
    directory = "app/database/attachments/problems"
    filenames = safe_image_upload([file], directory, 5 * 1024 * 1024)

    filename = filenames[0]

    if filename is None:
        flash("Ошибка при загрузке", "error")
        return redirect(f"/contest/{contest_id}/problem/{problem_hashed_id}")
    
    attachment = Attachment(
        db_folder=directory,
        db_filename=filename,
        short_name="Рисунок",
        parent_type=DbParent.fromType(type(cus)),
        parent_id=cus.id,
        other_data={}
    )
    attachment.add()

    return f"OK {attachment.db_filename}"

@contest.route("/contest/<contest_id>/solution/<solution_hashed_id>", methods=["GET", "POST"])
@login_required
def contest_solution(contest_id, solution_hashed_id):
    contest = Contest.get_by_id(contest_id)
    solution = Contest_User_Solution.get_by_hashed_id(solution_hashed_id)
    if (contest is None) or (not contest.is_description_available()):
        return redirect("/myprofile")
    if (solution is None) or (not solution.is_available()):
        return redirect(f"/contest/{contest_id}")
    if request.method == "POST":
        if request.form.get("save_comment") is not None:
            judge_comment = request.form.get("judge_comment")
            solution.act_set_judge_comment(judge_comment)
            score = request.form.get("score")
            solution.act_set_score(score)

            flash("Проверка успешно сохранена", "success")
        return redirect(f"/contest/{contest_id}/solution/{solution_hashed_id}")
    return render_template("contest/contest_solution.html", current_contest=contest,
                           current_solution=solution, title=f"{solution.contest_user.user.name} - решение",
                           str_from_dt = str_from_dt)

@contest.route("/contest/<contest_id>/rating/<string:mode>/<string:part>", methods=["GET"])
@login_required
def contest_rating(contest_id, mode, part):
    contest = Contest.get_by_id(contest_id)
    if (contest is None) or (not contest.is_description_available()):
        return redirect("/myprofile")
    if mode not in ["all", "my"]:
        return redirect(f"/contest/{contest_id}")
    if part not in ["real", "virtual"]:
        return redirect(f"/contest/{contest_id}")
    all_cu = contest.get_cu_by_mode_and_part(mode, part)
    table = contest.get_rating_table(all_cu)
    return render_template("contest/contest_rating.html", current_contest=contest, title=f"{contest.name} - рейтинг",
                           mode=mode, part=part, rating_table=table, str_from_dt = str_from_dt)