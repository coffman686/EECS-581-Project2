from enum import Enum
import random

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
    
    def has_flag(self):
        return self.flagged

class GameManager:
    def __init__(self, seed=None):
        """Constructor function for the GamerManager Class"""
        self.screen = Screen()
        self.should_quit = False

        # Save number of rows & cols
        self.rows = 10
        self.cols = 10

        # Save number of mines & mines left
        # Defaults to 10. We need to call set_total_mines to actually update it.
        self.mine_count = 10
        self.remaining_mine_count = 10

        # Generate grid
        self.grid = [[Cell() for i in range(self.cols)] for i in range(self.rows)]

        # Set game state to 'Starting'
        self.game_status = GameStatus.WELCOME
        
        # Generate Seed 
        if seed is not None:
            self.seed = seed
        else:
            self.seed = random.randrange(1 << 30)

        self.generate_mines()

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
        """Prints the grid"""
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

    def handle_clicked_cell(self, i, j):
        """
        Once cell is left clicked, reveal the cell.
            5 possible outcomes
                A cell that has already been revealed is picked
                    Do nothing
                A cell with 1-8 adjacent mines is picked
                    Action: Reveal just this cell
                A cell with a mine is picked
                    Reveal the mine, transition to game loss screen, have all mines be revealed
                A cell with a flag is picked
                    Do nothing, cells with flags must not be allowed to be revealed
                A cell with 0 adjacent mines
                    Use recursive backtracking to continually reveal all adjacent squares with 0 mines

        Order to check:
            Flagged? -> Has mine? -> 0 or Not-0 adjacent mines?
        """
        i_pos = i
        j_pos = j

        clicked_cell = (self.grid[i][j])
        # Uses a "is_hidden" function which is not yet implemented in the cell class.
        hidden_cell = clicked_cell.is_hidden()
        is_flagged = clicked_cell.has_flag()

        # If the cell has a flag on it, ignore.
        if is_flagged == True:
            pass
        
        # If the cell is already revealed, ignore.
        if hidden_cell == False:
            pass

        # Checks if the cell has a mine.
        is_a_mine = clicked_cell.has_mine()

        # If the cell is a mine, reveal the square, transition to end of game.
        if is_a_mine == True:
            # Reveal square / New function to reveal cell?
            self.grid[i][j].hidden = False

            # Add behavior that transitions to end screen / ends game here.

        # Gets the cell state to check if 
        if clicked_cell.adjacent != 0:
            # Reveal the square and its bomb count.
            clicked_cell.hidden = False
            
        if clicked_cell.adjacent == 0:
            rec_reveal(self, i_pos, j_pos)

        return

def rec_reveal(self, i, j):
    # Recursively reveal all the cells around the current cell that have 0 adjacent mines in the 8 nearby directions.
        # Care must be taken to ensure that no out of bounds errors occur.
        # The recursive backtracking with all 8 cells might be slow since certain cells might get processed multiple times.
    
    # Get the cell object from coordinate i,j
    current_cell = self.grid[i][j]

    # If the cell has already been revealed, nothing needs to be done.
    if not current_cell.hidden or current_cell.has_flag():
        return
    
    # Since current cell has not been revealed, reveal it.
    
    current_cell.hidden = False

    # If the cell has an adjacent mine, do not recurse on it. Just return since it has already been revealed.
    if current_cell.adjacent_mines > 0:
        return

    # NOTE: Use similar behavior to updating the mines counts, but instead of adding counts, calls rec_reveal on the adjacent squares, if their adjacent bomb count is also 0.
    
    # Get the row value, col value, # of rows, # of cols.
    row = i
    col = j
    rows = len(self.grid)
    cols = len(self.grid[0])

    # Check the adjacent 8 cells to the current cell to see if they are in bounds, are not revealed.
        # If so, reveals it.
            # Then if that cell also has 0 adjacent mines, recursively reveal it and its neighbors.

    for adj_row in [-1, 0, 1]:
        for adj_col in [-1, 0, 1]:
        # Check to make sure not adjusting the count of where the mine is.
            if (adj_row != 0 or adj_col != 0):
                temp_row = row + adj_row
                temp_col = col + adj_col
                # Check if temp_row and temp_col are in bounds. If so, reveal it
                if ((0 <= temp_row < rows) and (0 <= temp_col < cols)):
                    self.grid[temp_row][temp_col].hidden = False
                    # If the current cell has 0 as its count, call rec_reveal on it.
                    if self.grid[temp_row][temp_col].adjacent_mines == 0:
                        self.rec_reveal(temp_row, temp_col)