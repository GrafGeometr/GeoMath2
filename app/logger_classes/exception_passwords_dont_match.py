from app.logger_classes.register_exception import RegisterException


class ExceptionPasswordsDontMatch(RegisterException):
    def __init__(self, target, *args):
        self.content = "Пароли не совпадают"
        super().__init__(target, *args)
