from app.db_classes.standard_model.getter import StandardModelGetter
class ContestToProblemRelationGetter(StandardModelGetter):
    def by_contest(self,contest):
        self.manager.filter(self.manager.normal_cls.contest == contest)
        return self
    def by_problem(self,problem):
        self.manager.filter(self.manager.normal_cls.problem == problem)
        return self
    def by_user(self,user):
        self.manager.filter(self.manager.normal_cls.user == user)
        return self