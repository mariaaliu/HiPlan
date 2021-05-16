from member import Member
from record import Record
from typing import List, Tuple
from enum import Enum


class Background:
    class BackgroundType(Enum):
        IMAGE = 0
        COLOR = 1

    def __init__(self, color: Tuple[float, float, float]=None, image: str=None):
        self.color = color
        self.image = image
        if self.color:
            self.type = Background.BackgroundType.COLOR
        elif self.image:
            self.type = Background.BackgroundType.IMAGE
        else:
            raise Exception("No image or background color mentioned")
        
    def serialize(self):
        return{
            'color': self.color,
            'image': self.image,
        }

    @staticmethod
    def deserialize(dictionary):
        return Background(color=dictionary['color'], image=dictionary['image'])


class Board:
    def __init__(self, name="Untitled", records=None, description="", members=None, background=None):
        self.name = name
        self.records: List[Record] = records or []
        self.description = description
        self.members: List[Member] = members or []
        self.background = background or Background((0, 0, 1))

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
            'description': self.description,
            'background': self.background.serialize(),
            # 'members': [member.serialize() for member in self.members],
        }

    @staticmethod
    def deserialize(dictionary):
        board = Board(
            name=dictionary['name'], 
            records=None, 
            description=dictionary['description'], 
            members=None, 
            background=Background.deserialize(dictionary['background'])
        )

        for record in dictionary['records']:
            board.add_record(Record.deserialize(record))

        return board
