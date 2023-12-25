from .normal import Attachment
from .null import NullAttachment

class SelectManager:
    normal_cls = Attachment

    @staticmethod
    def filter(condition: bool) -> None:
        SelectManager.normal_cls.query = SelectManager.normal_cls.query.filter(condition)

    @staticmethod
    def order_by(order) -> None:
        if order is not None:
            SelectManager.normal_cls.query = SelectManager.normal_cls.query.order_by(order)

    @staticmethod
    def all() -> list[normal_cls]:
        return SelectManager.normal_cls.query.all()
    
    @staticmethod
    def first() -> normal_cls:
        res = SelectManager.normal_cls.query.first()
        if res is not None:
            return res
        return SelectManager.normal_cls.null_cls()
