from app.imports import *

from app.db_classes.standard_model.normal import StandardModel


class ContestToJudgeRelation(StandardModel):
    # --> INITIALIZE
    __tablename__ = "contest_judge"

    # --> RELATIONS
    contest_id = db.Column(db.Integer, db.ForeignKey("contest.id_"))
    user_id = db.Column(db.Integer, db.ForeignKey("user.id_"))

    # --> FUNCTIONS
    @staticmethod
    def get_by_contest_and_user(contest, user):
        if contest is None or user is None or contest.id is None or user.id is None:
            return None
        return ContestToJudgeRelation.query.filter_by(
            contest_id=contest.id, user_id=user.id
        ).first()
