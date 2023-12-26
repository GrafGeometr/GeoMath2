from .query_manager import QueryManager


class BaseGetter:
    def __init__(self, normal_cls):
        self.manager = QueryManager(normal_cls)

    def all(self):
        return self.manager.all()

    def first(self):
        return self.manager.first()


class NullGetter:
    def __init__(self, normal_cls):
        self.normal_cls = normal_cls

    def all(self):
        return []

    def first(self):
        return self.normal_cls.null_cls()

    def __getattr__(self, item):
        return self

    def __call__(self, *args, **kwargs):
        return self
