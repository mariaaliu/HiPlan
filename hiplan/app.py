from typing import List
import enum
from datetime import datetime
import json

app = App()
app.add_board()
app.boards[0].add_record()
app.save_to_file()
