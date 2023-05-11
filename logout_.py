from all_imports_ import *

@app.route("/logout")
def logout():
    logout_user()
    return redirect("/")