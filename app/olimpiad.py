from .imports import *
from .model_imports import *

olimpiad = Blueprint("olimpiad", __name__)


@olimpiad.route("/olimpiad", methods=["GET", "POST"])
@login_required
def olimpiad_mainpage():
    olimpiads = Olimpiad.get.all()
    return render_template(
        "olimpiad/mainpage.html", olimpiads=olimpiads, title="Олимпиады"
    )


@olimpiad.route("/olimpiad/<olimpiad_id>", methods=["GET", "POST"])
@login_required
def olimpiad_tree(olimpiad_id):
    olimpiad = Olimpiad.get.by_id(olimpiad_id).first()
    return render_template(
        "olimpiad/tree.html", olimpiad=olimpiad, title=f"{olimpiad.name}"
    )
