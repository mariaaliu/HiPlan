from typing import List
import enum
from datetime import datetime
import json

class Priority(enum.Enum):
    NONE = 0
    LOWEST = 1
    LOW = 2
    MEDIUM = 3
    HIGH = 4
    HIGHEST = 5
    CRITICAL = 6

class Member:
    pass

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
            'title': self.title

        }

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

class App:
    __instance = None
    def __init__(self):
        if App.__instance is not None:
            raise Exception("App was alredy instantiated")

        App.__instance = self
        
        self.boards: List[Board] = []

    @staticmethod
    def get_instance():
        if App.__instance is None:
            App()
    
        return App.__instance

    def add_board(self, board: Board = None):
        if not isinstance(board, Board) and board is not None:
            raise TypeError("{} is not a board".format(board))
        
        self.boards.append(board or Board())

    def serialize(self):
        return {
            'boards': [board.serialize() for board in self.boards]
        }

    def save_to_file(self, file_name:str = "App.json"):
        with open(file_name, "w") as f:
            f.write(json.dumps(self.serialize()))















app = App()
app.add_board()
app.boards[0].add_record()
app.save_to_file()
