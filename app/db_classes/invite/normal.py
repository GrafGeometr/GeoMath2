from app.imports import *

from app.sqlalchemy_custom_types import *

from app.db_classes.standard_model.normal import StandardModel
from app.db_classes.invite.abstract import AbstractInvite
from app.db_classes.invite.null import NullInvite
from app.db_classes.invite.getter import InviteGetter


class Invite(StandardModel, AbstractInvite):
    # --> INITIALIZE
    __abstract__ = False
    __tablename__ = "invite"

    code_ = db.Column(db.String, unique=True, nullable=True)
    expired_at_ = db.Column(db.DateTime)
    parent_type_ = db.Column(DbParentType)
    # parent_type = db.Column(db.String)  # 'Pool', 'Club'
    parent_id_ = db.Column(db.Integer)

    null_cls_ = NullInvite
    getter_cls_ = InviteGetter

    # --> RELATIONS

    # --> PROPERTIES
    @property
    def code(self):
        return self.code_

    @code.setter
    def code(self, code):
        self.code_ = code
        self.save()

    @property
    def expired_at(self):
        return self.expired_at_

    @expired_at.setter
    def expired_at(self, expired_at):
        self.expired_at_ = expired_at
        self.save()

    @property
    def parent_type(self):
        return self.parent_type_

    @parent_type.setter
    def parent_type(self, parent_type):
        self.parent_type_ = parent_type
        self.save()

    @property
    def parent_id(self):
        return self.parent_id_

    @parent_id.setter
    def parent_id(self, parent_id):
        self.parent_id_ = parent_id
        self.save()

    # --> METHODS
    def add(self):
        db.session.add(self)
        db.session.commit()
        self.code = self.generate_code()
        self.act_set_expired_at()
        return self

    @staticmethod
    def generate_code():
        while True:
            code = generate_token(10)
            if Invite.get.by_code(code).first().is_null():
                return code

    def is_expired(self):
        return self.expired_at <= current_time()

    def act_check_expired(self):
        if self.is_expired():
            self.remove()

    def act_set_expired_at(self):
        timedelta = datetime.timedelta(hours=24)
        self.expired_at = current_time() + timedelta
        db.session.commit()
        return self

    @staticmethod
    def act_refresh_all():
        for inv in Invite.get.all():
            inv.act_check_expired()

    def get_parent(self):
        par_type = self.parent_type.to_type()
        if par_type is None:  #  TODO : avoid None checking
            return None
        return par_type.get.by_id(self.parent_id).first()

    def is_from_parent(self, obj):
        return (
            self.parent_type == DbParent.from_type(type(obj))
            and self.parent_id == obj.id
        )
