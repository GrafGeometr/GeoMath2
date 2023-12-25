from .normal import User

class QueryManager:
    normal_cls = User

    @staticmethod
    def filter(condition: bool) -> None:
        QueryManager.normal_cls.query = QueryManager.normal_cls.query.filter(condition)

    @staticmethod
    def order_by(order) -> None:
        if order is not None:
            QueryManager.normal_cls.query = QueryManager.normal_cls.query.order_by(order)

    @staticmethod
    def all() -> list[normal_cls]:
        return QueryManager.normal_cls.query.all()
    
    @staticmethod
    def first() -> normal_cls:
        res = QueryManager.normal_cls.query.first()
        if res is not None:
            return res
        return QueryManager.normal_cls.null_cls()
