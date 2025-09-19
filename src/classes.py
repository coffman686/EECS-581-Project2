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

class Cell:
    def __init__(self, gameManager, col, row):
        # value >= 0 --> number of mines in a 9x9 are around the cell
        # value = -1 --> uninitialized
        self.state : None | CellState = None
        self.adjacent : int = -1
        self.hidden : bool = True
        self.flagged : bool = False
        self.row = row
        self.col = col
        self.manager = gameManager
        self.row = row
        self.col = col
        self.manager = gameManager

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

    def count_adjacent_cells(self):
        left_cell = self.manager.grid[(self.row)][(self.col - 1) % self.manager.cols]
        right_cell = self.manager.grid[(self.row)][(self.col + 1) % self.manager.cols]

        top_cell = self.manager.grid[(self.row - 1) % self.manager.rows][(self.col)]
        bottom_cell = self.manager.grid[(self.row + 1) % self.manager.rows][(self.col)]

        top_left_cell = self.manager.grid[(self.row - 1) % self.manager.rows][(self.col - 1) % self.manager.cols]
        top_right_cell = self.manager.grid[(self.row + 1) % self.manager.rows][(self.col - 1) % self.manager.cols]

        bottom_right_cell = self.manager.grid[(self.row + 1) % self.manager.rows][(self.col + 1) % self.manager.cols]
        bottom_left_cell = self.manager.grid[(self.row - 1) % self.manager.rows][(self.col + 1) % self.manager.cols]

        cells = [left_cell, right_cell, top_cell, bottom_cell, top_left_cell, top_right_cell, bottom_right_cell, bottom_left_cell]
    
        self.adjacent = sum(1 for cell in cells if cell.state == CellState.MINE)
        if self.adjacent > 0:
            self.state = CellState.HASADJACENT
    
    def has_flag(self):
        return self.flagged

    def count_adjacent_cells(self):
        left_cell = self.manager.grid[(self.row)][(self.col - 1) % self.manager.cols]
        right_cell = self.manager.grid[(self.row)][(self.col + 1) % self.manager.cols]

        top_cell = self.manager.grid[(self.row - 1) % self.manager.rows][(self.col)]
        bottom_cell = self.manager.grid[(self.row + 1) % self.manager.rows][(self.col)]

        top_left_cell = self.manager.grid[(self.row - 1) % self.manager.rows][(self.col - 1) % self.manager.cols]
        top_right_cell = self.manager.grid[(self.row + 1) % self.manager.rows][(self.col - 1) % self.manager.cols]

        bottom_right_cell = self.manager.grid[(self.row + 1) % self.manager.rows][(self.col + 1) % self.manager.cols]
        bottom_left_cell = self.manager.grid[(self.row - 1) % self.manager.rows][(self.col + 1) % self.manager.cols]

        cells = [left_cell, right_cell, top_cell, bottom_cell, top_left_cell, top_right_cell, bottom_right_cell, bottom_left_cell]
    
        self.adjacent = sum(1 for cell in cells if cell.state == CellState.MINE)
        if self.adjacent > 0:
            self.state = CellState.HASADJACENT

