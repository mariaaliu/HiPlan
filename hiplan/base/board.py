from hiplan.base.member import Member
from hiplan.base.record import Record
from typing import List
import json

class Board:
    def __init__(self, name = "Untitled", records = None, description = "", members = None):
        self.name = name
        self.records: List[Record] = records or []
        self.description = description
        self.members: List[Member] = members or []

    def add_record(self, record: Record = None):
        if not isinstance(record, Record) and record is not None:
            raise TypeError("{} is not a record".format(record))
        
        self.records.append(record or Record())

    def add_members(self, member: Member = None):
        if not isinstance(member, Member) and member is not None:
            raise TypeError("{} is not a member".format(member))
        
        self.members.append(member or Member())

    def serialize(self):
        return {
            'name': self.name,
            'records': [record.serialize() for record in self.records],
            'description': self.description
            #'members': [member.serialize() for member in self.members]
        }

    @staticmethod
    def deserialize(dict):
        board = Board(name=dict['name'], records=None, description=dict['description'], members=None)
        board.records = []
        board.members = []

        for record in dict['records']:
            board.add_record(Record.deserialize(record))
        
        # for member in dict['members']:
        #     board.add_members(Member.deserialize(member))

        return board
        # self.records = [Record.deserialize(record) for record in dict['records']]
        # self.members = [Member.deserialize(member) for member in dict['members']]
