from hiplan.base.member import Member
from hiplan.base.progress_status import ProgressStatus
from hiplan.base.goal import Goal
from typing import List
from datetime import datetime
import json
import enum

class Task:

    def __init__(self, title: str = "No title", description: str = '', deadline: datetime = None, members: Member = None, goals: Goal = None, labels: str = None, progress_status: ProgressStatus = ProgressStatus.UNSOLVED):
        self.title = title
        self.description = description
        self.deadline: datetime = deadline or datetime.now()
        self.members: List[Member] = members or []
        self.goals: List[Goal] = goals or []
        self.labels: List[str] = labels or []
        self.progress_status = progress_status

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
    def deserialize(dictionary: dict):
        task = Task(title=dictionary['title'], description=dictionary['description'], deadline=dictionary['deadline'], members=None, goals=None, labels=None)
        
        return task


        # self.title = dict['title']
        # self.description = dict['description']
        # self.deadline = dict['deadline']
        # self.members = [Member.deserialize(member) for member in dict['members']]
        # self.goals = [Goal.deserialize(goal) for goal in dict['goals']]
        # self.labels = [Label.deserialize(label) for label in dict['labels']]

