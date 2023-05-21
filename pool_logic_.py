from all_imports_ import *
from data.pool import Pool
from data.user import User
from data.user_pool import UserPool


@app.route("/accept_pool_invitation", methods=["POST"])
def accept_pool_invitation():
    data = request.get_json()
    pool_hashed_id = data["pool_hashed_id"]

    db_sess = db_session.create_session()

    pool = db_sess.query(Pool).filter(Pool.hashed_id == pool_hashed_id).first()

    if pool is None:
        return "pool not found"

    user = get_current_user(db_sess)

    relation = db_sess.query(UserPool).filter(UserPool.user_id == user.id, UserPool.pool_id == pool.id).first()

    if relation is None:
        return "user not invited"
    
    relation.role = "Participant"

    db_sess.commit()
    db_sess.close()
    print("DONE")

    return "ok"


@app.route("/decline_pool_invitation", methods=["POST"])
def decline_pool_invitation():
    data = request.get_json()
    pool_hashed_id = data["pool_hashed_id"]

    db_sess = db_session.create_session()

    pool = db_sess.query(Pool).filter(Pool.hashed_id == pool_hashed_id).first()

    if pool is None:
        return "pool not found"
    
    user = get_current_user(db_sess)

    relation = db_sess.query(UserPool).filter(UserPool.user_id == user.id, UserPool.pool_id == pool.id).first()

    if relation is None:
        return "user not invited"
    
    db_sess.delete(relation)
    db_sess.commit()
    db_sess.close()

    return "ok"


@route("/pool/<pool_hashed_id>/problems")
def pool_problems(pool_hashed_id):
    db_sess = db_session.create_session()

    pool = db_sess.query(Pool).filter(Pool.hashed_id == pool_hashed_id).first()

    if pool is None:
        return "pool not found"
    
    return render_template("pool_problems.html", current_pool=pool)


@route("/pool/<pool_hashed_id>/participants")
def pool_participants(pool_hashed_id):
    db_sess = db_session.create_session()

    pool = db_sess.query(Pool).filter(Pool.hashed_id == pool_hashed_id).first()

    if pool is None:
        return "pool not found"
    
    return render_template("pool_participants.html", current_pool=pool)

@route("/pool/<pool_hashed_id>/management")
def pool_manager(pool_hashed_id):
    db_sess = db_session.create_session()

    pool = db_sess.query(Pool).filter(Pool.hashed_id == pool_hashed_id).first()

    if pool is None:
        return "pool not found"
    
    return render_template("pool_management.html", current_pool=pool)


@route("/pools/create")
def create_pool():
    return render_template("pool_create.html")

@app.route("/create_new_pool", methods=["POST"])
def create_new_pool():
    data = request.get_json()
    name = data["name"]
    db_sess = db_session.create_session()
    used_tokens = [p.hashed_id for p in db_sess.query(Pool).all()]
    hashed_id = generate_token(30)
    while hashed_id in used_tokens:
        hashed_id = generate_token(30)
    
    pool = Pool(hashed_id=hashed_id, name=name)
    db_sess.add(pool)
    db_sess.commit()


    user = get_current_user(db_sess)
    
    link = f"/pool/{hashed_id}/problems"

    relation = UserPool(user_id=user.id, pool_id=pool.id, role="Owner")
    db_sess.add(relation)
    db_sess.commit()
    db_sess.close()
    
    print(link)
    return link

@app.route("/add_participant", methods=["POST"])
def add_participant():
    data = request.get_json()
    login = data["login"]
    pool_hashed_id = data["pool_hashed_id"]
    db_sess = db_session.create_session()


    relation = UserPool(user_id=db_sess.query(User).filter(User.name == login).first().id, pool_id=db_sess.query(Pool).filter(Pool.hashed_id == pool_hashed_id).first().id, role="Invited")
    db_sess.add(relation)
    db_sess.commit()

    db_sess.close()

    return render_template("mypools.html")


@app.route("/remove_participant", methods=["POST"])
def remove_participant():
    data = request.get_json()
    login = data["login"]
    pool_hashed_id = data["pool_hashed_id"]
    db_sess = db_session.create_session()

    user = db_sess.query(User).filter(User.name == login).first()
    pool = db_sess.query(Pool).filter(Pool.hashed_id == pool_hashed_id).first()

    relation = db_sess.query(UserPool).filter(UserPool.user_id == user.id, UserPool.pool_id == pool.id).first()
    db_sess.delete(relation)

    db_sess.commit()

    db_sess.refresh(user)
    db_sess.refresh(pool)
  
    return render_template("mypools.html")