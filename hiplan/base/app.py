from hiplan.base.board import Board
from typing import List
import json

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

    @staticmethod
    def deserialize(dictionary):
        app = App.get_instance()
        for board in dictionary['boards']:
            app.add_board(Board.deserialize(board))

        return app
            