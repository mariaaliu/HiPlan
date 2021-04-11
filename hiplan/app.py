from typing import List
from hiplan.base.app import App 

app = App()
app.add_board()
app.boards[0].add_record()
app.boards[0].records[0].add_tasks()
app.save_to_file()
