from classes import GameManager, Cell, CellState, GameStatus
from enum import Enum
import random

class Mode(Enum):
    NONE = 0
    EASY = 1
    MEDIUM = 2
    HARD = 3


class AI_mode():
    def __init__(self, game_manager):
        self.mode = Mode(0)
        self.is_turn = False
        self.game_manager = game_manager

    def set_mode_easy(self):
        self.mode = Mode.EASY

    def change_turn(self):
        if self.game_manager.game_status.name == "PLAYING":
            self.is_turn = not self.is_turn
    
    def easy_ai_turn(self):
        valid_moves = []
        for r in range(10):
            for c in range(10):
                cell = self.game_manager.grid[r][c]
                if cell.is_hidden() and not cell.has_flag():
                    valid_moves.append((r, c))

        if len(valid_moves) > 0:
            index = random.randint(0, len(valid_moves) - 1)
            r_rand, c_rand = valid_moves[index]
            self.game_manager.handle_clicked_cell(r_rand, c_rand)
            return (r_rand, c_rand)

        return (0,0)
        



