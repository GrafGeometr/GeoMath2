from .imports import *
from .model_imports import *

club = Blueprint('club', __name__)

@club.route("/club/create", methods=["POST", "GET"])
@login_required
def create_new_club():
    if request.method == "POST":
        create = request.form.get("create", False)
        join = request.form.get("join", False)
        name = request.form.get("name", "")
        code = request.form.get("code", "").strip()
        if (create):
            if name is None or name == "":
                flash("Необходимо указать название кружка", "warning")
                return render_template("club/club_create.html", title=f"Создание кружка", name=name, code=code)
            club = Club(name=name)
            club.add()
            club.add_user(user=current_user, role=Owner)
            flash("Кружок успешно создан", "success")
            return redirect(f"/club/{club.hashed_id}/chats")
        elif (join):
            Invite.act_refresh_all()
            if code is None or code == "":
                flash("Необходимо указать код-приглашение", "warning")
                return render_template("club/club_create.html", title=f"Создание кружка", name=name, code=code)
            i = Invite.query.filter_by(code=code).first()
            if i is None:
                flash("Код-приглашение не действителен", "error")
                return render_template("club/club_create.html", title=f"Создание кружка", name=name, code=code)
            club = i.get_parent()
            if type(club) != Club:
                flash("Код-приглашение не действителен", "error")
                return render_template("club/club_create.html", title=f"Создание кружка", name=name, code=code)
            club.add_user_by_invite(current_user, i)
            flash("Вы присоединились к кружку", "success")
            return redirect(f"/club/{club.hashed_id}/chats")

        

    return render_template("club/club_create.html", title=f"Создание кружка")

@club.route("/club/<club_hashed_id>/chats", methods=["GET", "POST"])
@login_required
def club_chats(club_hashed_id):
    club = Club.query.filter_by(hashed_id=club_hashed_id).first()
    if club is None:
        flash("Кружок с таким id не найден", "error")
        return redirect("/myprofile")
    if not club.is_my():
        flash("Вы не состоите в этом кружке", "error")
        return redirect("/myprofile")
    if request.method == "POST":
        if not current_user.get_club_relation(club.id).role.is_owner():
            flash("Недостаточно прав", "error")
            return redirect(f"/club/{club_hashed_id}/chats")
        if request.form.get("remove_chat") is not None:
            chat_id = request.form.get("remove_chat")
            club.act_remove_chat_by_id(chat_id)
            flash("Чат успешно удален", "success")
            return redirect(f"/club/{club_hashed_id}/chats")
    return render_template("club/club_chats.html", club=club, title=f"{club.name} - чаты")

@club.route("/club/<club_hashed_id>/chat/create", methods=["GET", "POST"])
@login_required
def create_new_chat(club_hashed_id):
    club = Club.query.filter_by(hashed_id=club_hashed_id).first()
    if club is None:
        flash("Кружок с таким id не найден", "error")
        return redirect("/myprofile")
    if not club.is_my():
        flash("Вы не состоите в этом кружке", "error")
        return redirect("/myprofile")
    if not current_user.get_club_relation(club.id).role.is_owner():
        flash("Недостаточно прав", "error")
        return redirect(f"/club/{club_hashed_id}/chats")
    if request.method == "POST":
        name = request.form.get("name")
        chat = club.act_add_chat(name)
        if chat is None:
            flash("Не удалось создать чат", "error")
            return redirect(f"/club/{club_hashed_id}/chats")
        flash("Чат успешно создан", "success")
        return redirect(f"/chat/{chat.hashed_id}/messages")

    return render_template("club/club_chat_create.html", title=f"Новый чат", club=club)

@club.route("/club/<club_hashed_id>/contests", methods=["GET", "POST"])
@login_required
def club_contests(club_hashed_id):
    club = Club.query.filter_by(hashed_id=club_hashed_id).first()
    if club is None:
        flash("Кружок с таким id не найден", "error")
        return redirect("/myprofile")
    if not club.is_my():
        flash("Вы не состоите в этом кружке", "error")
        return redirect("/myprofile")
    if request.method == "POST":
        if not current_user.get_club_relation(club.id).role.is_owner():
            flash("Недостаточно прав", "error")
            return redirect(f"/club/{club_hashed_id}/contests")
        if request.form.get("remove_contest") is not None:
            contest_id = request.form.get("remove_contest")
            club.act_remove_contest_by_id(contest_id)
            flash("Контест успешно откреплён", "success")
            return redirect(f"/club/{club_hashed_id}/contests")
    return render_template("club/club_contests.html", club=club, title=f"{club.name} - контесты")

