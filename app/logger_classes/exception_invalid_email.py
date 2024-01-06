from app.logger_classes.register_exception import RegisterException


class ExceptionInvalidEmail(RegisterException):
    def __init__(self, target, *args):
        self.content = "Некорректный email"
        super().__init__(target, *args)
