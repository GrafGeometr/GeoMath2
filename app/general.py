from .imports import *
from .model_imports import *

general = Blueprint('general', __name__)

# get problem image
@general.route("/get_image/<db_filename>", methods=["GET", "POST"])
@login_required
def get_image(db_filename):
    attachment = Attachment.query.filter_by(db_filename=db_filename).first()
    if attachment is None:
        print("attachment none")
        return
    par = attachment.get_parent()
    if par is None:
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
            if (flag):
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
            if (flag):
                return send_from_directory(
                    os.path.join(basedir, attachment.db_folder.split("app/")[1]),
                    db_filename,
                    as_attachment=True,
                )
            
        if pt.name == "Contest_User_Solution":
            flag = par.is_available()
            if (flag):
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
        tags = Tag.query.all()
        return [sorted(tag.name) for tag in tags]
    elif obj == "users":
        users = User.query.all()
        return [user.name for user in users]
    elif obj == "pools":
        return [up.pool.name for up in current_user.get_pools()]
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
        parent = Problem.query.filter_by(id=parent_id).first()
    elif parent_type == "Sheet":
        parent = Sheet.query.filter_by(id=parent_id).first()
    elif parent_type == "Contest":
        parent = Contest.query.filter_by(id=parent_id).first()

    if action == "add_like":
        Like.act_add_like_to_parent(parent, current_user, True)
    elif action == "add_dislike":
        Like.act_add_like_to_parent(parent, current_user, False)
    elif action == "remove":
        Like.act_remove_like_from_parent(parent)

    check = None
    like = Like.get_by_parent_and_user(parent, current_user)
    if like is not None:
        check = like.good
    cnt_likes = parent.total_likes
    cnt_dislikes = parent.total_dislikes
    return {"check": check, "cnt_likes": cnt_likes, "cnt_dislikes": cnt_dislikes}