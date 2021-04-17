import enum
from hiplan.base.task import Task

class Member:
    def __init__(self, name, email):
        self.name = name
        self.email = email

    def solve_task(self, task: Task):
        if not isinstance(task, Task):
            raise Exception("{} is not a task".format(task))

        if task.progress_status is ProgressStatus.SOLVED:
            raise Exception("The task was already solved")
        else:
            task.progress_status = ProgressStatus.SOLVED
    
    def serialize(self):
        return {
            'name': self.name,
            'email': self.email
        }

    @staticmethod
    def deserialize(dictionary: dict):
        member = Member(name=dictionary['name'], email=dictionary['email'])

        return member
