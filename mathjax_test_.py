from all_imports_ import *

@app.route("/mathjax_test")
def mathjax_test():
    return render_template("mathjax_test.html")