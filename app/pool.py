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
        flash("Пул с таким id не найден", "danger")
        return redirect("/myprofile")

    relation = UserPool.query.filter_by(user_id = current_user.id, pool_id = pool.id).first()

    if relation is None:
        return "user not invited"
    
    relation.role = Participant

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
        flash("Пул с таким id не найден", "danger")
        return redirect("/myprofile")
    

    relation = UserPool.query.filter_by(user_id = current_user.id, pool_id = pool.id).first()

    if relation is None:
        return "user not invited"
    
    db.session.delete(relation)
    db.session.commit()

    return "ok"


@pool.route("/pool/<pool_hashed_id>/problems")
def pool_problems(pool_hashed_id): # ok
    pool = Pool.query.filter_by(hashed_id = pool_hashed_id).first()

    if pool is None:
        flash("Пул с таким id не найден", "danger")
        return redirect("/myprofile")
    
    return render_template("pool/pool_problems.html", current_pool=pool, title=f"{pool.name} - задачи")


@pool.route("/pool/<pool_hashed_id>/participants", methods=["GET", "POST"])
def pool_participants(pool_hashed_id): # ok
    pool = Pool.query.filter_by(hashed_id = pool_hashed_id).first()
    if pool is None:
        flash("Пул с таким id не найден", "danger")
        return redirect("/myprofile")
    
    if request.method == "POST":
        if request.form.get("leave_pool") is not None:
            user_relation = current_user.get_pool_relation(pool.id)
            if user_relation is None:
                flash("Такого пользователя нет в пуле", "danger")
                return redirect(url_for("pool.pool_participants", pool_hashed_id=pool_hashed_id))
            if user_relation.role.isOwner():
                flash("Вы не можете выходить из пула", "danger")
                return redirect(url_for("pool.pool_participants", pool_hashed_id=pool_hashed_id))
            db.session.delete(user_relation)
            db.session.commit()
            flash(f"Пользователь {current_user.name} успешно удалён", "success")
            return redirect("/myprofile")


    return render_template("pool/pool_participants.html", current_pool=pool, title=f"{pool.name} - участники")


@pool.route("/pool/<pool_hashed_id>/new_problem", methods=["POST"])
def new_problem(pool_hashed_id): # reworked
    pool = Pool.query.filter_by(hashed_id = pool_hashed_id).first()

    if pool is None:
        flash("Пул с таким id не найден", "danger")
        return redirect("/myprofile")
    
    problem = pool.new_problem()

    return redirect(f"/pool/{pool_hashed_id}/problem/{problem.id}")

@pool.route("/remove_problem_from_pool", methods=["POST"])
def remove_problem_from_pool(): # ok
    data = request.get_json()
    pool_hashed_id = data["pool"]
    problem_id = data["problem"]
    pool = Pool.query.filter_by(hashed_id = pool_hashed_id).first()
    problem = Problem.query.filter_by(id = problem_id).first()
    db.session.delete(problem)
    db.session.commit()
    return render_template("pool/pool_problemlist.html", current_pool=pool)

@pool.route("/pool/<pool_hashed_id>/problem/<problem_id>", methods=["GET", "POST"])
def problem(pool_hashed_id, problem_id): # reworked
    pool = Pool.query.filter_by(hashed_id = pool_hashed_id).first()
    problem = Problem.query.filter_by(id = problem_id).first()
    if request.method == "POST":
        name = request.form["name"]
        statement = request.form["statement"]
        solution = request.form["solution"]
        """if name in [pr.name for pr in pool.problems if pr.id != problem.id]:
            problem.statement = statement
            problem.solution = solution
            db.session.commit()
            flash("Задача с таким именем уже существует", "danger")
        elif name == "" or statement == "" or solution == "":
            flash("Заполните все поля", "danger")"""
        
        # TODO add problem states checking

        problem.name = name
        problem.statement = statement
        problem.solution = solution
        db.session.commit()
        flash("Задача успешно сохранена", "success")    
        return redirect(f"/pool/{pool_hashed_id}/problem/{problem_id}")
    return render_template("pool/pool_1problem.html", current_pool=pool, current_problem=problem, title=f"Редактор - {problem.name}")


@pool.route("/pool/create", methods=["POST", "GET"])
def create_new_pool():
    if request.method == "POST":
        name = request.form.get("name")
        print(name)
        hashed_id = current_user.create_new_pool(name)
        return redirect(f"/pool/{hashed_id}/problems")
    
    return render_template("pool/pool_create.html", title=f"Создание пула")



# pool management

@pool.route("/pool/<pool_hashed_id>/management")
def pool_manager(pool_hashed_id): # ok
    return redirect(f"/pool/{pool_hashed_id}/management/general")


