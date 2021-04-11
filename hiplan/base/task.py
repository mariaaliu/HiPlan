from hiplan.base.member import Member
from typing import List
from datetime import datetime
import json

class Task:
    def __init__(self, title = "No title", description = '', deadline = None, members = None, goals = None, labels = None):
        self.title = title
        self.description = description
        self.deadline: datetime = deadline
        self.members: List[Member] = members or []
        self.goals: List["Goal"] = goals or []
        self.labels: List["Label"] = labels or []

    def serialize(self):
        return {
            'title': self.title,
            'description': self.description,
            'deadline': self.deadline.strftime("%m/%d/%Y, %H:%M:%S"),
            #'members': [member.serialize() for member in self.members]
            #'goals': [goal.serialize() for goal in self.goals],
            #'labels': [label.serialize() for label in self.labels]
        }

    # @staticmethod
    # def deserialize()

