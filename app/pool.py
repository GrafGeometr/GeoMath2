from .imports import *
from .model_imports import *

pool = Blueprint('pool', __name__)


@pool.route("/pool/<pool_hashed_id>/problem/<problem_id>/<filename>")
def show_problem_attachment(pool_hashed_id, problem_id, filename):
    print(pool_hashed_id, problem_id, filename)
    if not current_user.is_authenticated:
        print("not authenticated")
        return
    pool = Pool.query.filter_by(hashed_id = pool_hashed_id).first()
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
    problem = Problem.query.filter_by(id = problem_id).first()
    if problem is None:
        print("problem none")
        return
    attachment = ProblemAttachment.query.filter_by(problem_id = problem_id, db_filename = filename).first()
    if attachment is None:
        print("attachment none")
        return
    try:
        return send_from_directory(os.path.join(basedir, 'database/attachments/problems'), filename, as_attachment=True)
    except Exception as e:
        print(e)

def check_user_in_pool(user, pool):
    if user.get_pool_relation(pool.id) is None:
        flash("Вы не можете просматривать этот пул", "danger")
        return "/myprofile"
    if user.get_pool_relation(pool.id).role.isInvited():
        flash("Вы не приняли приглашение в этот пул", "danger")
        return f"/profile/{user.name}/pools"
    return None      

def check_management_access(user, pool):
    if user.get_pool_relation(pool.id).role.isOwner():
        return None
    flash("Вы не можете управлять этим пулом", "danger")
    return url_for("pool.pool_participants", pool_hashed_id=pool.hashed_id)

@pool.route("/accept_pool_invitation", methods=["POST"])
@login_required
def accept_pool_invitation():
    data = request.get_json()
    pool_hashed_id = data["pool_hashed_id"]


    pool = Pool.query.filter_by(hashed_id=pool_hashed_id).first()

    if pool is None:
        flash("Пул с таким id не найден", "danger")
        return redirect("/myprofile")

    relation = User_Pool.query.filter_by(user_id = current_user.id, pool_id = pool.id).first()

    if relation is None:
        return "user not invited"
    
    relation.role = Participant

    db.session.commit()
    print("DONE")

    return render_template("profile/profile_pools_table.html")


@pool.route("/decline_pool_invitation", methods=["POST"])
@login_required
def decline_pool_invitation():
    data = request.get_json()
    pool_hashed_id = data["pool_hashed_id"]


    pool = Pool.query.filter_by(hashed_id = pool_hashed_id).first()

    if pool is None:
        flash("Пул с таким id не найден", "danger")
        return redirect("/myprofile")
    

    relation = User_Pool.query.filter_by(user_id = current_user.id, pool_id = pool.id).first()

    if relation is None:
        return "user not invited"
    
    db.session.delete(relation)
    db.session.commit()

    return render_template("profile/profile_pools_table.html")


@pool.route("/pool/<pool_hashed_id>/problems", methods=["GET", "POST"])
@login_required
def pool_problems(pool_hashed_id): # ok
    pool = Pool.query.filter_by(hashed_id = pool_hashed_id).first()

    if pool is None:
        flash("Пул с таким id не найден", "danger")
        return redirect("/myprofile")
    
    user_checked = check_user_in_pool(current_user, pool)
    if user_checked is not None:
        return redirect(user_checked)
    
    if request.method == "POST":
        if request.form.get("back_to_pool") is not None:
            problem_id = request.form.get("problem_id")
            problem = Problem.query.filter_by(id = problem_id).first()
            problem.is_public = problem.moderated = False
            db.session.commit()

        """if request.form.get("switch_solution_access") is not None:
            problem.show_solution = not problem.show_solution
            db.session.commit()
            return redirect(f"/archive/problem/{problem_id}")
        if request.form.get("add_tag") is not None:
            tag_name = request.form["tag_name"]
            tag = Tag.query.filter_by(name=tag_name).first()
            if (tag is None) and (current_user.admin):
                tag = Tag(name=tag_name)
                db.session.add(tag)
                db.session.commit()
            if Problem_Tag.query.filter_by(problem=problem, tag=tag).first() is None:
                problem_tag = Problem_Tag(problem=problem, tag=tag)
                db.session.add(problem_tag)
                db.session.commit()
            return redirect(f"/archive/problem/{problem_id}")
        if request.form.get("remove_tag") is not None:
            tag_id = request.form.get("remove_tag")
            tag = Tag.query.filter_by(id=tag_id).first()
            if tag is None:
                return redirect(f"/archive/problem/{problem_id}")
            if Problem_Tag.query.filter_by(problem=problem, tag=tag).first() is not None:
                db.session.delete(Problem_Tag.query.filter_by(problem=problem, tag=tag).first())
                db.session.commit()
            return redirect(f"/archive/problem/{problem_id}")
        if request.form.get("delete_problem") is not None:
            db.session.delete(problem)
            db.session.commit()
            return redirect("/archive/my")
        if request.form.get("switch_attachment_access") is not None:
            attachment_id = request.form.get("switch_attachment_access")
            attachment = ProblemAttachment.query.filter_by(id=attachment_id).first()
            if attachment is None:
                return redirect(f"/archive/problem/{problem_id}")
            if attachment.problem_id != problem_id:
                return redirect(f"/archive/problem/{problem_id}")
            if Problem_Tag.query.filter_by(problem=problem, tag=tag).first() is not None:
                db.session.delete(Problem_Tag.query.filter_by(problem=problem, tag=tag).first())
                db.session.commit()
            return redirect(f"/archive/problem/{problem_id}")
        if request.form.get("delete_problem") is not None:
            db.session.delete(problem)
            db.session.commit()
            return redirect("/archive/my")"""
    
    return render_template("pool/pool_problems.html", current_pool=pool, title=f"{pool.name} - задачи")


