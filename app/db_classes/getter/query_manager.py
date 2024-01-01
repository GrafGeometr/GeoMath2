class QueryManager:
    def __init__(self, normal_cls):
        self.normal_cls = normal_cls
        self.filters = []

    def filter(self, condition: bool) -> None:
        self.filters.append(condition)

    def order_by(self, order) -> None:
        if order is not None:
            self.normal_cls.query = self.normal_cls.query.order_by(order)

    def all(self):
        from sqlalchemy import and_, true
        return self.normal_cls.query.where(and_(true(), *self.filters)).all()
    
    def first(self):
        from sqlalchemy import and_, true
        res = self.normal_cls.query.where(and_(true(), *self.filters)).first()
        if res is not None:
            return res
        return self.normal_cls.null_cls_()
