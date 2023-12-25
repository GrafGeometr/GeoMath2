from .query_manager import QueryManager

class Getter:
    manager = QueryManager

    @staticmethod
    def by_id(id):
        Getter.manager.filter(Getter.manager.normal_cls.id == id)
    
    @staticmethod
    def by_short_name(name):
        Getter.manager.filter(Getter.manager.normal_cls.name == name)

    @staticmethod
    def all():
        return Getter.manager.all()
    
    @staticmethod
    def first():
        return Getter.manager.first()

