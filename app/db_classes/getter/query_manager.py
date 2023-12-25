class QueryManager:
    def __init__(self, normal_cls):
        self.normal_cls = normal_cls

    def filter(self, condition: bool) -> None:
        self.normal_cls.query = self.normal_cls.query.filter(condition)

    def order_by(self, order) -> None:
        if order is not None:
            self.normal_cls.query = self.normal_cls.query.order_by(order)

    def all(self):
        return self.normal_cls.query.all()
    
    def first(self):
        res = self.normal_cls.query.first()
        if res is not None:
            return res
        return self.normal_cls.null_cls()
