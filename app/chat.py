from .imports import *
from .model_imports import *

chat = Blueprint('chat', __name__)




@chat.route("/chat/<chat_hashed_id>/messages", methods=["GET", "POST"])
@login_required
def chat_messages(chat_hashed_id):
    chat = Chat.query.filter_by(hashed_id=chat_hashed_id).first()
    if chat is None:
        flash("Чат с таким id не найден", "error")
        return redirect("/profile/chats")
    if not chat.is_my():
        flash("Вы не состоите в этом чате", "error")
        return redirect("/profile/chats")
    chat.act_mark_all_as_read()
    return render_template("chat/chat_messages.html", chat=chat, messages=chat.get_all_messages(), str_from_dt = str_from_dt)


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

    if chat.club_id is None:
        flash("Страница недоступна", "error")
        return redirect(f"/chat/{chat_hashed_id}/messages")

    if request.method == "POST":
        if not current_user.is_chat_owner(chat):
            flash("Вы не имеете доступа к этой странице", "error")
            return redirect(
                url_for("chat.chat_manager_general", chat_hashed_id=chat_hashed_id)
            )
        if request.form.get("chat_name") is not None:
            chat.name = request.form.get("chat_name")
            db.session.commit()
            flash("Название чата успешно изменено", "success")
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
        return redirect("/profile/chats")

    if not chat.is_my():
        flash("Вы не состоите в этом чате", "error")
        return redirect("/profile/chats")
    
    if chat.club_id is None:
        flash("Страница недоступна", "error")
        return redirect(f"/chat/{chat_hashed_id}/messages")

    if request.method == "POST":
        if not current_user.is_chat_owner(chat):
            flash("Вы не имеете доступа к этой странице", "error")
            return redirect(
                url_for("chat.chat_collaborators", chat_hashed_id=chat_hashed_id)
            )
        if request.form.get("toggle_access") is not None:
            chat.readonly = (request.form.get("toggle_access") == "true")
            db.session.commit()

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
    if (chat.readonly and (not current_user.is_chat_owner(chat))):
        flash("Недостаточно прав", "error")
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