from app.imports import *
from app.sqlalchemy_custom_types import *

from app.db_classes.standart_database_classes import *


class Like(db.Model, StandartModel):
    # --> INITIALIZE
    __tablename__ = "like"

    parent_type = db.Column(DbParentType)
    parent_id = db.Column(db.Integer)
    good = db.Column(db.Boolean)

    # --> RELATIONS
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    # --> FUNCTIONS
    def get_parent(self):
        par_type = self.parent_type.toType()
        if par_type is None:
            return None
        return par_type.get_by_id(self.parent_id)

    def add(self):
        db.session.add(self)
        self.save()
        par = self.get_parent()
        if par is not None:
            if self.good:
                if not par.total_likes:
                    par.total_likes = 0
                par.total_likes += 1
            else:
                if not par.total_dislikes:
                    par.total_dislikes = 0
                par.total_dislikes += 1
            db.session.commit()
        return self

    def remove(self, par=None):
        if par is None:
            par = self.get_parent()
        if par is not None:
            if self.good:
                if not par.total_likes:
                    par.total_likes = 0
                par.total_likes -= 1
            else:
                if not par.total_dislikes:
                    par.total_dislikes = 0
                par.total_dislikes -= 1
            db.session.commit()
        db.session.delete(self)
        self.save()

    @staticmethod
    def get_by_parent_and_user(parent, user=current_user):
        if parent is None or user is None:
            return None
        parent_type = DbParent.fromType(type(parent))
        if parent_type is None:
            return None
        return Like.query.filter_by(
            parent_type=parent_type, parent_id=parent.id, user_id=user.id
        ).first()

    @staticmethod
    def get_all_by_parent(parent):
        if parent is None:
            return []
        parent_type = DbParent.fromType(type(parent))
        if parent_type is None:
            return []
        return Like.query.filter_by(parent_type=parent_type, parent_id=parent.id).all()

    @staticmethod
    def is_has_like(parent, user=current_user):
        return Like.get_by_parent_and_user(parent, user) is not None

    @staticmethod
    def act_add_like_to_parent(parent, user=current_user, good=True):
        if parent is None or user is None:
            return
        Like.act_remove_like_from_parent(parent, user)
        Like(
            parent_type=DbParent.fromType(type(parent)),
            parent_id=parent.id,
            user_id=user.id,
            good=good,
        ).add()

    @staticmethod
    def act_remove_like_from_parent(parent, user=current_user):
        if parent is None or user is None:
            return
        if Like.is_has_like(parent, user):
            like = Like.get_by_parent_and_user(parent, user)
            like.remove()
