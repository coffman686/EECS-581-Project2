from enum import Enum

class CellState(Enum):
    NONEADJACENT = 0
    MINE = 1
    HASADJACENT = 2
    MINED = 3

class GameStatus(Enum):
    WELCOME = 0
    STARTING = 1
    PLAYING = 2
    LOSE = 3
    WIN = 4
    END = 5

# Think of this like the frontend manager. When the backend needs to change the state
# of the frontend, it will call these methods.
class Screen:
    def set_welcome(self):
        pass

    def set_start(self):
        pass

    def set_playing(self):
        pass

    def set_lose(self):
        pass

    def set_win(self):
        pass

    def set_end(self):
        pass

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

class GameManager:
    def __init__(self):
        self.total_mines = 10 # Should be updated in the start screen
        self.remaining_mine_count = self.total_mines
        self.game_status = GameStatus.WELCOME
        self.grid = [[Cell() for i in range(0, 10)] for j in range(0, 10)] # Create a 2D 10x10 array filled with Cell objects
        self.screen = Screen()
        self.should_quit = False

    def set_total_mines(self, total_mines):
        self.total_mines = total_mines

    def hide_cell(self, r, c):
        self.grid[r][c].hidden = False
    
    def place_flag(self, r, c):
        self.grid[r][c].flagged = True
    
    def remove_flag(self, r, c):
        self.grid[r][c].flagged = False

    def is_flagged(self, r, c):
        return self.grid[r][c].flagged

    # Debug function to print our cell grid
    def print_grid(self):
        for row in self.grid:
            out_row = ""
            for column in row:
                out_row += str(column)
            print(out_row)

    def change_state(self, status):
        match status:
            case GameStatus.WELCOME:
                self.game_status = GameStatus.WELCOME
                self.screen.set_welcome()
            case GameStatus.STARTING:
                self.game_status = GameStatus.STARTING
                self.screen.set_start()
            case GameStatus.PLAYING:
                self.game_status = GameStatus.PLAYING
                self.screen.set_playing()
            case GameStatus.LOSE:
                self.game_status = GameStatus.LOSE
                self.screen.set_lose()
            case GameStatus.WIN:
                self.game_status = GameStatus.WIN
                self.screen.set_win()
            case GameStatus.END:
                self.game_status = GameStatus.END
                self.screen.set_end()
            case _:
                pass
