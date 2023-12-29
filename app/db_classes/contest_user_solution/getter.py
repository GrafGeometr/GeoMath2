from app.db_classes.standard_model.getter import StandardModelGetter
class ContestUserSolutionGetter(StandardModelGetter):
    def by_contest_problem(self, contest_problem):
        self.manager.filter(self.manager.normal_cls.contest_problem_id == contest_problem.id)
        return self
    
    def by_contest_user(self, contest_user):
        self.manager.filter(self.manager.normal_cls.contest_user_id == contest_user.id)
        return self