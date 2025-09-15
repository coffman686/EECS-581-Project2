from enum import Enum
import random

class CellState(Enum):
    NONEADJACENT = 0
    MINE = 1
    HASADJACENT = 2
    MINED = 3

class GameStatus(Enum):
    STARTING = 0
    PLAYING = 1
    LOSE = 2
    WIN = 3
    END = 4

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
    def __init__(self, rows, cols, mine_count, seed=None):
        """Constructor function for the GamerManager Class"""

        # Save number of rows & cols
        self.rows = rows
        self.cols = cols

        # Save number of mines & mines left
        self.mine_count = mine_count
        self.remaining_mine_count = mine_count

        # Generate grid
        self.grid = [[Cell() for i in range(cols)] for i in range(rows)]

        # Set game state to 'Starting'
        self.game_status = GameStatus.STARTING
        
        # Generate Seed 
        if seed is not None:
            self.seed = seed
        else:
            self.seed = random.randrange(1 << 30)

        self.generate_mines()

    def print_grid(self):
        """Prints the grid"""
        for row in self.grid:
            out_row = ""
            for column in row:
                out_row += str(column)
            print(out_row)

    def generate_mines(self):
        """Randomly places mines on the grid"""

        rows = len(self.grid)
        cols = len(self.grid[0])

        # Use a seeded RNG if a seed was provided, otherwise use system randomness
        seed_num = random.Random(self.seed)

        # Select unique mine positions across the grid
        mine_positions = seed_num.sample(range(rows * cols), self.mine_count)

        for pos in mine_positions:
            # Convert 1D position -> (row, col)
            row = pos // cols
            col = pos % cols

            # Place a mine
            self.grid[row][col].state = CellState.MINED

            # Update all neighbors to increase their adjacent count
            for adj_row in [-1, 0, 1]:
                for adj_col in [-1, 0, 1]:
                    # Skip the mine itself
                    if adj_row == 0 and adj_col == 0:
                        continue

                    temp_row = row + adj_row
                    temp_col = col + adj_col

                    # Only update if neighbor is inside grid bounds
                    if 0 <= temp_row < rows and 0 <= temp_col < cols:
                        self.grid[temp_row][temp_col].adjacent += 1




            