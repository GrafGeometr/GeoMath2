from .imports import *
from .model_imports import *

contest = Blueprint('contest', __name__)

@contest.route("/contest/<contest_id>", methods=["GET", "POST"])
@login_required
def contest_mainpage(contest_id):
    contest = Contest.get_by_id(contest_id)
    if (contest is None) or (not contest.is_archived()):
        return redirect("/myprofile")
    if request.method == "POST":
        if request.form.get("register") is not None:
            mode = request.form.get("register")
            start_date = request.form.get("start_date")
            end_date = request.form.get("end_date")
            contest.act_register(mode=mode, start_date=start_date, end_date=end_date)
        if request.form.get("stop") is not None:
            contest.act_stop_for_user()
        return redirect(f"/contest/{contest_id}")
    return render_template("contest/contest_mainpage.html", current_contest=contest, title=f"Контест - {contest.name}")

@contest.route("/contest/<contest_id>/problem/<problem_hashed_id>", methods=["GET", "POST"])
@login_required
def contest_problem(contest_id, problem_hashed_id):
    contest = Contest.get_by_id(contest_id)
    problem = Problem.get_by_hashed_id(problem_hashed_id)
    if (contest is None) or (not contest.is_archived()):
        return redirect("/myprofile")

    cp = Contest_Problem.get_by_contest_and_problem(contest, problem)
    if (cp is None) or (not cp.is_accessible()):
        return redirect(f"/contest/{contest_id}")

    idx = contest.get_idx_by_contest_problem(cp)
    if idx is None:
        return redirect(f"/contest/{contest_id}")
    
    cus = cp.get_active_contest_user_solution()

    if request.method == "POST":
        if cus is None:
            return redirect(f"/contest/{contest_id}/problem/{problem_hashed_id}")
        if request.form.get("save_solution") is not None:
            content = request.form.get("content")
            cus.act_update_content(content)


            form = request.form.to_dict()
            print(form)

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

    return render_template("contest/contest_problem.html", current_contest=contest, current_cp=cp, current_cus=cus, title=f"{contest.name} - №{idx}")


@contest.route("/contest/<contest_id>/solution/<solution_hashed_id>", methods=["GET", "POST"])
@login_required
def contest_solution(contest_id, solution_hashed_id):
    contest = Contest.get_by_id(contest_id)
    solution = Contest_User_Solution.get_by_hashed_id(solution_hashed_id)
    if (contest is None) or (not contest.is_archived()):
        return redirect("/myprofile")
    if solution is None:
        return redirect(f"/contest/{contest_id}")
    if request.method == "POST":
        return redirect(f"/contest/{contest_id}/solution/{solution_hashed_id}")
    return render_template("contest/contest_solution.html", current_contest=contest, current_solution=solution, title=f"{solution.contest_user.user.name} - решение")