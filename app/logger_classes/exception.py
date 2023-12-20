from app.imports import *
class Exception:
    def __init__(self, target):
        from app.dbc import User
        self.date = current_time()
        self.user_id = User.get_current_user().get_id()
        self.target = target
        self.log()
    def log(self):
        logger.log_exception(self)
    def flash(self):
        flash(self.get_content(), "error")


    def get_date(self):
        return self.date
    def get_user_id(self):
        return self.user_id
    def get_target(self):
        return self.target
    def get_content(self):
        return self.content
    
    def __str__(self):
        s = ""
        s += f"DATE   : \t{self.get_date()}" + "\n"
        s += f"USER_ID: \t{self.get_user_id()}" + "\n"
        s += f"TARGET : \t{self.get_target()}" + "\n"
        s += f"CONTENT: \t{self.get_content()}" + "\n"
        return s