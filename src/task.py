from member import Member
from progress_status import ProgressStatus
from goal import Goal
from typing import List
from datetime import datetime


class Task:

    def __init__(self, title: str = "No title", description: str = '', deadline: datetime = None, members: Member = None, goals: Goal = None, labels: str = None, progress_status: ProgressStatus = ProgressStatus.UNSOLVED):
        self.title = title
        self.description = description
        self.deadline: datetime = deadline
        self.members: List[Member] = members or []
        self.goals: List[Goal] = goals or []
        self.labels: List[str] = labels or []
        self.progress_status = progress_status

    def serialize(self):
        return {
            'title': self.title,
            'description': self.description,
            'deadline': self.deadline.strftime("%d/%m/%Y, %H:%M") if self.deadline else None
            # 'members': [member.serialize() for member in self.members]
            # 'goals': [goal.serialize() for goal in self.goals],
            # 'labels': [label.serialize() for label in self.labels]
        }

    @staticmethod
    def deserialize(dictionary: dict):
        task = Task(title=dictionary['title'], description=dictionary['description'], members=None, goals=None, labels=None)
        if dictionary['deadline']: 
            task.deadline = datetime.strptime(dictionary['deadline'], "%d/%m/%Y, %H:%M")

        return task
