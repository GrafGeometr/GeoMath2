from .query_manager import QueryManager

class BaseGetter:
    def __init__(self, normal_cls):
        self.manager = QueryManager(normal_cls)

    def all(self):
        return self.manager.all()
    
    def first(self):
        return self.manager.first()

