from .imports import *
from .model_imports import *

general = Blueprint("general", __name__)


# get problem image
@general.route("/get_image/<db_filename>", methods=["GET", "POST"])
@login_required
def get_image(db_filename):
    attachment = Attachment.get.by_db_filename(db_filename).first()
    if attachment.is_null():
        print("attachment none")
        return
    par = attachment.get_parent()
    if par.is_null():
        print("parent none")
        return
    pt = attachment.parent_type
    try:
        if pt.name == "Problem":
            flag = None
            if not attachment.other_data["is_secret"]:
                flag = par.is_statement_available()
            else:
                flag = par.is_solution_available()
            if flag:
                print("OK, sending", attachment.short_name)
                img = send_from_directory(
                    os.path.join(basedir, attachment.db_folder.split("app/")[1]),
                    db_filename,
                    as_attachment=True,
                )
                print(img)
                return send_from_directory(
                    os.path.join(basedir, attachment.db_folder.split("app/")[1]),
                    db_filename,
                    as_attachment=True,
                )

        if pt.name == "Sheet":
            flag = par.is_text_available()
            if flag:
                return send_from_directory(
                    os.path.join(basedir, attachment.db_folder.split("app/")[1]),
                    db_filename,
                    as_attachment=True,
                )

        if pt.name == "Contest_User_Solution":
            flag = par.is_available()
            if flag:
                return send_from_directory(
                    os.path.join(basedir, attachment.db_folder.split("app/")[1]),
                    db_filename,
                    as_attachment=True,
                )

    except Exception as e:
        print(e)
        return


@general.route("/autocomplete", methods=["POST"])
@login_required
def autocomplete():
    data = request.get_json()
    obj = data["obj"]
    if obj == "tags":
        tags = Tag.get.all()
        return sorted([tag.name for tag in tags])
    elif obj == "users":
        users = User.get.all()
        return [user.name for user in users]
    elif obj == "pools":
        return [up.pool.name for up in current_user.get_user_pools()]
    elif obj == "olimpiads":
        olimpiads = Olimpiad.get.all()
        return [olimpiad.name for olimpiad in olimpiads]
    else:
        return []


@general.route("/like", methods=["POST"])
@login_required
def like():
    data = request.get_json()

    parent_type = data.get("parent_type")
    parent_id = int(data.get("parent_id"))
    action = data.get("action")

    if parent_type == "Problem":
        parent = Problem.get.by_id(parent_id).first()
    elif parent_type == "Sheet":
        parent = Sheet.get.by_id(parent_id).first()
    elif parent_type == "Contest":
        parent = Contest.get.by_id(parent_id).first()

    if action == "add_like":
        Like.act_add_like_to_parent(parent, current_user, True)
    elif action == "add_dislike":
        Like.act_add_like_to_parent(parent, current_user, False)
    elif action == "remove":
        Like.act_remove_like_from_parent(parent)

    check = None
    like = Like.get.by_parent(parent).by_user(current_user).first()
    check = like.good
    cnt_likes = parent.total_likes
    cnt_dislikes = parent.total_dislikes
    return {"check": check, "cnt_likes": cnt_likes, "cnt_dislikes": cnt_dislikes}


@general.route("/notifications", methods=["POST"])
@login_required
def notifications():
    data = request.get_json()
    if data.get("remove") is not None:
        remove_id = data.get("remove")
        notification = Notification.get.by_id(remove_id).first()
        if notification.user == current_user:
            notification.remove()
    elif data.get("mark_all_as_read") is not None:
        Notification.mark_all_as_read()

    return "OK"


@general.route("/get_tags_structure", methods=["POST"])
@login_required
def get_tags_structure():
    data = request.get_json()

    resp = [topic.JSON for topic in Topic.get.all()]

    return resp
    
@general.route("/get_tags_by_problem", methods=["POST"])
@login_required
def get_tags_by_problem():
    data = request.get_json()
    id = data.get("id")
    obj = Problem.get.by_id(id).first()

    return [tag.name for tag in obj.tags]

@general.route("/get_tags_by_sheet", methods=["POST"])
@login_required
def get_tags_by_sheet():
    data = request.get_json()
    id = data.get("id")
    obj = Sheet.get.by_id(id).first()
    print(obj.tags)

    return [tag.name for tag in obj.tags]

@general.route("/get_tags_by_contest", methods=["POST"])
@login_required
def get_tags_by_contest():
    data = request.get_json()
    id = data.get("id")
    obj = Contest.get.by_id(id).first()

    return [tag.name for tag in obj.tags]