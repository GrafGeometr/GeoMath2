from app.db_classes.getter.getter import BaseGetter
class Getter(BaseGetter):
    def by_id(self, id):
        self.manager.filter(self.manager.normal_cls.id == id)
        return self
    
    def by_name(self,name):
        self.manager.filter(self.manager.normal_cls.name == name)
        return self

