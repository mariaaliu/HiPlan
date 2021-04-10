from typing import List
from hiplan.base.app import App 

app = App()
app.add_board()
app.boards[0].add_record()
app.save_to_file()
