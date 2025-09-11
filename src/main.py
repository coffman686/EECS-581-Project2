from enum import Enum

# class syntax

class CellState(Enum):

    NONEADJACENT = 0

    MINE = 1

    HASADJACENT = 2

    MINED = 3

# very basic class, feel free to change anything
class Cell:
    def __init__(self):
        # value >= 0 --> number of mines in a 9x9 are around the cell
        # value = -1 --> uninitialized
        self.state : None | CellState = None
        self.adjacent : int = -1
        self.hidden : bool = True
        self.flagged : bool = False

    def is_valid(self):
        return True if self.adjacent >= 0 else False
    
    def has_mine(self):
        return self.state == CellState.MINED
    
    def is_hidden(self):
        return self.hidden
    
    def get_value(self):
        return self.adjacent
    
    def __str__(self):
        return "X" if self.hidden else "M" if self.state == CellState.MINED else str(self.adjacent)
    
    def __repr__(self):
        return str(self.adjacent)


class GameState:
    game_statuses = ["Starting","Playing","Lose","Win"]
    grid = [[Cell() for i in range(0, 10)] for j in range(0, 10)] # Create a 2D 10x10 array filled with Cell objects

    total_mines = 10
    def __init__(self):
        self.remaining_mine_count = self.total_mines
        self.game_status = self.game_statuses[0]
        self.print_grid()
    
    def print_grid(self):
        for row in self.grid:
            out_row = ""
            for column in row:
                out_row += str(column)
            print(out_row)

if __name__ == "__main__":
    GameState()


