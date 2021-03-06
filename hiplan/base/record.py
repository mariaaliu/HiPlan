from hiplan.base.task import Task
from hiplan.base.priority import Priority
from hiplan.base.progress_item import ProgressItem
from typing import List


class Record:
    def __init__(self, name: str = "Untitled", tasks: Task = None, labels: str = None, progress_items: ProgressItem = None, priority: Priority = Priority.NONE):
        self.name = name
        self.tasks: List[Task] = tasks or []
        self.labels: List[str] = labels or []
        self.progress_items: List[ProgressItem] = progress_items or []
        self.priority: Priority = priority

    def add_tasks(self, task: Task = None):
        if not isinstance(task, Task) and task is not None:
            raise TypeError("{} is not a task".format(task))

        self.tasks.append(task or Task())

    def serialize(self):
        return {
            'name': self.name,
            'tasks': [task.serialize() for task in self.tasks],
            # 'labels': [label.serialize() for label in self.labels],
            'progress_items': [progress_item.serialize() for progress_item in self.progress_items],
            'priority': self.priority.value
        }

    @staticmethod
    def deserialize(dictionary):
        record = Record(name=dictionary['name'], tasks=None, labels=None, progress_items=None, priority=Priority(dictionary['priority']))

        for task in dictionary['tasks']:
            record.add_tasks(Task.deserialize(task))

        return record

        # self.name = dict['name']
        # self.tasks = [Task.deserialize(task) for task in dict['tasks']]
        # self.labels = [Label.deserialize(label) for label in dict['labels']]
        # self.progress_items = [Progress_item.deserialize(progress_item) for progress_item in dict['progress_items']]
        # self.priority.value = dict['priority']
