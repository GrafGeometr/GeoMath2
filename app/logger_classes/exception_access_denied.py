from app.logger_classes.exception import CustomException


class ExceptionAccessDenied(CustomException):
    def __init__(self, target, *args):
        self.content = "Отказано в доступе"
        super().__init__(target, *args)
