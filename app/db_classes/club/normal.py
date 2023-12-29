from app.imports import *
from app.sqlalchemy_custom_types import *

from app.db_classes.standard_model.normal import StandardModel
from .abstract import AbstractClub
from .null import NullClub
from .getter import ClubGetter


class Club(StandardModel):
    # --> INITIALIZE
    __abstract__ = False
    __tablename__ = "club"

    null_cls_ = NullClub
    getter_cls_ = ClubGetter

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
    
    @chats.setter
    def chats(self, chats: list["Chat"]):
        self.chats_ = chats
        self.save()

    @property
    def club_contests(self) -> list["Club_Contest"]:
        return self.club_contests_
    
    @club_contests.setter
    def club_contests(self, club_contests: list["Club_Contest"]):
        self.club_contests_ = club_contests
        self.save()



    # --> FUNCTIONS
    def contains_user(self, user=current_user) -> bool:
        return user in [uc.user for uc in self.user_clubs]

    def add_user(self, user=current_user, role=Participant):
        from app.dbc import UserToClubRelation
        if self.contains_user(user):
            return
        uc = UserToClubRelation(user=user, club=self, role=role)
        uc.add()
        for chat in self.chats:
            chat.add_user(user)
        return self

    def remove_user(self, user=current_user):
        from app.dbc import UserToClubRelation
        if not self.contains_user(user):
            return
        uc = UserToClubRelation.get.by_user(user).by_club(self).first()
        uc.remove()
        for chat in self.chats:
            chat.remove_user(user)
        return self

    def add_user_by_invite(self, user=current_user, invite=None):
        if (invite is None) or (invite.is_expired()) or (invite.get_parent() != self):
            return
        if self.contains_user(user):
            return
        self.add_user(user)
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
        Chat.get.by_id(id).first().remove()

    def act_add_contest(self, contest_id=None):
        from app.dbc import Contest, ClubToContestRelation

        if contest_id is None:
            return
        try:
            contest_id = int(contest_id)
        except:
            return
        contest = Contest.get.by_id(contest_id).first()
        if contest is None:
            return
        if not contest.is_archived():
            if (not current_user.get_pool_relation(contest.pool_id).is_owner()) or (
                    not current_user.get_club_relation(self.id).is_owner()
            ):
                return
        ClubToContestRelation(contest=contest, club=self).add()
        return self

    def act_remove_contest(self, contest=None):
        from app.dbc import ClubToContestRelation

        if contest is None:
            return self
        ClubToContestRelation.get.by_club(self).by_contest(contest).remove()
        return self

    def act_remove_contest_by_id(self, contest_id=None):
        from app.dbc import Contest

        if contest_id is None:
            return self
        contest = Contest.get.by_id(id).first()
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
