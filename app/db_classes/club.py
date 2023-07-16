from app.imports import *
from app.sqlalchemy_custom_types import *


class Club(db.Model):
    # --> INITIALIZE
    __tablename__ = "club"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=True)
    hashed_id = db.Column(db.String, unique=True, nullable=True)

    # --> RELATIONS
    user_clubs = db.relationship("User_Club", backref="club")
    chats = db.relationship("Chat", backref="club")
    club_contests = db.relationship("Club_Contest", backref="club")

    # --> FUNCTIONS
    def is_my(self):
        return self.is_contains_user(current_user)

    def is_contains_user(self, user=current_user):
        return user in [uc.user for uc in self.user_clubs]
    
    def act_set_hashed_id(self):
        while True:
            hashed_id = generate_token(20)
            if not Club.get_by_hashed_id(hashed_id):
                self.hashed_id = hashed_id
                break

        self.hashed_id = hashed_id
        return self.save()
    
    def act_add_user(self, user=current_user, role=Participant):
        from app.dbc import User_Club
        if user is None:
            return
        if self.is_contains_user(user):
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
        if not self.is_contains_user(user):
            return
        uc = User_Club.query.filter_by(user=user, club=self).first()
        uc.remove()
        for chat in self.chats:
            chat.act_remove_user(user)
        return self
    
    def act_add_user_by_invite(self, user=current_user, invite=None):
        if (invite is None) or (invite.is_expired()) or (invite.get_parent() != self):
            return
        if self.is_contains_user(user):
            return
        self.act_add_user(user)
        return self
    
    def act_add_chat(self, name=None):
        from app.dbc import Chat, User_Chat
        if name is None or name.strip()=="":
            return
        chat = Chat(name=name, club=self)
        chat.add()
        for user in [uc.user for uc in self.user_clubs]:
            uc = User_Chat(user=user, chat=chat)
            uc.add()
        return chat
    
    def act_remove_chat(self, chat=None):
        from app.dbc import Chat
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
            return
        cc = Club_Contest(contest=contest, club=self)
        cc.add()
        return self
    
    def act_remove_contest(self, contest=None):
        from app.dbc import Club_Contest
        if contest is None:
            return self
        cc = Club_Contest.query.filter_by(club_id=self.id, contest_id=contest.id).first()
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
        invite = Invite(parent_type=DbParent.fromType(Club), parent_id=self.id)
        invite.add()
        return invite
        

    def add(self):
        db.session.add(self.act_set_hashed_id())
        return self.save()
    
    def remove(self):
        for c in self.chats:
            c.remove()
        for uc in self.user_clubs:
            uc.remove()
        for cc in self.club_contests:
            cc.remove()
        db.session.delete(self)
        db.session.commit()

    def save(self):
        db.session.commit()
        return self
    
    def count_owners(self):
        return len([uc.user for uc in self.user_clubs if uc.role.isOwner()])

    def count_participants(self):
        return len([uc.user for uc in self.user_clubs if uc.role.isParticipant()])
    
    def get_all_invites(self):
        from app.dbc import Invite
        return Invite.get_all_by_parent(self)

    @staticmethod
    def get_by_id(id):
        if id is None:
            return None
        return Club.query.filter_by(id=id).first()
    
    @staticmethod
    def get_by_hashed_id(hashed_id):
        if hashed_id is None:
            return None
        return Club.query.filter_by(hashed_id=hashed_id).first()