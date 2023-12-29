from app.imports import *

from app.sqlalchemy_custom_types import *

from app.db_classes.standard_model.normal import StandardModel
from app.db_classes.like.abstract import AbstractLike
from app.db_classes.like.null import NullLike
from app.db_classes.like.getter import LikeGetter


class Like(StandardModel, AbstractLike):
    # --> INITIALIZE
    __abstract__ = False
    __tablename__ = "like"

    parent_type_ = db.Column(DbParentType)
    parent_id_ = db.Column(db.Integer)
    good_ = db.Column(db.Boolean)

    null_cls_ = NullLike
    getter_cls_ = LikeGetter

    # --> RELATIONS
    user_id_ = db.Column(db.Integer, db.ForeignKey("user.id_"))

    # --> PROPERTIES
    @property
    def parent_type(self):
        return self.parent_type_

    @parent_type.setter
    def parent_type(self, value):
        self.parent_type_ = value
        self.save()

    @property
    def parent_id(self):
        return self.parent_id_

    @parent_id.setter
    def parent_id(self, value):
        self.parent_id_ = value
        self.save()

    @property
    def good(self):
        return self.good_

    @good.setter
    def good(self, value):
        self.good_ = value
        self.save()

    @property
    def bad(self):
        return not self.good

    @bad.setter
    def bad(self, value):
        self.good = not value

    @property
    def user_id(self):
        return self.user_id_

    @user_id.setter
    def user_id(self, value):
        self.user_id_ = value
        self.save()

    @property
    def user(self):
        return self.user_

    @user.setter
    def user(self, value):
        self.user_ = value
        self.save()

    # --> METHODS
    def get_parent(self):
        par_type = self.parent_type.to_type()
        if par_type is None:  # TODO : find a way to avoid None checking
            return None
        return par_type.get.by_id(self.parent_id)

    def add(self):
        db.session.add(self)
        self.save()
        par = self.get_parent()
        if not par.is_null():
            if self.good:
                if not par.total_likes:
                    par.total_likes = 0
                par.total_likes += 1
            else:
                if not par.total_dislikes:
                    par.total_dislikes = 0
                par.total_dislikes += 1
        return self.save()

    def remove(self, par=None):
        if par is None:
            par = self.get_parent()
        if par is not None:
            if self.good:
                if not par.total_likes:
                    par.total_likes = 0  # TODO : how this can happen?
                par.total_likes -= 1
            else:
                if not par.total_dislikes:
                    par.total_dislikes = 0
                par.total_dislikes -= 1
            db.session.commit()
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def get_by_parent_and_user(parent, user=current_user):
        if parent is None or user is None:
            return None
        parent_type = DbParent.from_type(type(parent))
        if parent_type is None:
            return None
        return Like.get.by_parent(parent).by_user(user).first()

    @staticmethod
    def get_all_by_parent(parent):
        if parent is None:
            return []
        parent_type = DbParent.from_type(type(parent))
        if parent_type is None:
            return []
        return Like.get.by_parent(parent).all()

    @staticmethod
    def exists(parent, user=current_user):
        return Like.get.by_parent(parent).by_user(user).first().is_not_null()

    @staticmethod
    def act_add_like_to_parent(parent, user=current_user, good=True):
        if parent.is_null() or user.is_null():
            return
        Like.act_remove_like_from_parent(parent, user)
        Like(
            parent_type_=DbParent.from_type(type(parent)),
            parent_id_=parent.id,
            user_id_=user.id,
            good_=good,
        ).add()

    @staticmethod
    def act_remove_like_from_parent(parent, user=current_user):
        if parent is None or user is None:
            return
        if Like.exists(parent, user):
            Like.get.by_parent(parent).by_user(user).first().remove()
