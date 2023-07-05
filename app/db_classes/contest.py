from app.imports import *
from app.sqlalchemy_custom_types import *

class Contest(db.Model):
    __tablename__ = "contest"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String)
    description = db.Column(db.String)
    start_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)
    is_public = db.Column(db.Boolean, default=False)
    contest_problems = db.relationship("Contest_Problem", backref="contest")
    contest_judges = db.relationship("Contest_Judge", backref="contest")

    pool_id = db.Column(db.Integer, db.ForeignKey("pool.id"))

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

    def is_archived(self):
        return self.is_public

    def is_description_available(self):
        return self.is_public or self.is_my()

    def is_my(self):
        relation = current_user.get_pool_relation(self.pool_id)
        if relation is None:
            return False
        if relation.role.isOwner() or relation.role.isParticipant():
            return True
        return False

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

    def get_active_cu(self):
        from app.dbc import Contest_User
        for cu in Contest_User.query.filter_by(
            user_id=current_user.id, contest_id=self.id
        ).all():
            if not cu.is_ended():
                return cu
        return None

    def is_started(self):
        return self.start_date <= current_time()

    def is_ended(self):
        return self.end_date <= current_time()

    def register(self, virtual=False, virtual_start=None, virtual_end=None):
        from app.dbc import Contest_User, Contest_User_Solution
        if not self.is_public:
            return
        cu = self.get_active_cu()
        if cu:
            return
        if not virtual:
            if not self.is_started():
                cu = Contest_User(
                    contest_id=self.id,
                    user_id=current_user.id,
                    start_date=self.start_date,
                    end_date=self.end_date,
                    virtual=False,
                )
            elif not self.is_ended():
                cu = Contest_User(
                    contest_id=self.id,
                    user_id=current_user.id,
                    start_date=current_time(),
                    end_date=self.end_date,
                    virtual=False,
                )
            else:
                return
            db.session.add(cu)
            db.session.commit()
            for p in self.get_problems():
                cus = Contest_User_Solution(contest_user_id=cu.id, problem_id=p.id)
                cus.set_hashed_id()
                db.session.add(cus)
            db.session.commit()
            return
        else:
            if (
                (virtual_start is None)
                or (virtual_end is None)
                or (virtual_start > virtual_end)
            ):
                return
            cu = Contest_User(
                contest_id=self.id,
                user_id=current_user.id,
                start_date=virtual_start,
                end_date=virtual_end,
                virtual=True,
            )
            db.session.add(cu)
            db.session.commit()
            for p in self.get_problems():
                cus = Contest_User_Solution(contest_user_id=cu.id, problem_id=p.id)
                cus.set_hashed_id()
                db.session.add(cus)
            db.session.commit()
            return

    def stop(self):
        if not self.is_public:
            return
        cu = self.get_active_cu()
        if not cu:
            return
        cu.end_manually()
        db.session.commit()
        return