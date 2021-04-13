from hiplan.base.member import Member
from typing import List
from datetime import datetime
import json

class Task:
    def __init__(self, title = "No title", description = '', deadline = datetime.now(), members = None, goals = None, labels = None):
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
            'deadline': self.deadline.strftime("%d/%m/%Y, %H:%M:%S") or None,
            # 'members': [member.serialize() for member in self.members]
            # 'goals': [goal.serialize() for goal in self.goals],
            # 'labels': [label.serialize() for label in self.labels]
        }

    @staticmethod
    def deserialize(dict):
        task = Task(title=dict['title'], description=dict['description'], deadline=dict['deadline'], members=None, goals=None, labels=None)
        task.members = []
        task.goals = []
        task.labels = []
        
        return task


        self.title = dict['title']
        self.description = dict['description']
        self.deadline = dict['deadline']
        # self.members = [Member.deserialize(member) for member in dict['members']]
        # self.goals = [Goal.deserialize(goal) for goal in dict['goals']]
        # self.labels = [Label.deserialize(label) for label in dict['labels']]

