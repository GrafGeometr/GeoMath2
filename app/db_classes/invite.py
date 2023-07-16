from app.imports import *
from app.sqlalchemy_custom_types import *


class Invite(db.Model):
    # --> INITIALIZE
    __tablename__ = "invite"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    code = db.Column(db.String, unique=True, nullable=True)
    expired_at = db.Column(db.DateTime)
    parent_type = db.Column(DbParentType)
    # parent_type = db.Column(db.String)  # 'Pool', 'Club'
    parent_id = db.Column(db.Integer)

    # --> RELATIONS

    # --> FUNCTIONS
    def add(self):
        db.session.add(self)
        db.session.commit()
        self.act_set_code()
        self.act_set_expired_at()
        return self
    
    def remove(self):
        db.session.delete(self)
        db.session.commit()
    
    def is_expired(self):
        return self.expired_at <= current_time()

    def act_check_expired(self):
        if self.is_expired():
            self.remove()

    def act_set_code(self):
        while True:
            code = generate_token(10)
            if not Invite.query.filter_by(code=code).first():
                self.code = code
                break
        db.session.commit()

    def act_set_expired_at(self):
        timedelta = datetime.timedelta(hours=24)
        self.expired_at = current_time() + timedelta
        db.session.commit()
        return self
    
    @staticmethod
    def get_by_id(id):
        if id is None:
            return None
        return Invite.query.filter_by(id=id).first()
    


    @staticmethod
    def get_all_by_parent(parent):
        from app.dbc import Problem, Sheet, Contest_User_Solution, Pool, Club
        par_class = DbParent.fromType(type(parent))
        if par_class is None:
            return None
        return Invite.query.filter_by(parent_type=par_class, parent_id=parent.id).all()
    
    @staticmethod
    def act_refresh_all():
        for inv in Invite.query.all():
            inv.act_check_expired()


    def get_parent(self):
        par_type = self.parent_type.toType()

        if par_type is None:
            return None
        return par_type.get_by_id(self.parent_id)

    def is_from_parent(self, obj):
        return self.parent_type == DbParent.fromType(type(obj)) and self.parent_id == obj.id