@pool.route("/pool/<pool_hashed_id>/management/general", methods=["GET", "POST"])
def pool_manager_general(pool_hashed_id):
    pool = Pool.query.filter_by(hashed_id = pool_hashed_id).first()
    
    if pool is None:
        flash("Пул с таким id не найден", "danger")
        return redirect("/myprofile")
    
    if request.method == "POST":
        if not current_user.get_pool_relation(pool.id).role.isOwner():
            flash("Вы не имеете доступа к этой странице", "danger")
            return redirect(url_for("pool.pool_manager_general", pool_hashed_id=pool_hashed_id))
        if request.form.get("pool_name") is not None:
            pool.name = request.form.get("pool_name")
            db.session.commit()
            flash("Имя пула успешно изменено", "success")
            return redirect(url_for("pool.pool_manager_general", pool_hashed_id=pool_hashed_id))
        if request.form.get("delete_pool") is not None:
            db.session.delete(pool)
            db.session.commit()
            flash("Пул успешно удален", "success")
            return redirect("/myprofile")
    
    return render_template("pool/pool_management_general.html", current_pool=pool, title=f"{pool.name} - управление")

@pool.route("/pool/<pool_hashed_id>/management/collaborators", methods=["GET", "POST"])
def pool_collaborators(pool_hashed_id):
    pool = Pool.query.filter_by(hashed_id = pool_hashed_id).first()
    
    if pool is None:
        flash("Пул с таким id не найден", "danger")
        return redirect("/myprofile")

    if request.method == "POST":
        if not current_user.get_pool_relation(pool.id).role.isOwner():
            flash("Вы не имеете доступа к этой странице", "danger")
            return redirect(url_for("pool.pool_collaborators", pool_hashed_id=pool_hashed_id))
        if request.form.get("make_owner_user_id") is not None:
            user_id = request.form.get("make_owner_user_id")
            user = User.query.filter_by(id = user_id).first()
            if user is None:
                flash("Пользователь не найден", "danger")
                return redirect(url_for("pool.pool_collaborators", pool_hashed_id=pool_hashed_id))
            user_relation = user.get_pool_relation(pool.id)
            if user_relation is None:
                flash("Такого пользователя нет в пуле", "danger")
                return redirect(url_for("pool.pool_collaborators", pool_hashed_id=pool_hashed_id))
            if user_relation.role.isOwner():
                flash("Пользователь уже владелец пула", "warning")
                return redirect(url_for("pool.pool_collaborators", pool_hashed_id=pool_hashed_id))
            if user_relation.role.isInvited():
                flash("Передать права владельца можно только участнику", "warning")
                return redirect(url_for("pool.pool_collaborators", pool_hashed_id=pool_hashed_id))
            user_relation.role = Owner
            current_user.get_pool_relation(pool.id).role = Participant
            db.session.commit()
            flash(f"Права владельца успешно переданы пользователю {user.name}", "success")
            return redirect(url_for("pool.pool_collaborators", pool_hashed_id=pool_hashed_id))
        elif request.form.get("remove_user_id") is not None:
            user_id = request.form.get("remove_user_id")
            user = User.query.filter_by(id = user_id).first()
            if user is None:
                flash("Пользователь не найден", "danger")
                return redirect(url_for("pool.pool_collaborators", pool_hashed_id=pool_hashed_id))
            user_relation = user.get_pool_relation(pool.id)
            if user_relation is None:
                flash("Такого пользователя нет в пуле", "danger")
                return redirect(url_for("pool.pool_collaborators", pool_hashed_id=pool_hashed_id))
            if user_id == current_user.id:
                flash("Вы не можете удалить себя из пула на этой странице", "danger")
                return redirect(url_for("pool.pool_collaborators", pool_hashed_id=pool_hashed_id))
            db.session.delete(user_relation)
            db.session.commit()
            flash(f"Пользователь {user.name} успешно удалён", "success")
            return redirect(url_for("pool.pool_collaborators", pool_hashed_id=pool_hashed_id))
        elif request.form.get("login1") is not None:

            print(request.form.get("login1"))

            user_name = request.form.get("login1")
            user = User.query.filter_by(name = user_name).first()

            if user is None:
                flash(f"Пользователь {user_name} не найден", "danger")
                print("Пользователь не найден")
                return redirect(url_for("pool.pool_collaborators", pool_hashed_id=pool_hashed_id))

            # add this user to the pool

            relation = UserPool(user=user, pool=pool, role=Invited)
            db.session.add(relation)
            db.session.commit()
            flash(f"Пользователь {user.name} успешно приглашен", "success")
            return redirect(url_for("pool.pool_collaborators", pool_hashed_id=pool_hashed_id))
    
    return render_template("pool/pool_management_collaborators.html", current_pool=pool, title=f"{pool.name} - участники")