class GameManager:
    def __init__(self, seed=None):
        """Constructor function for the GamerManager Class"""
        self.is_first_click = True

        self.should_quit = False

        # Save number of rows & cols
        self.rows = 10
        self.cols = 10

        # Save number of mines & mines left
        # Defaults to 10. We need to call set_total_mines to actually update it.
        self.total_mines = 10
        self.remaining_mine_count = self.total_mines

        self.placed_flags = 0
        self.total_flags = 0
        self.remaining_flag_count = 0
        
        # Generate grid
        self.grid = [[Cell(self, col,row) for col in range(self.cols)] for row in range(self.rows)]

        # Set game state to 'Starting'
        self.game_status = GameStatus.WELCOME
        
        # Generate Seed 
        if seed is not None:
            self.seed = seed
        else:
            self.seed = random.randrange(1 << 30)

        self.count_adjacent_cells()

    def count_adjacent_cells(self):
        for row in self.grid:
            for cell in row:
                cell.count_adjacent_cells()

    def set_total_mines(self, total_mines):
        self.total_mines = total_mines
        self.remaining_mine_count = total_mines

    def reveal_cell(self, r, c):
        self.grid[r][c].hidden = False
    
    def place_flag(self, r, c):
        if self.remaining_flag_count <= 0 or self.grid[r][c].flagged:
            return

        self.grid[r][c].flagged = True
        self.placed_flags += 1
        self.remaining_flag_count -= 1

    def remove_flag(self, r, c):
        if not self.grid[r][c].flagged:
            return

        self.grid[r][c].flagged = False
        self.placed_flags -= 1
        self.remaining_flag_count += 1

    def is_flagged(self, r, c):
        return self.grid[r][c].flagged

    # Debug function to print our cell grid

    def reveal_cell(self, r, c):
        self.grid[r][c].hidden = False
    
    def place_flag(self, r, c):
        if self.remaining_flag_count <= 0 or self.grid[r][c].flagged:
            return

        self.grid[r][c].flagged = True
        self.placed_flags += 1
        self.remaining_flag_count -= 1

    def remove_flag(self, r, c):
        if not self.grid[r][c].flagged:
            return

        self.grid[r][c].flagged = False
        self.placed_flags -= 1
        self.remaining_flag_count += 1

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
            case GameStatus.STARTING:
                self.game_status = GameStatus.STARTING
            case GameStatus.PLAYING:
                self.game_status = GameStatus.PLAYING
            case GameStatus.LOSE:
                self.game_status = GameStatus.LOSE
            case GameStatus.WIN:
                self.game_status = GameStatus.WIN
            case GameStatus.END:
                self.game_status = GameStatus.END
            case _:
                pass
            
    def generate_mines(self, i, j):
        """Randomly places mines on the grid"""

        rows = len(self.grid)
        cols = len(self.grid[0])

        # Use a seeded RNG if a seed was provided, otherwise use system randomness
        seed_num = random.Random(self.seed)

        # Select unique mine positions across the grid
        mine_positions = seed_num.sample(range(rows * cols), self.total_mines)

        while(sum(1 for pos in mine_positions if pos // cols == i and pos % cols == j) >= 1): # ensure we don't create mines on first click position
            mine_positions = seed_num.sample(range(rows * cols), self.total_mines)


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
                        # Also do not update adjacent count if the cell has a mine.
                        if self.grid[temp_row][temp_col].has_mine() == False:
                            # If cell state is -1, add 2 so it becomes 1, otherwise just add 1.
                            if self.grid[temp_row][temp_col].adjacent == -1:
                                self.grid[temp_row][temp_col].adjacent += 2
                            else:
                                self.grid[temp_row][temp_col].adjacent += 1

    def handle_first_click(self, i, j):
            self.is_first_click = False
            self.generate_mines(i, j)


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
        if(self.is_first_click == True):
            self.handle_first_click(i, j)
        clicked_cell = (self.grid[i][j])
        # Uses a "is_hidden" function which is not yet implemented in the cell class.
        hidden_cell = clicked_cell.is_hidden()
        is_flagged = clicked_cell.has_flag()

        # If the cell has a flag on it, ignore.
        if is_flagged == True:
            return
        
        # If the cell is already revealed, ignore.
        if hidden_cell == False:
            return

        # Checks if the cell has a mine.
        is_a_mine = clicked_cell.has_mine()

        # If the cell is a mine, reveal all the squares, change GameStatus to LOSE.
        if is_a_mine == True:
            self.reveal_all()
            self.change_state(GameStatus.LOSE)
            return
            # Add behavior that transitions to end screen / ends game here.

        # Reveal the cell if it has at least one adjacent mine.
        if clicked_cell.adjacent > 0:
            # Reveal the square and its bomb count.
            self.reveal_cell(i, j)
        # If it has no adjacent mines, recursively reveal other adjacent squares with 0 adjacent mines.
        else:
            self.rec_reveal(i, j)

        # Check if the user has won the game.
        if self.check_win():
            self.change_state(GameStatus.WIN)
            return

        return
    
    def check_win(self):
        for row in self.grid:
            for cell in row:
                if cell.is_hidden() and not cell.has_mine():
                    return False
        return True

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
        
        self.reveal_cell(i, j)

        # If the cell has an adjacent mine, do not recurse on it. Just return since it has already been revealed.
        if current_cell.adjacent > 0:
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
                    # Check if temp_row and temp_col are in bounds. If so, recursively reveal.
                    if ((0 <= temp_row < rows) and (0 <= temp_col < cols)):
                        self.rec_reveal(temp_row, temp_col)
        return

    # Reveal all the cells on the grid. Gets called when a mine is pressed.
    def reveal_all(self):
        for row in range(self.rows):
            for col in range(self.cols):
                self.reveal_cell(row, col)
        return