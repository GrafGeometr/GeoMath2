from app.imports import *
from app.sqlalchemy_custom_types import *


class Chat(db.Model):
    # --> INITIALIZE
    __tablename__ = "chat"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    hashed_id = db.Column(db.String, unique=True, nullable=True)
    readonly = db.Column(db.Boolean, default=False)

    # --> RELATIONS
    user_chats = db.relationship("User_Chat", backref="chat")
    club_id = db.Column(db.Integer, db.ForeignKey("club.id"))  # if not a dialog

    # --> FUNCTIONS
    def add(self):
        db.session.add(self)
        db.session.commit()
        self.act_set_hashed_id()
        return self

    def remove(self):
        from app.dbc import Invite

        for i in Invite.get_all_by_parent(self):
            i.remove()
        for uc in self.user_chats:
            uc.remove()
        db.session.delete(self)
        db.session.commit()

    def is_contains_user(self, user=current_user):
        return user in [uc.user for uc in self.user_chats]

    def is_my(self, user=current_user):
        from app.dbc import User_Chat

        uc = User_Chat.query.filter_by(user_id=user.id, chat_id=self.id).first()
        return uc is not None

    def get_all_messages(self):
        res = []
        for uc in self.user_chats:
            res.extend(uc.messages)
        return sorted(res, key=lambda m: m.date)

    def get_unread_messages(self, user=current_user):
        from app.dbc import User_Message

        res = []
        for m in self.get_all_messages():
            res.extend(
                User_Message.query.filter_by(user=user, message=m, read=False).all()
            )
        return res

    def get_last_message_date(self):
        messages = self.get_all_messages()
        if len(messages) == 0:
            return datetime.datetime.min
        return max([m.date for m in messages])

    def get_other_user(self, user=current_user):
        if self.club_id is not None:
            return None
        from app.dbc import User_Chat

        users = [uc.user for uc in self.user_chats]
        if user not in users:
            return None
        if len(users) <= 1:
            return None
        if user == users[0]:
            return users[1]
        return users[0]

    def count_owners(self):
        return len([uc.user for uc in self.user_chats if uc.is_owner()])

    def count_participants(self):
        return len([uc.user for uc in self.user_chats if uc.is_participant()])

    def act_set_hashed_id(self):
        while True:
            hashed_id = generate_token(20)
            if not Chat.query.filter_by(hashed_id=hashed_id).first():
                self.hashed_id = hashed_id
                break
        db.session.commit()

    def act_add_user(self, user=current_user):
        from app.dbc import User_Chat

        if self.is_contains_user(user):
            return
        uc = User_Chat(user=user, chat=self)
        uc.add()
        return self

    def act_remove_user(self, user=current_user):
        from app.dbc import User_Chat

        if not self.is_contains_user(user):
            return
        uc = User_Chat.query.filter_by(user=user, chat=self).first()
        uc.remove()
        return self

    def act_refresh_chat_invites(self):
        for ci in self.chat_invites:
            ci.act_check_expired()

    def act_generate_new_invite_code(self):
        self.act_refresh_chat_invites()
        from app.dbc import Chat_Invite

        ci = Chat_Invite(chat=self)
        ci.add()

    def act_mark_all_as_read(self, user=current_user):
        for um in self.get_unread_messages(user):
            um.act_mark_as_read()
        return