@club.route("/club/<club_hashed_id>/contest/create", methods=["GET", "POST"])
@login_required
def create_new_contest(club_hashed_id):
    club = Club.query.filter_by(hashed_id=club_hashed_id).first()
    if club is None:
        flash("Кружок с таким id не найден", "error")
        return redirect("/myprofile")
    if not club.is_my():
        flash("Вы не состоите в этом кружке", "error")
        return redirect("/myprofile")
    if not current_user.get_club_relation(club.id).role.is_owner():
        flash("Недостаточно прав", "error")
        return redirect(f"/club/{club_hashed_id}/contests")
    if request.method == "POST":
        contest_id = request.form.get("contest_id")
        if club.act_add_contest(contest_id) is None:
            flash("Не удалось прикрепить контест", "error")
            return redirect(f"/club/{club_hashed_id}/contests")
        flash("Контест успешно прикреплён", "success")
        return redirect(f"/club/{club_hashed_id}/contests")
    return render_template("club/club_contest_create.html", title=f"Новый контест", club=club)


@club.route("/club/<club_hashed_id>/participants", methods=["GET", "POST"])
@login_required
def club_participants(club_hashed_id):
    club = Club.query.filter_by(hashed_id=club_hashed_id).first()
    if club is None:
        flash("Кружок с таким id не найден", "error")
        return redirect("/myprofile")
    if not club.is_my():
        flash("Вы не состоите в этом кружке", "error")
        return redirect("/myprofile")

    if request.method == "POST":
        if request.form.get("leave_club") is not None:
            user_relation = current_user.get_club_relation(club.id)
            is_owner = user_relation.role.is_owner()
            is_participant = user_relation.role.is_participant()
            if (not is_owner) and (not is_participant):
                flash("Такого пользователя нет в кружке", "error")
                return redirect(url_for("club.club_participants", club_hashed_id=club_hashed_id))
            if (is_owner) and club.count_owners() == 1:
                flash("Вы единственный владелец, сначала удалите кружок", "error")
                return redirect(url_for("club.club_participants", club_hashed_id=club_hashed_id))
            user_relation.remove()
            flash(f"Вы вышли из кружка", "success")
            return redirect("/profile/clubs")

    return render_template("club/club_participants.html", club=club, title=f"{club.name} - участники")

@club.route("/club/<club_hashed_id>/management")
@login_required
def club_manager(club_hashed_id):  # ok
    return redirect(f"/club/{club_hashed_id}/management/general")


@club.route("/club/<club_hashed_id>/management/general", methods=["GET", "POST"])
@login_required
def club_manager_general(club_hashed_id):
    club = Club.query.filter_by(hashed_id=club_hashed_id).first()
    if club is None:
        flash("Кружок с таким id не найден", "error")
        return redirect("/myprofile")
    if not club.is_my():
        flash("Вы не состоите в этом кружке", "error")
        return redirect("/myprofile")
    if not current_user.get_club_relation(club.id).role.is_owner():
        flash("Недостаточно прав", "error")
        return redirect(f"/club/{club_hashed_id}/chats")

    if request.method == "POST":
        if request.form.get("club_name") is not None:
            club.name = request.form.get("club_name")
            db.session.commit()
            flash("Название кружка успешно изменено", "success")
            return redirect(url_for("club.club_manager_general", club_hashed_id=club_hashed_id))
        if request.form.get("delete_club") is not None:
            msg = request.form.get("confirm_message")
            if msg != "Подтверждаю":
                flash("Вы не подтвердили удаление кружка", "error")
                return redirect(f"/club/{club_hashed_id}/management/general")
            club.remove()
            flash("Кружок успешно удален", "success")
            return redirect("/profile/clubs")

    return render_template("club/club_management_general.html", club=club, title=f"{club.name} - управление")



