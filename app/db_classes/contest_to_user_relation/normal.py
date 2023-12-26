from app.imports import *

from app.db_classes.standard_model.normal import StandardModel
from .abstract import AbstractChat
from .null import NullChat
from .getter import Getter


class ContestToUserRelation(StandardModel):
    # --> INITIALIZE
    __tablename__ = "contest_user"

    start_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)
    virtual = db.Column(db.Boolean, default=False)

    # --> RELATIONS
    contest_id = db.Column(db.Integer, db.ForeignKey("contest.id_"))
    user_id = db.Column(db.Integer, db.ForeignKey("user.id_"))
    contest_user_solutions = db.relationship(
        "Contest_User_Solution", backref="contest_user"
    )

    # --> FUNCTIONS

    def add(self):
        from app.dbc import Contest_User_Solution

        db.session.add(self)
        db.session.commit()
        for cp in self.contest.contest_problems:
            Contest_User_Solution(
                contest_user_id=self.id, contest_problem_id=cp.id
            ).add()
        return self

    def remove(self):
        for cus in self.contest_user_solutions:
            db.session.delete(cus)
        db.session.delete(self)
        db.session.commit()

    def is_started(self):
        return self.start_date <= current_time()

    def is_ended(self):
        return self.end_date <= current_time()

    def is_active(self):
        return not self.is_ended()

    def is_any_cus_available(self, user=current_user):
        print(user)
        return any([cus.is_available(user) for cus in self.contest_user_solutions])

    def get_total_score(self):
        total_score = 0
        for cus in self.contest_user_solutions:
            if cus.score is not None:
                total_score += cus.score
        return total_score

    def act_stop(self):
        if self.is_ended():
            pass
        elif self.is_started():
            self.end_date = current_time()
            db.session.commit()
        else:
            self.remove()

    @staticmethod
    def get_all_by_contest_and_user(contest, user):
        if contest is None or user is None or contest.id is None or user.id is None:
            return None
        return ContestToUserRelation.query.filter_by(
            contest_id=contest.id, user_id=user.id
        ).all()

    @staticmethod
    def get_active_by_contest_and_user(contest, user):
        for cu in ContestToUserRelation.get_all_by_contest_and_user(contest, user):
            if cu.is_active():
                return cu
        return None
