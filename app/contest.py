from .imports import *
from .model_imports import *

contest = Blueprint('contest', __name__)

@contest.route("/contest/<contest_id>", methods=["GET", "POST"])
@login_required
def contest_mainpage(contest_id):
    contest = Contest.query.filter_by(id=contest_id).first()
    if contest is None:
        return redirect("/myprofile")
    if not contest.is_public:
        return redirect(f"/myprofile")
    if request.method == "POST":
        if request.form.get("register_default") is not None:
            contest.register(virtual=False)
            return redirect(f"/contest/{contest_id}")
        if request.form.get("register_virtual") is not None:
            try:
                start_date = datetime.datetime.strptime(request.form.get("start_date"), '%Y-%m-%dT%H:%M')
            except:
                start_date = None
            try:
                end_date = datetime.datetime.strptime(request.form.get("end_date"), '%Y-%m-%dT%H:%M')
            except:
                end_date = None
            contest.register(virtual=True, virtual_start=start_date, virtual_end=end_date)
            return f"/contest/{contest_id}"
        if request.form.get("stop") is not None:
            contest.stop()
            return redirect(f"/contest/{contest_id}")
    return render_template("contest/contest_mainpage.html", current_contest=contest, title=f"Контест - {contest.name}")

@contest.route("/contest/<contest_id>/problem/<problem_hashed_id>", methods=["GET", "POST"])
@login_required
def contest_problem(contest_id, problem_hashed_id):
    contest = Contest.query.filter_by(id=contest_id).first()
    if contest is None:
        return redirect("/myprofile")
    if not contest.is_public:
        return redirect(f"/myprofile")
    problem = Problem.query.filter_by(hashed_id=problem_hashed_id).first()
    if problem is None:
        return redirect(f"/myprofile")
    problems = contest.get_nonsecret_problems()
    if problem not in problems:
        return redirect(f"/myprofile")
    idx = problems.index(problem) + 1

    contest_user = Contest_User.query.filter_by(
        contest_id=contest_id,
        user_id=current_user.id
    ).first()

    if contest_user is None:
        return redirect(f"/contest/{contest_id}")
    
    contest_user_solution = Contest_User_Solution.query.filter_by(
        contest_user_id=contest_user.id,
        problem_id=problem.id
    ).first()

    if contest_user_solution is None:
        return redirect(f"/contest/{contest_id}")
    

    return render_template("contest/contest_problem.html", current_contest=contest, current_problem=problem, current_solution=contest_user_solution, title=f"{contest.name} - №{idx}")


@contest.route("/contest/<contest_id>/solution/<solution_hashed_id>", methods=["GET", "POST"])
@login_required
def contest_solution(contest_id, solution_hashed_id):
    contest = Contest.query.filter_by(id=contest_id).first()
    if contest is None:
        return redirect("/myprofile")
    solution = Contest_User_Solution.query.filter_by(hashed_id=solution_hashed_id).first()
    if solution is None:
        return redirect(f"/contest/{contest_id}")
    return render_template("contest/contest_solution.html", current_contest=contest, current_solution=solution, title=f"{solution.contest_user.user.name} - решение")