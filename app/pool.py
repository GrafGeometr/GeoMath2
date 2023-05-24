from .imports import *
from .model_imports import *

pool = Blueprint('pool', __name__)

@login_required
@pool.route("/accept_pool_invitation", methods=["POST"])
def accept_pool_invitation():
    data = request.get_json()
    pool_hashed_id = data["pool_hashed_id"]


    pool = Pool.query.filter_by(hashed_id=pool_hashed_id).first()

    if pool is None:
        return "pool not found"

    relation = UserPool.query.filter_by(user_id = current_user.id, pool_id = pool.id).first()

    if relation is None:
        return "user not invited"
    
    relation.role = "Participant"

    db.session.commit()
    print("DONE")

    return "ok"

@login_required
@pool.route("/decline_pool_invitation", methods=["POST"])
def decline_pool_invitation():
    data = request.get_json()
    pool_hashed_id = data["pool_hashed_id"]


    pool = Pool.query.filter_by(hashed_id = pool_hashed_id).first()

    if pool is None:
        return "pool not found"
    

    relation = UserPool.query.filter_by(user_id = current_user.id, pool_id = pool.id).first()

    if relation is None:
        return "user not invited"
    
    db.session.delete(relation)
    db.session.commit()

    return "ok"


@pool.route("/pool/<pool_hashed_id>/problems")
def pool_problems(pool_hashed_id):
    pool = Pool.query.filter_by(hashed_id = pool_hashed_id).first()

    if pool is None:
        return "pool not found"
    
    return render_template("pool_problems.html", current_pool=pool)


@pool.route("/pool/<pool_hashed_id>/participants")
def pool_participants(pool_hashed_id):
    pool = Pool.query.filter_by(hashed_id = pool_hashed_id).first()

    if pool is None:
        return "pool not found"
    
    return render_template("pool_participants.html", current_pool=pool)

@pool.route("/pool/<pool_hashed_id>/management")
def pool_manager(pool_hashed_id):
    pool = Pool.query.filter_by(hashed_id = pool_hashed_id).first()

    if pool is None:
        return "pool not found"
    
    return render_template("pool_management.html", current_pool=pool)

@pool.route("/pool/<pool_hashed_id>/new_problem", methods=["POST"])
def new_problem(pool_hashed_id):
    pool = Pool.query.filter_by(hashed_id = pool_hashed_id).first()

    if pool is None:
        return "pool not found"
    
    problem = Problem(statement="Условие", solution="Решение", pool_id=pool.id)
    db.session.add(problem)
    db.session.commit()
    problem.name = f"Задача #{problem.id}"
    db.session.commit()
    return redirect(f"/pool/{pool_hashed_id}/problem/{problem.id}")

@pool.route("/remove_problem_from_pool", methods=["POST"])
def remove_problem_from_pool():
    data = request.get_json()
    pool_hashed_id = data["pool"]
    problem_id = data["problem"]
    pool = Pool.query.filter_by(hashed_id = pool_hashed_id).first()
    problem = Problem.query.filter_by(id = problem_id).first()
    db.session.delete(problem)
    db.session.commit()
    return render_template("pool_problemlist.html", current_pool=pool)

@pool.route("/pool/<pool_hashed_id>/problem/<problem_id>", methods=["GET", "POST"])
def problem(pool_hashed_id, problem_id):
    pool = Pool.query.filter_by(hashed_id = pool_hashed_id).first()
    problem = Problem.query.filter_by(id = problem_id).first()
    if request.method == "POST":
        name = request.form["name"]
        statement = request.form["statement"]
        solution = request.form["solution"]
        if name in [pr.name for pr in pool.problems if pr.id != problem.id]:
            flash("Задача с таким именем уже существует", "danger")
        elif name == "" or statement == "" or solution == "":
            flash("Заполните все поля", "danger")
        else:
            problem.name = name
            problem.statement = statement
            problem.solution = solution
            db.session.commit()
            flash("Задача успешно сохранена", "success")    
        return redirect(f"/pool/{pool_hashed_id}/problem/{problem_id}")
    return render_template("pool_1problem.html", current_pool=pool, current_problem=problem)

@pool.route("/pools/create")
def create_pool():
    return render_template("pool_create.html")

@pool.route("/create_new_pool", methods=["POST"])
def create_new_pool():
    data = request.get_json()
    name = data["name"]
    used_tokens = [p.hashed_id for p in Pool.query.all()]
    hashed_id = generate_token(30)
    while hashed_id in used_tokens:
        hashed_id = generate_token(30)
    
    pool = Pool(hashed_id=hashed_id, name=name)
    db.session.add(pool)
    relation = UserPool(user_id=current_user.id, pool_id=pool.id, role="Owner")
    db.session.add(relation)
    db.session.commit()

    return f"/pool/{hashed_id}/problems"

@pool.route("/add_participant", methods=["POST"])
def add_participant():
    data = request.get_json()
    login = data["login"]
    pool_hashed_id = data["pool_hashed_id"]

    relation = UserPool(user=User.query.filter_by(name = login).first(), pool=Pool.query.filter_by(hashed_id = pool_hashed_id).first(), role="Invited")
    db.session.add(relation)
    db.session.commit()

    return render_template("mypools.html")


@pool.route("/remove_participant", methods=["POST"])
def remove_participant():
    data = request.get_json()
    login = data["login"]
    pool_hashed_id = data["pool_hashed_id"]

    user = User.query.filter_by(name = login).first()
    pool = Pool.query.filter_by(hashed_id = pool_hashed_id).first()

    relation = UserPool.query.filter_by(user_id = user.id, pool_id = pool.id).first()
    db.session.delete(relation)
    db.session.commit()
  
    return render_template("mypools.html")