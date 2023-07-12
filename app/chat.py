from .imports import *
from .model_imports import *

chat = Blueprint('chat', __name__)

@chat.route("/chats", methods=["GET", "POST"])
@login_required
def chats():
    return render_template("chat/chat_chats.html", chats=[uc.chat for uc in current_user.user_chats])

@chat.route("/chat/create", methods=["POST", "GET"])
@login_required
def create_new_chat():
    if request.method == "POST":
        create = request.form.get("create", False)
        join = request.form.get("join", False)
        name = request.form.get("name", "")
        code = request.form.get("code", "")
        if (create):
            if name is None or name == "":
                flash("Необходимо указать имя чата", "warning")
                return render_template("chat/chat_create.html", title=f"Создание чата", name=name, code=code)
            chat = Chat(name=name)
            chat.add()
            chat.act_add_user(user=current_user, role=Owner)
            flash("Чат успешно создан", "success")
            return redirect(f"/chat/{chat.hashed_id}/messages")
        elif (join):
            if code is None or code == "":
                flash("Необходимо указать код-приглашение", "warning")
                return render_template("chat/chat_create.html", title=f"Создание чата", name=name, code=code)
            ci = Chat_Invite.query.filter_by(code=code).first()
            if ci is None:
                flash("Код-приглашение не действителен", "error")
                return render_template("chat/chat_create.html", title=f"Создание чата", name=name, code=code)
            ci.chat.act_add_user_by_code(current_user, code)
            flash("Вы присоединились к чату", "success")
            return redirect(f"/chat/{ci.chat.hashed_id}/messages")

        

    return render_template("chat/chat_create.html", title=f"Создание чата")


@chat.route("/chat/<chat_hashed_id>/messages", methods=["GET", "POST"])
@login_required
def chat_messages(chat_hashed_id):
    chat = Chat.query.filter_by(hashed_id=chat_hashed_id).first()
    if chat is None:
        flash("Чат с таким id не найден", "error")
        return redirect("/chats")
    chat.act_mark_all_as_read()
    return render_template("chat/chat_messages.html", chat=chat, messages=chat.get_all_messages(), str_from_dt = str_from_dt)


@chat.route("/chat/<chat_hashed_id>/participants", methods=["GET", "POST"])
@login_required
def chat_participants(chat_hashed_id):
    chat = Chat.query.filter_by(hashed_id=chat_hashed_id).first()
    if chat is None:
        flash("Чат с таким id не найден", "error")
        return redirect("/myprofile")

    if not chat.is_my():
        flash("Вы не состоите в этом чате", "error")
        return redirect("/myprofile")

    if request.method == "POST":
        if request.form.get("leave_chat") is not None:
            user_relation = current_user.get_chat_relation(chat.id)
            if user_relation is None:
                flash("Такого пользователя нет в чате", "error")
                return redirect(
                    url_for("chat.chat_participants", chat_hashed_id=chat_hashed_id)
                )
            if user_relation.role.isOwner() and chat.count_owners() == 1:
                flash(
                    "Вы единственный владелец, сначала удалите чат",
                    "error",
                )
                return redirect(
                    url_for("chat.chat_participants", chat_hashed_id=chat_hashed_id)
                )
            user_relation.remove()
            flash(f"Вы вышли из чата", "success")
            return redirect("/myprofile")

    return render_template(
        "chat/chat_participants.html",
        chat=chat,
        title=f"{chat.name} - участники",
    )



# redirect to chat/management/general
@chat.route("/chat/<chat_hashed_id>/management")
@login_required
def chat_manager(chat_hashed_id):  # ok
    return redirect(f"/chat/{chat_hashed_id}/management/general")


# chat management - general
@chat.route("/chat/<chat_hashed_id>/management/general", methods=["GET", "POST"])
@login_required
def chat_manager_general(chat_hashed_id):
    chat = Chat.query.filter_by(hashed_id=chat_hashed_id).first()

    if chat is None:
        flash("Чат с таким id не найден", "error")
        return redirect("/myprofile")

    if not chat.is_my():
        flash("Вы не состоите в этом чате", "error")
        return redirect("/myprofile")


    if request.method == "POST":
        if not current_user.get_chat_relation(chat.id).role.isOwner():
            flash("Вы не имеете доступа к этой странице", "error")
            return redirect(
                url_for("chat.chat_manager_general", chat_hashed_id=chat_hashed_id)
            )
        if request.form.get("chat_name") is not None:
            chat.name = request.form.get("chat_name")
            db.session.commit()
            flash("Имя чата успешно изменено", "success")
            return redirect(
                url_for("chat.chat_manager_general", chat_hashed_id=chat_hashed_id)
            )
        if request.form.get("delete_chat") is not None:
            chat.remove()
            flash("Чат успешно удален", "success")
            return redirect("/myprofile")

    return render_template(
        "chat/chat_management_general.html",
        chat=chat,
        title=f"{chat.name} - управление",
    )



