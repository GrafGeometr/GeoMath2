from app.imports import *

from app.db_classes.standard_model.normal import StandardModel
from .abstract import AbstractContestToProblemRelation
from .null import NullContestToProblemRelation
from .getter import ContestToProblemRelationGetter


class ContestToProblemRelation(StandardModel):
    # --> INITIALIZE
    __abstract__ = False
    __tablename__ = "contest_problem"

    null_cls_ = NullContestToProblemRelation
    getter_cls_ = ContestToProblemRelationGetter

    max_score_ = db.Column(db.Integer, default=7)
    list_index_ = db.Column(db.Integer)

    # --> RELATIONS
    contest_id_ = db.Column(db.Integer, db.ForeignKey("contest.id_"))
    problem_id_ = db.Column(db.Integer, db.ForeignKey("problem.id_"))
    contest_user_solutions_ = db.relationship(
        "Contest_User_Solution", backref="contest_problem"
    )

    # --> PROPERTIES
    @property
    def max_score(self) -> int:
        return self.max_score_
    
    @max_score.setter
    def max_score(self, max_score: int):
        self.max_score_ = max_score
        self.save()

    @property
    def list_index(self) -> int:
        return self.list_index_
    
    @list_index.setter
    def list_index(self, list_index: int):
        self.list_index_ = list_index
        self.save()

    @property
    def contest_id(self) -> int:
        return self.contest_id_
    
    @contest_id.setter
    def contest_id(self, contest_id: int):
        self.contest_id_ = contest_id
        self.save()

    @property
    def problem_id(self) -> int:
        return self.problem_id_
    
    @problem_id.setter
    def problem_id(self, problem_id: int):
        self.problem_id_ = problem_id
        self.save()

    @property
    def contest_user_solutions(self) -> list("Contest_User_Solution"):
        return self.contest_user_solutions_
    
    @contest_user_solutions.setter
    def contest_user_solutions(self, contest_user_solutions: list("Contest_User_Solution")):
        self.contest_user_solutions_ = contest_user_solutions
        self.save()

    # --> FUNCTIONS
    def add(self):
        from app.dbc import Contest_User_Solution

        db.session.add(self)
        db.session.commit()
        for cu in self.contest.contest_users:
            Contest_User_Solution(contest_user=cu, contest_problem=self).add()
        return self

    def remove(self):
        for cus in self.contest_user_solutions:
            db.session.delete(cus)
        db.session.delete(self)
        db.session.commit()

    def act_set_list_index(self, index):
        contest = self.contest
        if len(contest.contest_problems) < index:
            return self  # TODO write normal error handling
        self.list_index = index
        return self.save()

    def act_set_max_score(self, score):
        try:
            score = int(score)
            if score <= 0:
                score = None
        except:
            score = None
        if score is None:
            if self.max_score is None:
                self.max_score = 7
        else:
            self.max_score = score
        db.session.commit()
        return self

    def is_accessible(self, user=current_user):
        return (
                self.is_valid()
                and self.problem is not None
                and self.problem.is_statement_available(user)
        )

    def is_valid(self):
        if self.problem is None or self.contest is None:
            return False
        return (
                self.problem.is_archived() or self.problem.pool.id == self.contest.pool.id
        )

    def get_active_contest_user_solution(self, user=current_user):
        if user is None:
            return None
        from app.dbc import Contest_User, Contest_User_Solution

        contest_user = Contest_User.get_active_by_contest_and_user(self.contest, user)
        return Contest_User_Solution.get_by_contest_problem_and_contest_user(
            self, contest_user
        )

    @staticmethod
    def get_by_contest_and_problem(contest, problem):
        if (
                contest is None
                or problem is None
                or contest.id is None
                or problem.id is None
        ):
            return None
        return ContestToProblemRelation.get.by_problem(problem).by_contest(contest).first()

    @staticmethod
    def get_all_by_contest(contest):
        if contest is None:
            return []
        res = sorted(
            ContestToProblemRelation.get.by_contest(contest).all(),
            key=lambda contest_problem: (
                contest_problem.list_index
                if contest_problem.list_index is not None
                else 0
            ),
        )
        return res
