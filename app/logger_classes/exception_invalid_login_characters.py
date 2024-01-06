from app.logger_classes.register_exception import RegisterException


class ExceptionInvalidLoginCharacters(RegisterException):
    def __init__(self, target, *args):
        self.content = "Некорректный логин, допустимые символы: A-Z a-z 0-9 _ - ."
        super().__init__(target, *args)
