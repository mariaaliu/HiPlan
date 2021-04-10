class Record:
    def __init__(self, name = "Untitled", tasks = None, labels = None, progress_items = None, priority = Priority.NONE):
        self.name = name
        self.tasks: List[Task] = tasks or []
        self.labels: List[Label] = labels or []
        self.progress_items: List[ProgressItem] = progress_items or []
        self.priority: Priority = priority

    def add_tasks(self, task: Task = None):
        if not isinstance(task, Task) and task is not None:
            raise TypeError("{} is not a task".format(task))

        self.tasks.append(task or Task())

    def serialize(self):
        return {
            'name': self.name,
            'tasks': [task.serialize() for task in self.tasks]
        }