@club.route("/club/<club_hashed_id>/management/collaborators", methods=["GET", "POST"])
@login_required
def club_collaborators(club_hashed_id):
    club = Club.query.filter_by(hashed_id=club_hashed_id).first()
    if club is None:
        flash("Кружок с таким id не найден", "error")
        return redirect("/myprofile")
    if not club.is_my():
        flash("Вы не состоите в этом кружке", "error")
        return redirect("/profile/clubs")
    if not current_user.get_club_relation(club.id).role.is_owner():
        flash("Недостаточно прав", "error")
        return redirect(f"/club/{club_hashed_id}/chats")

    if request.method == "POST":
        if request.form.get("upgrade_to_owner") is not None:
            user_id = request.form.get("upgrade_to_owner")
            user = User.query.filter_by(id=user_id).first()
            if user is None:
                flash("Пользователь не найден", "error")
                return redirect(url_for("club.club_collaborators", club_hashed_id=club_hashed_id))
            user_relation = user.get_club_relation(club.id)
            if user_relation is None:
                flash("Такого пользователя нет в кружке", "error")
                return redirect(url_for("chat.chat_collaborators", club_hashed_id=club_hashed_id))
            if user_relation.role.is_owner():
                flash("Пользователь уже владелец кружка", "warning")
                return redirect(url_for("club.club_collaborators", club_hashed_id=club_hashed_id))
            user_relation.role = Owner
            # current_user.get_chat_relation(chat.id).role = Participant
            db.session.commit()
            flash(f"Права владельца успешно выданы пользователю {user.name}", "success")
            return redirect(url_for("club.club_collaborators", club_hashed_id=club_hashed_id))

        elif request.form.get("downgrade_to_participant") is not None:
            user_id = request.form.get("downgrade_to_participant")
            user = User.query.filter_by(id=user_id).first()
            if user is None:
                flash("Пользователь не найден", "error")
                return redirect(url_for("club.club_collaborators", club_hashed_id=club_hashed_id))
            user_relation = user.get_club_relation(club.id)
            if user_relation is None:
                flash("Такого пользователя нет в кружке", "error")
                return redirect(url_for("chat.chat_collaborators", club_hashed_id=club_hashed_id))
            if user_relation.role.is_participant():
                flash("Пользователь уже участник кружка", "warning")
                return redirect(url_for("club.club_collaborators", club_hashed_id=club_hashed_id))
            if user.id == current_user.id and club.count_owners() == 1:
                flash("Вы единственный владелец кружка, понижение невозможно", "warning")
                return redirect(url_for("club.club_collaborators", club_hashed_id=club_hashed_id))
            user_relation.role = Participant
            db.session.commit()
            flash(f"Пользователь {user.name} успешно понижен до участника", "success")
            return redirect(url_for("club.club_collaborators", club_hashed_id=club_hashed_id))

        elif request.form.get("remove_participant") is not None:
            user_id = request.form.get("remove_participant")
            user = User.query.filter_by(id=user_id).first()
            if user is None:
                flash("Пользователь не найден", "error")
                return redirect(url_for("club.club_collaborators", club_hashed_id=club_hashed_id))
            user_relation = user.get_club_relation(club.id)
            if user_relation is None:
                flash("Такого пользователя нет в кружке", "error")
            if user_id == current_user.id:
                flash("Вы не можете удалить себя из кружка на этой странице", "error")
                return redirect(url_for("club.club_collaborators", club_hashed_id=club_hashed_id))
            if user_relation.role.is_owner():
                flash("Удалить владельца невозможно, сначала понизьте его до участника")
                return redirect(url_for("club.club_collaborators", club_hashed_id=club_hashed_id))
            user_relation.remove()
            flash(f"Пользователь {user.name} успешно удалён", "success")
            return redirect(url_for("club.club_collaborators", club_hashed_id=club_hashed_id))
        elif request.form.get("new_invite_code") is not None:
            club.act_generate_new_invite_code()
            return redirect(url_for("club.club_collaborators", club_hashed_id=club_hashed_id))

    return render_template("club/club_management_collaborators.html", club=club, title=f"{club.name} - управление участниками")