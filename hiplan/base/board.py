
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
            'records': [record.serialize() for record in self.records]
        }