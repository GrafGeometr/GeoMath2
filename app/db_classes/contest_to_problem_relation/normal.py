from typing import List

from app.imports import *

from app.db_classes.standard_model.normal import StandardModel
from .abstract import AbstractContestToProblemRelation
from .null import NullContestToProblemRelation
from .getter import ContestToProblemRelationGetter


class ContestToProblemRelation(StandardModel, AbstractContestToProblemRelation):
    # --> INITIALIZE
    __abstract__ = False
    __tablename__ = "contest_to_problem_relation"

    null_cls_ = NullContestToProblemRelation
    getter_cls_ = ContestToProblemRelationGetter

    max_score_ = db.Column(db.Integer, default=7)
    list_index_ = db.Column(db.Integer)

    # --> RELATIONS
    contest_id_ = db.Column(db.Integer, db.ForeignKey("contest.id_"))
    problem_id_ = db.Column(db.Integer, db.ForeignKey("problem.id_"))
    contest_user_solutions_ = db.relationship(
        "ContestUserSolution", backref="contest_to_problem_relation_"
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
    def contest(self) -> "AbstractContest":
        return self.contest_

    @contest.setter
    def contest(self, contest: "AbstractContest"):
        self.contest_ = contest
        self.save()

    @property
    def problem_id(self) -> int:
        return self.problem_id_

    @problem_id.setter
    def problem_id(self, problem_id: int):
        self.problem_id_ = problem_id
        self.save()

    @property
    def problem(self) -> "AbstractProblem":
        return self.problem_

    @problem.setter
    def problem(self, problem: "AbstractProblem"):
        self.problem_ = problem
        self.save()

    @property
    def contest_user_solutions(self) -> List["ContestUserSolution"]:
        return self.contest_user_solutions_

    @contest_user_solutions.setter
    def contest_user_solutions(
        self, contest_user_solutions: List["ContestUserSolution"]
    ):
        self.contest_user_solutions_ = contest_user_solutions
        self.save()

    # --> FUNCTIONS
    def add(self):
        from app.dbc import ContestUserSolution

        db.session.add(self)
        db.session.commit()
        for cu in self.contest.contest_users:
            ContestUserSolution(contest_user=cu, contest_problem=self).add()
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
        from app.dbc import ContestToUserRelation, ContestUserSolution

        contest_user = ContestToUserRelation.get_active_by_contest_and_user(
            self.contest, user
        )
        return ContestUserSolution.get.by_contest_problem(self).get_by_contest_user(
            contest_user
        )
