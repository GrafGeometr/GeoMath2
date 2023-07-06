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

    def is_description_available(self, user=current_user):
        if user is None:
            return False
        return self.is_public or self.is_my(user)

    def is_my(self, user=current_user):
        if user is None:
            return False
        return user.is_pool_access(self.pool_id)

    def is_started(self):
        return self.start_date <= current_time()

    def is_ended(self):
        return self.end_date <= current_time()

    def is_problem_submitted(self, problem):
        from app.dbc import Contest_Problem, Contest_User_Solution

        if problem is None:
            return False
        cu = self.get_active_cu()
        if cu is None:
            return False
        cp = Contest_Problem.get_by_contest_and_problem(self, problem)
        if cp is None:
            return False
        cus = Contest_User_Solution.get_by_contest_problem_and_contest_user(cp, cu)
        return (cus is not None) and (cus.content is not None)

    def get_tags(self):
        from app.dbc import Tag, Tag_Relation

        return sorted(
            [
                Tag.get_by_id(contest_tag.tag_id)
                for contest_tag in Tag_Relation.get_all_by_parent(self)
            ],
        )

    def get_tag_names(self):
        return list(map(lambda t: t.name.lower(), self.get_tags()))

    def get_problems(self):
        from app.dbc import Problem, Contest_Problem

        result = list(
            filter(
                lambda x: x is not None,
                [
                    Problem.get_by_id(id=cp.problem_id)
                    for cp in Contest_Problem.get_all_by_contest(self)
                ],
            )
        )
        return result

    def get_judges(self):
        return [
            cj.user
            for cj in self.contest_judges
            if cj is not None and cj.user is not None
        ]

    def get_nonsecret_problems(self):
        return [cp.problem for cp in self.contest_problems if cp.is_accessible()]

    def get_active_cu(self, user=current_user):
        from app.dbc import Contest_User

        return Contest_User.get_active_by_contest_and_user(self, user)

    def get_idx_by_contest_problem(self, contest_problem):
        cproblems = [cp for cp in self.contest_problems if cp.is_accessible()]
        if contest_problem not in cproblems:
            return None
        return cproblems.index(contest_problem) + 1

    def act_set_name(self, name):
        self.name = name
        return self.save()
    
    def act_set_description(self, description):
        self.description = description
        return self.save()

    def act_set_date(self, start_date, end_date):
        if start_date is None or end_date is None or start_date > end_date:
            return self
        self.start_date = start_date
        self.end_date = end_date
        return self.save()

    def act_register(
        self, user=current_user, mode="real", start_date=None, end_date=None
    ):
        if user is None:
            return
        print(mode, start_date, end_date)
        # регистрация user на контест, если виртуально - то с указанием начала и завершения
        # mode = "real" / "virtual", start=end='%Y-%m-%dT%H:%M' (строка в таком формате, надо преобразовать в datetime)
        from app.dbc import Contest_User, Contest_User_Solution

        if not self.is_archived():
            return
        if self.get_active_cu():
            return
        if mode == "real":
            if self.is_ended():
                return
            Contest_User(
                contest_id=self.id,
                user_id=user.id,
                start_date=self.start_date if not self.is_started() else current_time(),
                end_date=self.end_date,
                virtual=False,
            ).add()
        else:
            start = dt_from_str(start_date)
            end = dt_from_str(end_date)
            if (start is None) or (end is None) or (start > end):
                return
            Contest_User(
                contest_id=self.id,
                user_id=user.id,
                start_date=start,
                end_date=end,
                virtual=True,
            ).add()
        return self

    def act_stop(self, user=current_user):
        if not self.is_archived():
            return self
        cu = self.get_active_cu(user)
        print(cu)
        if cu is None:
            return self
        cu.act_stop()
        return self

    def act_add_judge(self, user):
        from app.dbc import Contest_Judge

        if user is None:
            return self
        if not self.is_my(user):
            return self
        if user.is_judge(self):
            return self
        Contest_Judge(contest_id=self.id, user_id=user.id).add()
        return self

    def act_add_judge_by_name(self, name):
        from app.dbc import User

        self.act_add_judge(User.get_by_name(name))
        return self

    def act_remove_judge(self, user):
        from app.dbc import Contest_Judge

        if user is None:
            return self
        if not self.is_my(user):
            return self
        cj = Contest_Judge.get_by_contest_and_user(self, user)
        if cj is not None:
            cj.remove()
        return self

    def act_remove_judge_by_name(self, name):
        from app.dbc import User

        return self.act_remove_judge(User.get_by_name(name))

    def act_set_judges(self, names):
        for judge in [
            cj.user
            for cj in self.contest_judges
            if cj is not None and cj.user is not None
        ]:
            self.act_remove_judge(judge)
        for name in names:
            self.act_add_judge_by_name(name)
        return self

    def act_remove_problem(self, problem):
        from app.dbc import Contest_Problem

        if problem is None:
            return self
        if not self.is_my():
            return self
        cp = Contest_Problem.get_by_contest_and_problem(self, problem)
        if cp is not None:
            cp.remove()
        return self

    def act_add_problem(self, problem, max_score=7):
        from app.dbc import Contest_Problem

        if problem is None:
            return self
        if not self.is_my():
            return self
        if problem.is_in_contest(self):
            return self
        cp = Contest_Problem(contest_id=self.id, problem_id=problem.id).add()
        cp.act_set_max_score(max_score)
        return self

    def act_add_problem_by_hashed_id(self, hashed_id, max_score=7):
        from app.dbc import Problem

        return self.act_add_problem(Problem.get_by_hashed_id(hashed_id), max_score)

    def act_set_problem_score(self, problem, score):
        from app.dbc import Contest_Problem

        if problem is None:
            return self
        if not self.is_my():
            return self
        if not problem.is_in_contest(self):
            return self
        cp = Contest_Problem.get_by_contest_and_problem(self, problem)
        if cp is not None:
            cp.act_set_max_score(score)
        return self

    def act_set_problem_score_by_hashed_id(self, hashed_id, score):
        from app.dbc import Problem

        return self.act_set_problem_score(Problem.get_by_hashed_id(hashed_id), score)

    def act_set_problems(self, hashes, scores):
        print(hashes, scores)
        if len(hashes) != len(scores):
            return self
        for i in range(len(hashes)):
            self.act_add_problem_by_hashed_id(hashes[i], scores[i])
        for i in range(len(hashes)):
            self.act_set_problem_score_by_hashed_id(hashes[i], scores[i])
        for cp in self.contest_problems:
            if cp.problem.hashed_id not in hashes:
                cp.remove()
        return self

    @staticmethod
    def get_by_id(id):
        return Contest.query.filter_by(id=id).first()

    @staticmethod
    def get_by_hashed_id(hashed_id):
        return Contest.query.filter_by(hashed_id=hashed_id).first()

    @staticmethod
    def get_all_by_pool(pool):
        return Contest.query.filter_by(pool_id=pool.id).all()

    def add(self):
        db.session.add(self)
        db.session.commit()
        return self

    def remove(self):
        cp_s = self.contest_problems
        cu_s = self.contest_users
        cj_s = self.contest_judges
        for cp in cp_s:
            cp.remove()
        for cj in cj_s:
            cj.remove()
        for cu in cu_s:
            cu.remove()
        db.session.delete(self)
        db.session.commit()

    def save(self):
        db.session.commit()
        return self
