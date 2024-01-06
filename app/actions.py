class NoActionContext(Exception):
    pass


class AbstractAction:
    def __str__(self):
        return f"{self.__class__.__name__}({', '.join(f'{k}={v}' for k, v in self.__dict__.items())})"

    def check_possibility(self):
        pass

    def act(self, context=None):
        pass


class Action(AbstractAction):
    def act(self, context=None):
        self.check_possibility()
        pass


class ContextOnlyAction(AbstractAction):
    def act(self, context=None):
        if context is None:
            raise NoActionContext(str(self))
