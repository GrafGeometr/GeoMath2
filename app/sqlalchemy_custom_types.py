# -*- coding: utf-8 -*-
from sqlalchemy import TypeDecorator, String


class Role:
    def __init__(self, name):
        self.name = name

    def __eq__(self, object):
        return self.name == object.name
    
    def isOwner(self):
        return self.name == Owner.name
    
    def setOwner(self):
        self.name = Owner.name
    
    def isParticipant(self):
        return self.name == Participant.name
    
    def setParticipant(self):
        self.name = Participant.name
    
    def isInvited(self):
        return self.name == Invited.name
    
    def setInvited(self):
        self.name = Invited.name

Owner = Role("Owner")
Participant = Role("Participant")
Invited = Role("Invited")

class RoleType(TypeDecorator):
    impl = String


    def process_bind_param(self, value, dialect):
        return value.name
    
    def process_result_value(self, value, dialect):
        return Role(value)
    
    
    




