from .imports import *
from .model_imports import *

from pool import pool



@pool.route("/pool/<pool_hashed_id>/management")
def pool_manager(pool_hashed_id): # ok
    pool = Pool.query.filter_by(hashed_id = pool_hashed_id).first()

    if pool is None:
        return "pool not found" # TODO rework errors system
    
    return render_template("pool/pool_management.html", current_pool=pool, title=f"{pool.name} - управление")
