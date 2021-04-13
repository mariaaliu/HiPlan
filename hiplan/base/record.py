from hiplan.base.task import Task
from hiplan.base.priority import Priority
from typing import List
import json

class Record:
    def __init__(self, name = "Untitled", tasks = None, labels = None, progress_items = None, priority = Priority.NONE):
        self.name = name
        self.tasks: List[Task] = tasks or []
        self.labels: List["Label"] = labels or []
        self.progress_items: List["ProgressItem"] = progress_items or []
        self.priority: Priority = priority

    def add_tasks(self, task: Task = None):
        if not isinstance(task, Task) and task is not None:
            raise TypeError("{} is not a task".format(task))

        self.tasks.append(task or Task())

    def serialize(self):
        return {
            'name': self.name,
            'tasks': [task.serialize() for task in self.tasks],
            #'labels': [label.serialize() for label in self.labels],
            #'progress_items': [progress_item.serialize() for progress_item in self.progress_items],
            'priority': self.priority.value
        }

    @staticmethod
    def deserialize(dict):
        record = Record(name=dict['name'], tasks=None, labels=None, progress_items=None, priority=dict['priority'])
        record.task = []
        record.labels = []
        record.progress_items = []

        for task in dict['tasks']:
            record.add_tasks(Task.deserialize(task))

        return record

        # self.name = dict['name']
        # self.tasks = [Task.deserialize(task) for task in dict['tasks']]
        # self.labels = [Label.deserialize(label) for label in dict['labels']]
        # self.progress_items = [Progress_item.deserialize(progress_item) for progress_item in dict['progress_items']]
        # self.priority.value = dict['priority']
