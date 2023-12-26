from app.imports import *

from app.db_classes.standard_model.normal import StandardModel
from .abstract import AbstractClub
from .null import NullClub
from .getter import Getter


class Club(StandardModel):
    # --> INITIALIZE
    __abstract__ = False
    __tablename__ = "club"

    null_cls_ = NullClub
    getter_cls_ = Getter

    # --> RELATIONS
    user_clubs_ = db.relationship("User_Club", backref="club_")
    chats_ = db.relationship("Chat", backref="club_")
    club_contests_ = db.relationship("Club_Contest", backref="club_")

    # --> PROPERTIES
    @property
    def user_clubs(self) -> list["User_Club"]:
        return self.user_clubs_
    
    @user_clubs.setter
    def user_clubs(self, user_clubs: list["User_Club"]):
        self.user_clubs_ = user_clubs
        self.save()

    @property
    def chats(self) -> list["Chat"]:
        return self.chats_

    @property
    def club_contests(self) -> list["Club_Contest"]:
        return self.club_contests_



    # --> FUNCTIONS
    def is_my(self):
        return self.contains_user(current_user)

    def contains_user(self, user=current_user):
        return user in [uc.user for uc in self.user_clubs]

    def act_add_user(self, user=current_user, role=Participant):
        from app.dbc import User_Club

        if user is None:
            return
        if self.contains_user(user):
            return
        uc = User_Club(user=user, club=self, role=role)
        uc.add()
        print(self.chats)
        for chat in self.chats:
            print(chat, "trying to add", user.name)
            chat.act_add_user(user)
        return self

    def act_remove_user(self, user=current_user):
        from app.dbc import User_Club

        if user is None:
            return
        if not self.contains_user(user):
            return
        uc = User_Club.query.filter_by(user=user, club=self).first()
        uc.remove()
        for chat in self.chats:
            chat.act_remove_user(user)
        return self

    def act_add_user_by_invite(self, user=current_user, invite=None):
        if (invite is None) or (invite.is_expired()) or (invite.get_parent() != self):
            return
        if self.contains_user(user):
            return
        self.act_add_user(user)
        return self

    def act_add_chat(self, name=None):
        from app.dbc import Chat, User_Chat

        if name is None or name.strip() == "":
            return
        chat = Chat(name=name, club=self)
        chat.add()
        for user in [uc.user for uc in self.user_clubs]:
            uc = User_Chat(user=user, chat=chat)
            uc.add()
        return chat

    def act_remove_chat(self, chat=None):

        if (chat is None) or (chat not in self.chats):
            return self
        chat.remove()
        return self

    def act_remove_chat_by_id(self, chat_id=None):
        from app.dbc import Chat

        if chat_id is None:
            return self
        chat = Chat.query.filter_by(id=chat_id).first()
        self.act_remove_chat(chat)
        return self

    def act_add_contest(self, contest_id=None):
        from app.dbc import Contest, Club_Contest

        if contest_id is None:
            return
        try:
            contest_id = int(contest_id)
        except:
            return
        contest = Contest.query.filter_by(id=contest_id).first()
        if contest is None:
            return
        if not contest.is_archived():
            if (not current_user.get_pool_relation(contest.pool_id).is_owner()) or (
                    not current_user.get_club_relation(self.id).is_owner()
            ):
                return
        cc = Club_Contest(contest=contest, club=self)
        cc.add()
        return self

    def act_remove_contest(self, contest=None):
        from app.dbc import Club_Contest

        if contest is None:
            return self
        cc = Club_Contest.query.filter_by(
            club_id=self.id, contest_id=contest.id
        ).first()
        if cc is None:
            return self
        cc.remove()
        return self

    def act_remove_contest_by_id(self, contest_id=None):
        from app.dbc import Contest

        if contest_id is None:
            return self
        contest = Contest.query.filter_by(id=contest_id).first()
        self.act_remove_contest(contest)

    def act_generate_new_invite_code(self):
        from app.dbc import Invite

        Invite.act_refresh_all()
        invite = Invite(parent_type=DbParent.from_type(Club), parent_id=self.id)
        invite.add()
        return invite

    def remove(self):
        for c in self.chats:
            c.remove()
        for uc in self.user_clubs:
            uc.remove()
        for cc in self.club_contests:
            cc.remove()
        db.session.delete(self)
        db.session.commit()

    def count_owners(self):
        return len([uc.user for uc in self.user_clubs if uc.role.is_owner()])

    def count_participants(self):
        return len([uc.user for uc in self.user_clubs if uc.role.is_participant()])

    def get_all_invites(self):
        from app.dbc import Invite

        return Invite.get_all_by_parent(self)
