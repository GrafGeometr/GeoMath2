from all_imports_ import *
from data.pool import Pool
from data.user import User
from data.user_pool import UserPool


@route("/accept_pool_invitation")
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

    return "ok"


@route("/decline_pool_invitation")
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

    return "ok"


@route("/pools/<pool_hashed_id>/problems")
def get_pool_problems(pool_hashed_id):
    db_sess = db_session.create_session()

    pool = db_sess.query(Pool).filter(Pool.hashed_id == pool_hashed_id).first()

    if pool is None:
        return "pool not found"
    
    return render_template("pool_problems.html", current_pool=pool)


@route("/pool/<pool_hashed_id>/participants")
def get_pool_participants(pool_hashed_id):
    db_sess = db_session.create_session()

    pool = db_sess.query(Pool).filter(Pool.hashed_id == pool_hashed_id).first()

    if pool is None:
        return "pool not found"
    
    return render_template("pool_participants.html", current_pool=pool)


@route("/pools/create")
def create_pool():
    pass
