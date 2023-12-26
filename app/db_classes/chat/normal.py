from app.imports import *
from sqlalchemy_custom_types import *

from app.db_classes.standard_model.normal import StandardModel
from .abstract import AbstractChat
from .null import NullChat
from .getter import ChatGetter

class Chat(AbstractChat, StandardModel):
    # --> INITIALIZE
    __abstract__ = False
    __tablename__ = "chat"

    readonly_ = db.Column(db.Boolean, default=False)

    null_cls_ = NullChat
    getter_cls_ = ChatGetter

    # --> RELATIONS
    user_chats_ = db.relationship("User_Chat", backref="chat_")
    club_id_ = db.Column(db.Integer, db.ForeignKey("club.id_"))

    # --> PROPERTIES
    @property
    def readonly(self) -> bool:
        return self.readonly_

    @readonly.setter
    def readonly(self, readonly: bool):
        self.readonly_ = readonly
        self.save()

    @property
    def user_chats(self) -> list["User_Chat"]:
        return self.user_chats_

    @user_chats.setter
    def user_chats(self, user_chats: list["User_Chat"]):
        self.user_chats_ = user_chats
        self.save()

    @property
    def club_id(self, club_id: int):
        return self.club_id_

    @club_id.setter
    def club_id(self, club_id: int):
        self.club_id_ = club_id
        self.save()


    # --> FUNCTIONS
    def remove(self):
        from app.dbc import Invite

        for i in Invite.get.by_parent(self).all():
            i.remove()
        for uc in self.user_chats:
            uc.remove()
        db.session.delete(self)
        db.session.commit()

    def contains_user(self, user=current_user) -> bool:
        return user in [uc.user for uc in self.user_chats]

    def all_messages(self):
        res = []
        for uc in self.user_chats:
            res.extend(uc.messages)
        return sorted(res, key=lambda m: m.date)

    def unread_messages(self, user=current_user) -> list["Message"]:
        res = []
        for m in self.all_messages():
            if m.unread_by_user(user):
                res.append(m)
        return res

    def last_message_date(self) -> datetime.datetime:
        messages = self.all_messages()
        if len(messages) == 0:
            return datetime.datetime.min
        return max([m.date for m in messages])

    def other_user(self, user=current_user):
        if self.club_id is not None:
            return None

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

    def add_user(self, user=current_user):
        from app.dbc import UserToChatRelation

        if self.contains_user(user):
            return
        uc = UserToChatRelation(user=user, chat=self)
        uc.add()
        return self

    def remove_user(self, user=current_user):
        from app.dbc import UserToChatRelation
        uc = UserToChatRelation.get.by_user(user).by_chat(self).first()
        uc.remove()
        return self

    def act_refresh_chat_invites(self):
        for ci in self.chat_invites:
            ci.act_check_expired()

    def act_generate_new_invite_code(self):
        self.act_refresh_chat_invites()
        from app.dbc import Invite

        ci = Invite(parent_type=DbParent.from_type(Chat), parent_id=self.id)
        ci.add()

    def act_mark_all_as_read(self, user=current_user):
        for um in self.unread_messages(user):
            um.act_mark_as_read()
        return
