from app.logger_classes.login_exception import LoginException


class ExceptionLoginOrPasswordWrong(LoginException):
    def __init__(self, target, *args):
        self.content = "Неверный логин или пароль"
        super().__init__(target, *args)