@pool.route("/pool/<pool_hashed_id>/participants", methods=["GET", "POST"])
@login_required
def pool_participants(pool_hashed_id): # ok
    pool = Pool.query.filter_by(hashed_id = pool_hashed_id).first()
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
                return redirect(url_for("pool.pool_participants", pool_hashed_id=pool_hashed_id))
            if user_relation.role.isOwner() and pool.count_owners() == 1:
                flash("Вы не можете выходить из пула, так как являетесь единственным владельцем", "danger")
                return redirect(url_for("pool.pool_participants", pool_hashed_id=pool_hashed_id))
            db.session.delete(user_relation)
            db.session.commit()
            flash(f"Пользователь {current_user.name} успешно удалён", "success")
            return redirect("/myprofile")


    return render_template("pool/pool_participants.html", current_pool=pool, title=f"{pool.name} - участники")


@pool.route("/pool/<pool_hashed_id>/new_problem", methods=["POST"])
@login_required
def new_problem(pool_hashed_id): # reworked
    pool = Pool.query.filter_by(hashed_id = pool_hashed_id).first()

    if pool is None:
        flash("Пул с таким id не найден", "danger")
        return redirect("/myprofile")
    
    user_checked = check_user_in_pool(current_user, pool)
    if user_checked is not None:
        return redirect(user_checked)
    
    problem = pool.new_problem()

    return redirect(f"/pool/{pool_hashed_id}/problem/{problem.id}")

@pool.route("/remove_problem_from_pool", methods=["POST"])
@login_required
def remove_problem_from_pool(): # ok
    data = request.get_json()
    pool_hashed_id = data["pool"]
    problem_id = data["problem"]
    pool = Pool.query.filter_by(hashed_id = pool_hashed_id).first()

    if pool is None:
        flash("Пул с таким id не найден", "danger")
        return redirect("/myprofile")
    
    user_checked = check_user_in_pool(current_user, pool)
    if user_checked is not None:
        return redirect(user_checked)

    problem = Problem.query.filter_by(id = problem_id).first()

    if problem is None:
        flash("Задача не найдена", "danger")
        return redirect(f"/pool/{pool_hashed_id}/problems")
    
    db.session.delete(problem)
    db.session.commit()
    return render_template("pool/pool_problemlist.html", current_pool=pool)

@pool.route("/pool/<pool_hashed_id>/problem/<int:problem_id>", methods=["GET", "POST"])
@login_required
def problem(pool_hashed_id, problem_id): # reworked
    pool = Pool.query.filter_by(hashed_id = pool_hashed_id).first()

    if pool is None:
        flash("Пул с таким id не найден", "danger")
        return redirect("/myprofile")
    
    user_checked = check_user_in_pool(current_user, pool)
    if user_checked is not None:
        return redirect(user_checked)

    problem = Problem.query.filter_by(id = problem_id).first()
    #print("pr", problem.id)

    if problem is None:
        flash("Задача не найдена", "danger")
        return redirect(f"/pool/{pool_hashed_id}/problems")
    
    if request.method == "POST":
        if request.form.get("save_problem") is not None:
            name = request.form.get("name")
            statement = request.form.get("statement")
            solution = request.form.get("solution")
            
            # TODO add problem states checking

            problem.name = name
            problem.statement = statement
            problem.solution = solution

            for attachment in problem.attachments:
                preview_name = request.form.get("attachment_name " + str(attachment.id))
                if preview_name is None:
                    problem.delete_attachment(attachment)
                    continue
                
                attachment.preview_name = preview_name
                show = request.form.get("lock_attachment " + str(attachment.id))
                if show is None:
                    attachment.locked = False
                else:
                    attachment.locked = True
                print(attachment.id, show)

            db.session.commit()

            print(request.files.getlist("attachments"))

            directory = "app/database/attachments/problems"
            filenames = safe_image_upload(request, "attachments", directory, 5*1024*1024)
            
            for filename in filenames:
                if filename is None:
                    continue
                attachment = ProblemAttachment(db_folder=directory, db_filename=filename, preview_name="Рисунок", problem_id=problem.id)
                db.session.add(attachment)

            db.session.commit()

            flash("Задача успешно сохранена", "success")    
            return redirect(f"/pool/{pool_hashed_id}/problem/{problem_id}")
    return render_template("pool/pool_1problem.html", current_pool=pool, current_problem=problem, title=f"Редактор - {problem.name}")


