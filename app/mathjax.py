from .imports import *
from .model_imports import *

mathjax = Blueprint('mathjax', __name__)

@mathjax.route("/mathjax_test")
def mathjax_test():
    return render_template("mathjax_test.html")