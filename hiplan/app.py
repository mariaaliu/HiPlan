from typing import List
import enum
from datetime import datetime
import json
from base.app.py import App
from base.board.py import Board
from base.task.py import Task
from base.member.py import Member
from base.record.py import Record
from base.priority.py import Priority 

app = App()
app.add_board()
app.boards[0].add_record()
app.save_to_file()