@pool.route("/pool/create", methods=["POST", "GET"])
@login_required
def create_new_pool():
    if request.method == "POST":
        name = request.form.get("name")
        print(name)
        hashed_id = current_user.create_new_pool(name)
        return redirect(f"/pool/{hashed_id}/problems")
    
    return render_template("pool/pool_create.html", title=f"Создание пула")



# pool management

@pool.route("/pool/<pool_hashed_id>/management")
@login_required
def pool_manager(pool_hashed_id): # ok
    return redirect(f"/pool/{pool_hashed_id}/management/general")


@pool.route("/pool/<pool_hashed_id>/management/general", methods=["GET", "POST"])
@login_required
def pool_manager_general(pool_hashed_id):
    pool = Pool.query.filter_by(hashed_id = pool_hashed_id).first()
    
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
            return redirect(url_for("pool.pool_manager_general", pool_hashed_id=pool_hashed_id))
        if request.form.get("pool_name") is not None:
            print(type(request.form.get("pool_name")))
            pool.name = request.form.get("pool_name")
            db.session.commit()
            print(pool.name)
            flash("Имя пула успешно изменено", "success")
            return redirect(url_for("pool.pool_manager_general", pool_hashed_id=pool_hashed_id))
        if request.form.get("delete_pool") is not None:
            for relation in User_Pool.query.filter_by(pool_id = pool.id).all():
                db.session.delete(relation)
            for problem in Problem.query.filter_by(pool_id = pool.id).all():
                db.session.delete(problem)
            db.session.delete(pool)
            db.session.commit()
            flash("Пул успешно удален", "success")
            return redirect("/myprofile")
    
    return render_template("pool/pool_management_general.html", current_pool=pool, title=f"{pool.name} - управление")

@pool.route("/pool/<pool_hashed_id>/management/collaborators", methods=["GET", "POST"])
@login_required
def pool_collaborators(pool_hashed_id):
    pool = Pool.query.filter_by(hashed_id = pool_hashed_id).first()
    
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
            return redirect(url_for("pool.pool_collaborators", pool_hashed_id=pool_hashed_id))
        if request.form.get("upgrade_to_owner") is not None:
            user_id = request.form.get("upgrade_to_owner")
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
            #current_user.get_pool_relation(pool.id).role = Participant
            db.session.commit()
            flash(f"Права владельца успешно переданы пользователю {user.name}", "success")
            return redirect(url_for("pool.pool_participants", pool_hashed_id=pool_hashed_id))
        

        elif request.form.get("downgrade_to_participant") is not None:
            user_id = request.form.get("downgrade_to_participant")
            user = User.query.filter_by(id = user_id).first()
            if user is None:
                flash("Пользователь не найден", "danger")
                return redirect(url_for("pool.pool_collaborators", pool_hashed_id=pool_hashed_id))
            user_relation = user.get_pool_relation(pool.id)
            if user_relation is None:
                flash("Такого пользователя нет в пуле", "danger")
                return redirect(url_for("pool.pool_collaborators", pool_hashed_id=pool_hashed_id))
            if user_relation.role.isParticipant():
                flash("Пользователь уже участник пула", "warning")
                return redirect(url_for("pool.pool_collaborators", pool_hashed_id=pool_hashed_id))
            if user_relation.role.isInvited():
                flash("Понизить до участника можно только владельца", "warning")
                return redirect(url_for("pool.pool_collaborators", pool_hashed_id=pool_hashed_id))
            if user.id == current_user.id and pool.count_owners() == 1:
                flash("Вы являетесь единственным владельцем пула, понижение невозможно", "warning")
                return redirect(url_for("pool.pool_collaborators", pool_hashed_id=pool_hashed_id))
            user_relation.role = Participant
            db.session.commit()
            flash(f"Пользователь {user.name} успешно понижен до участника", "success")
            return redirect(url_for("pool.pool_participants", pool_hashed_id=pool_hashed_id))
            

        elif request.form.get("remove_participant") is not None:
            user_id = request.form.get("remove_participant")
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
            if user_relation.role.isOwner():
                flash("Удалить владельца невозможно, сначала понизьте его до участника")
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
            user_relation = user.get_pool_relation(pool.id)
            if user_relation is not None:
                flash(f"Пользователь {user.name} уже приглашен или состоит в пуле", "danger")
                return redirect(url_for("pool.pool_collaborators", pool_hashed_id=pool_hashed_id))
            # add this user to the pool

            relation = User_Pool(user=user, pool=pool, role=Invited)
            db.session.add(relation)
            db.session.commit()
            flash(f"Пользователь {user.name} успешно приглашен", "success")
            return redirect(url_for("pool.pool_collaborators", pool_hashed_id=pool_hashed_id))
    
    return render_template("pool/pool_management_collaborators.html", current_pool=pool, title=f"{pool.name} - участники")