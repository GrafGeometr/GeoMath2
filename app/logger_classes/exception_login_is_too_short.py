from app.logger_classes.register_exception import RegisterException


class ExceptionLoginIsTooShort(RegisterException):
    def __init__(self, target, *args):
        self.content = "Длина логина должна быть не менее 4 символов"
        super().__init__(target, *args)
