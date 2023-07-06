from app.imports import *
from app.sqlalchemy_custom_types import *

class Contest(db.Model):
    # --> INITIALIZE
    __tablename__ = "contest"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String)
    description = db.Column(db.String)
    start_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)
    is_public = db.Column(db.Boolean, default=False)

    # --> RELATIONS
    contest_problems = db.relationship("Contest_Problem", backref="contest")
    contest_judges = db.relationship("Contest_Judge", backref="contest")
    contest_users = db.relationship("Contest_User", backref="contest")
    pool_id = db.Column(db.Integer, db.ForeignKey("pool.id"))

    # --> FUNCTIONS
    def is_archived(self):
        return self.is_public

    def is_description_available(self):
        return self.is_public or self.is_my()

    def is_my(self, user=current_user):
        return user.is_pool_access(self.pool_id)
    
    def is_started(self):
        return self.start_date <= current_time()
    
    def is_ended(self):
        return self.end_date <= current_time()
    
    @staticmethod
    def get_by_id(id):
        if id is None:
            return None
        return Contest.query.filter_by(id=id).first()

    def get_tags(self):
        from app.dbc import Tag, Tag_Relation
        return sorted(
            [
                Tag.query.filter_by(id=sheet_tag.tag_id).first()
                for sheet_tag in Tag_Relation.query.filter_by(
                    parent_type="Contest", parent_id=self.id
                ).all()
            ],
            key=lambda t: t.name.lower(),
        )

    def get_tag_names(self):
        return list(map(lambda t: t.name, self.get_tags()))

    def get_problems(self):
        from app.dbc import Problem, Contest_Problem
        result = []
        for cp in Contest_Problem.query.filter_by(contest_id=self.id).all():
            result.append(Problem.query.filter_by(id=cp.problem_id).first())
        return result

    def get_judges(self):
        return [cj.user for cj in self.contest_judges]
    
    def get_nonsecret_problems(self):
        return [p for p in self.get_problems() if p.is_statement_available()]

    def get_active_cu(self, user=current_user):
        from app.dbc import Contest_User
        for cu in Contest_User.query.filter_by(
            user_id=user.id, contest_id=self.id
        ).all():
            if not cu.is_ended():
                return cu
        return None
    
    def get_idx_by_contest_problem(self, contest_problem):
        cproblems = [cp for cp in self.contest_problems if cp.is_accessible()]
        if contest_problem not in cproblems:
            return None
        return cproblems.index(contest_problem) + 1
    
    def act_register(self, user=current_user, mode="real", start_date=None, end_date=None):
        # регистрация user на контест, если виртуально - то с указанием начала и завершения
        # mode = "real" / "virtual", start=end='%Y-%m-%dT%H:%M' (строка в таком формате, надо преобразовать в datetime)
        from app.dbc import Contest_User, Contest_User_Solution
        if not self.is_archived():
            return
        cu = self.get_active_cu()
        if cu:
            return
        if mode == "real":
            if not self.is_started():
                cu = Contest_User(
                    contest_id=self.id,
                    user_id=user.id,
                    start_date=self.start_date,
                    end_date=self.end_date,
                    virtual=False,
                )
            elif not self.is_ended():
                cu = Contest_User(
                    contest_id=self.id,
                    user_id=user.id,
                    start_date=current_time(),
                    end_date=self.end_date,
                    virtual=False,
                )
            else:
                return
            cu.add()
            return
        else:
            try:
                start = datetime.datetime.strptime(start_date, '%Y-%m-%dT%H:%M')
            except:
                start = None
            try:
                end = datetime.datetime.strptime(end_date, '%Y-%m-%dT%H:%M')
            except:
                end = None
            if (
                (start is None)
                or (end is None)
                or (start > end)
            ):
                return
            cu = Contest_User(
                contest_id=self.id,
                user_id=user.id,
                start_date=start,
                end_date=end,
                virtual=True,
            )
            cu.add()
            return

    def act_stop(self, user=current_user):
        if not self.is_archived():
            return
        cu = self.get_active_cu(user)
        print(cu)
        if not cu:
            return
        cu.act_stop()
    
    def act_add_judge(self, user):
        from app.dbc import Contest_Judge
        if user is None:
            return
        if not self.is_my():
            return
        if user.is_judge(self):
            return
        cj = Contest_Judge(contest_id=self.id, user_id=user.id)
        cj.add()

    def act_add_judge_by_name(self, name):
        from app.dbc import User
        self.act_add_judge(User.query.filter_by(name=name).first())

    def act_remove_judge(self, user):
        from app.dbc import Contest_Judge
        if user is None:
            return
        if not self.is_my():
            return
        if not user.is_judge(self):
            return
        cj = Contest_Judge.query.filter_by(contest_id=self.id, user_id=user.id).first()
        cj.remove()

    def act_remove_judge_by_name(self, name):
        from app.dbc import User
        self.act_remove_judge(User.query.filter_by(name=name).first())

    def act_update_judges(self, names):
        for judge in [cj.user for cj in self.contest_judges]:
            self.act_remove_judge(judge)
        for name in names:
            self.act_add_judge_by_name(name)

    def act_remove_problem(self, problem):
        from app.dbc import Contest_Problem
        if problem is None:
            return
        if not self.is_my():
            return
        if not problem.is_in_contest(self):
            return
        cp = Contest_Problem.query.filter_by(contest_id=self.id, problem_id=problem.id).first()
        cp.remove()

    def act_add_problem(self, problem, max_score=7):
        from app.dbc import Contest_Problem
        if problem is None:
            return
        if not self.is_my():
            return
        if problem.is_in_contest(self):
            return
        cp = Contest_Problem(contest_id=self.id, problem_id=problem.id)
        cp.add()
        cp.act_set_max_score(max_score)

    def act_add_problem_by_hashed_id(self, hashed_id, max_score=7):
        from app.dbc import Problem
        problem = Problem.query.filter_by(hashed_id=hashed_id).first()
        self.act_add_problem(problem, max_score)

    def act_update_problem_score(self, problem, score):
        from app.dbc import Contest_Problem
        if problem is None:
            return
        if not self.is_my():
            return
        if not problem.is_in_contest(self):
            return
        cp = Contest_Problem.query.filter_by(contest_id=self.id, problem_id=problem.id).first()
        cp.act_set_max_score(score)

    def act_update_problem_score_by_hashed_id(self, hashed_id, score):
        from app.dbc import Problem
        problem = Problem.query.filter_by(hashed_id=hashed_id).first()
        self.act_update_problem_score(problem, score)


    def act_update_problems(self, hashes, scores):
        print(hashes, scores)
        if len(hashes) != len(scores):
            return
        for i in range(len(hashes)):
            self.act_add_problem_by_hashed_id(hashes[i], scores[i])
        for i in range(len(hashes)):
            self.act_update_problem_score_by_hashed_id(hashes[i], scores[i])
        for cp in self.contest_problems:
            if cp.problem.hashed_id not in hashes:
                cp.remove()
        