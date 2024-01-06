from app.logger_classes.register_exception import RegisterException


class ExceptionLoginAlreadyUsed(RegisterException):
    def __init__(self, target, *args):
        self.content = "Пользователь с таким именем уже существует"
        super().__init__(target, *args)
