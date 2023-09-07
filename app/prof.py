from .imports import *
from .model_imports import *

prof = Blueprint('prof', __name__)



@prof.route("/show_profile_pic/<path:filename>")
def show_profile_pic(filename):
    print(filename)
    try:
        return send_from_directory(os.path.join(basedir, 'database/profile_pics'), filename, as_attachment=True)
    except Exception as e:
        print(e)

@prof.route("/myprofile")
@login_required
def to_profile():
    return redirect(f"/profile/user/{current_user.name}")
    

def squarify(d, f):
    path = os.path.join(d, f)
    img = Image.open(path)
    x, y = img.size
    if x > y:
        img = img.crop(((x-y)//2, 0, (x+y)//2, y))
    else:
        img = img.crop((0, (y-x)//2, x, (y+x)//2))
    img.save(path)


@prof.route("/profile/user/<username>", methods=["GET", "POST"])
@login_required
def profile(username):
    user = User.query.filter_by(name = username).first()
    if user is None:
        flash("Пользователь не найден", "error")
        return redirect("/myprofile")
    if request.method == "POST":
        if request.form.get("chat_with_user") is not None:
            if user.name == current_user.name:
                return redirect(f"/profile/user/{user.name}")
            
            current_user_nonclub = current_user.get_nonclub_chats()
            user_nonclub = user.get_nonclub_chats()
            for chat in current_user_nonclub:
                if (chat in user_nonclub):
                    return redirect(f"/chat/{chat.hashed_id}/messages")
            
            chat = Chat(name="")
            chat.add()
            User_Chat(user=current_user, chat=chat).add()
            User_Chat(user=user, chat=chat).add()
            return redirect(f"/chat/{chat.hashed_id}/messages")
        if request.form.get("update_profile_pic") is not None:
            if user.name != current_user.name:
                return redirect(f"/profile/user/{user.name}")
            directory = 'app/database/profile_pics'
            file = request.files.get("profile_pic")
            if file is None:
                flash("Файл не был загружен", "error")
                return redirect(f"/myprofile")
            filenames = safe_image_upload([file], directory, 5*1024*1024)
            if filenames and filenames[0] is not None:
                filename = filenames[0]
                try:
                    os.remove(os.path.join(directory, current_user.profile_pic))
                except:
                    pass
                squarify(directory, filename)
                current_user.profile_pic = filename
                db.session.commit()
                return redirect(f"/profile/user/{user.name}")
        if request.form.get("delete_profile_pic") is not None:
            if user.name != current_user.name:
                return redirect(f"/profile/user/{user.name}")
            directory = 'app/database/profile_pics'
            try:
                os.remove(os.path.join(directory, current_user.profile_pic))
            except:
                pass
            current_user.profile_pic = None
            db.session.commit()
            return redirect(f"/profile/user/{user.name}")
        if request.form.get("save_about") is not None:
            if user.name != current_user.name:
                return redirect(f"/profile/user/{user.name}")
            current_user.about = request.form.get("about")
            db.session.commit()
            return redirect(f"/profile/user/{user.name}")



    title = "Мой профиль"
    if user.name != current_user.name:
        title = f"Профиль {user.name}"
    return render_template("profile/profile_about.html", title=title, user=user)


@prof.route("/profile/pools")
@login_required
def profile_pools():
    return render_template("profile/profile_pools.html", title="Мои пулы", user=current_user, str_from_dt = str_from_dt)


@prof.route("/profile/clubs")
@login_required
def profile_clubs():
    return render_template("profile/profile_clubs.html", title="Мои кружки", user=current_user)

@prof.route("/profile/chats", methods=["GET", "POST"])
@login_required
def profile_chats():
    if request.method == "POST":
        if request.form.get("remove_chat") is not None:
            chat_id = request.form.get("remove_chat")
            chat = Chat.query.filter_by(id=chat_id).first()
            if (chat is None) or (chat.club_id is not None) or (not chat.is_my()):
                flash("Чат не найден", "error")
                return redirect("/profile/chats")
            chat.remove()
            return redirect("/profile/chats")
        if request.form.get("cmd") is not None:
            cmd = request.form.get("cmd")
            if cmd == "remove_friend":
                friend_id = request.form.get("friend_id")
                user = User.query.filter_by(id=friend_id).first()
                if (user is not None):
                    for friend in Friend.query.all():
                        f,t = friend.friend_from, friend.friend_to
                        if (friend.accepted) and ((f,t)==(user.id,current_user.id) or (f,t)==(current_user.id,user.id)):
                            friend.remove()
                            return redirect("/profile/chats")
                        
            elif cmd == "accept_friend":
                friend_id = request.form.get("friend_id")
                user = User.query.filter_by(id=friend_id).first()
                if (user is not None):
                    for friend in Friend.query.all():
                        if friend.friend_from == user.id and friend.friend_to == current_user.id and (not friend.accepted):
                            friend.act_accept()
                            return redirect("/profile/chats")
                        
            elif cmd == "reject_friend":
                friend_id = request.form.get("friend_id")
                user = User.query.filter_by(id=friend_id).first()
                if (user is not None):
                    for friend in Friend.query.all():
                        if friend.friend_from == user.id and friend.friend_to == current_user.id and (not friend.accepted):
                            friend.remove()
                            return redirect("/profile/chats")

            elif cmd == "cancel_friend":
                friend_id = request.form.get("friend_id")
                user = User.query.filter_by(id=friend_id).first()
                if (user is not None):
                    for friend in Friend.query.all():
                        if friend.friend_from == current_user.id and friend.friend_to == user.id and (not friend.accepted):
                            friend.remove()
                            return redirect("/profile/chats")
                        
            elif cmd == "send_friend":
                friend_id = request.form.get("friend_id")
                user = User.query.filter_by(id=friend_id).first()
                if (user is not None) and (user != current_user):
                    if (user not in current_user.get_friends_to()) and (user not in current_user.get_friends_from()) and (user not in current_user.get_friends()):
                        friend = Friend(friend_from=current_user.id, friend_to=user.id, accepted=False)
                        friend.add()
                        return redirect("/profile/chats")
            
            
    return render_template("profile/profile_chats.html", title="Мои чаты", user=current_user)

@prof.route("/profile/settings")
@login_required
def profile_settings():
    return render_template("profile/profile_settings.html", title="Настройки", user=current_user)