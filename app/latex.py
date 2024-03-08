from .imports import *
from .model_imports import *

latex = Blueprint("mathjax", __name__)


@latex.route("/latex_test")
def mathjax_test():
    return render_template("wip/latex_test.html")


@latex.route("/blocks_test")
def blocks_test():
    return render_template("wip/blocks_test.html")
