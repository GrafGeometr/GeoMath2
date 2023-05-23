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