# chat management - collaborators
@chat.route("/chat/<chat_hashed_id>/management/collaborators", methods=["GET", "POST"])
@login_required
def chat_collaborators(chat_hashed_id):
    chat = Chat.query.filter_by(hashed_id=chat_hashed_id).first()

    if chat is None:
        flash("чат с таким id не найден", "error")
        return redirect("/myprofile")

    if not chat.is_my():
        flash("Вы не состоите в этом чате", "error")
        return redirect("/myprofile")

    if request.method == "POST":
        if not current_user.get_chat_relation(chat.id).role.isOwner():
            flash("Вы не имеете доступа к этой странице", "error")
            return redirect(
                url_for("chat.chat_collaborators", chat_hashed_id=chat_hashed_id)
            )
        if request.form.get("upgrade_to_owner") is not None:
            user_id = request.form.get("upgrade_to_owner")
            user = User.query.filter_by(id=user_id).first()
            if user is None:
                flash("Пользователь не найден", "error")
                return redirect(
                    url_for("chat.chat_collaborators", chat_hashed_id=chat_hashed_id)
                )
            user_relation = user.get_chat_relation(chat.id)
            if user_relation is None:
                flash("Такого пользователя нет в чате", "error")
                return redirect(
                    url_for("chat.chat_collaborators", chat_hashed_id=chat_hashed_id)
                )
            if user_relation.role.isOwner():
                flash("Пользователь уже владелец чата", "warning")
                return redirect(
                    url_for("chat.chat_collaborators", chat_hashed_id=chat_hashed_id)
                )
            user_relation.role = Owner
            # current_user.get_chat_relation(chat.id).role = Participant
            db.session.commit()
            flash(
                f"Права владельца успешно выданы пользователю {user.name}", "success"
            )
            return redirect(
                url_for("chat.chat_participants", chat_hashed_id=chat_hashed_id)
            )

        elif request.form.get("downgrade_to_participant") is not None:
            user_id = request.form.get("downgrade_to_participant")
            user = User.query.filter_by(id=user_id).first()
            if user is None:
                flash("Пользователь не найден", "error")
                return redirect(
                    url_for("chat.chat_collaborators", chat_hashed_id=chat_hashed_id)
                )
            user_relation = user.get_chat_relation(chat.id)
            if user_relation is None:
                flash("Такого пользователя нет в чате", "error")
                return redirect(
                    url_for("chat.chat_collaborators", chat_hashed_id=chat_hashed_id)
                )
            if user_relation.role.isParticipant():
                flash("Пользователь уже участник чата", "warning")
                return redirect(
                    url_for("chat.chat_collaborators", chat_hashed_id=chat_hashed_id)
                )
            if user.id == current_user.id and chat.count_owners() == 1:
                flash(
                    "Вы единственный владелец чата, понижение невозможно",
                    "warning",
                )
                return redirect(
                    url_for("chat.chat_collaborators", chat_hashed_id=chat_hashed_id)
                )
            user_relation.role = Participant
            db.session.commit()
            flash(f"Пользователь {user.name} успешно понижен до участника", "success")
            return redirect(
                url_for("chat.chat_participants", chat_hashed_id=chat_hashed_id)
            )

        elif request.form.get("remove_participant") is not None:
            user_id = request.form.get("remove_participant")
            user = User.query.filter_by(id=user_id).first()
            if user is None:
                flash("Пользователь не найден", "error")
                return redirect(
                    url_for("chat.chat_collaborators", chat_hashed_id=chat_hashed_id)
                )
            user_relation = user.get_chat_relation(chat.id)
            if user_relation is None:
                flash("Такого пользователя нет в чате", "error")
                return redirect(
                    url_for("chat.chat_collaborators", chat_hashed_id=chat_hashed_id)
                )
            if user_id == current_user.id:
                flash("Вы не можете удалить себя из чата на этой странице", "error")
                return redirect(
                    url_for("chat.chat_collaborators", chat_hashed_id=chat_hashed_id)
                )
            if user_relation.role.isOwner():
                flash("Удалить владельца невозможно, сначала понизьте его до участника")
                return redirect(
                    url_for("chat.chat_collaborators", chat_hashed_id=chat_hashed_id)
                )
            db.session.delete(user_relation)
            db.session.commit()
            flash(f"Пользователь {user.name} успешно удалён", "success")
            return redirect(
                url_for("chat.chat_collaborators", chat_hashed_id=chat_hashed_id)
            )
        elif request.form.get("new_invite_code") is not None:
            print("gen try")
            chat.act_generate_new_invite_code()
                
            return redirect(
                url_for("chat.chat_collaborators", chat_hashed_id=chat_hashed_id)
            )

    return render_template(
        "chat/chat_management_collaborators.html",
        chat=chat,
        title=f"{chat.name} - участники",
    )

@socketio.on("connect")
def connect(auth):
    for uc in current_user.user_chats:
        join_room(uc.chat.hashed_id)

@socketio.on("disconnect")
def disconnect():
    for uc in current_user.user_chats:
        leave_room(uc.chat.hashed_id)

@socketio.on("message")
def message(data):
    room = data['room']
    chat = Chat.query.filter_by(hashed_id=room).first()
    if chat is None:
        flash("Чат с таким id не найден", "error")
        return
    uc = User_Chat.query.filter_by(user=current_user, chat=chat).first()
    if uc is None:
        flash("Вы не присоединились к этому чату", "error")
        return
    message = Message(content=data['message'], user_chat=uc)
    message.add()

    content = {
        "user": current_user.name,
        "message": data['message'],
        "date": str_from_dt(message.date)
    }

    send(content, to=room)
    print(f"{current_user.name} sent {content} to {chat.name}")