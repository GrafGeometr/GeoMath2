from app.logger_classes.register_exception import RegisterException


class ExceptionPasswordIsTooShort(RegisterException):
    def __init__(self, target, *args):
        self.content = "Длина пароля должна быть не менее 6 символов"
        super().__init__(target, *args)
