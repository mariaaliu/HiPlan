from hiplan.base.member import Member
from typing import List
from datetime import datetime
import json

class Task:
    def __init__(self, title = "No title", description = '', deadline = None, members = None, goals = None, labels = None):
        self.title = title
        self.description = description
        self.deadline: datetime = deadline or datetime.now()
        self.members: List[Member] = members or []
        self.goals: List["Goal"] = goals or []
        self.labels: List["Label"] = labels or []

    def serialize(self):
        return {
            'title': self.title,
            'description': self.description,
            'deadline': self.deadline.strftime("%d/%m/%Y, %H:%M:%S") if self.deadline else None
            # 'members': [member.serialize() for member in self.members]
            # 'goals': [goal.serialize() for goal in self.goals],
            # 'labels': [label.serialize() for label in self.labels]
        }

    @staticmethod
    def deserialize(dictionary):
        task = Task(title=dictionary['title'], description=dictionary['description'], deadline=dictionary['deadline'], members=None, goals=None, labels=None)
        
        return task


        # self.title = dict['title']
        # self.description = dict['description']
        # self.deadline = dict['deadline']
        # self.members = [Member.deserialize(member) for member in dict['members']]
        # self.goals = [Goal.deserialize(goal) for goal in dict['goals']]
        # self.labels = [Label.deserialize(label) for label in dict['labels']]

