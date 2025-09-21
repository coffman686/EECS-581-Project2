"""
File Name: classes.py
Function: Create the classes and functions necessary to run the backend / game logic
Inputs: None
Outputs: None
Authors:
    Blake Carlson
    Logan Smith
    Jack Bauer
    Delroy Wright
    Nifemi Lawal
Creation Date: 9/14/2025

NOTE: All code in the file was authored by 1 or more of the authors. No outside sources were used for code
"""

# Import enum and random
from enum import Enum
import enum
import random

# Create a CellState class which is used to represent the current state of the cell
    # Determines some of the behavior that Cells can have occur

"""
The CellStates are:
    NONADJACENT: The Cell has no adjacent Cells that have a mine
    MINE: Designates that a mine should be placed here when mines are being generated
    HASADJACENT: The Cell as at least 1 adjacent Cells with a mine
    MINED: The Cell has a mine placed on it
"""
class CellState(Enum):
    NONEADJACENT = 0
    HASADJACENT = 2
    MINED = 3

# Create a GameStatus class which keeps track of what the current status of the game is
    # This is used to take certain actions, such as knowing to reveal the board when the player loses

"""
Each represents a different status the game can be in and determines what is allowed to happen in the game
    The statuses are:
        WELCOME: program starts
        PLAYING: user is playing game, after the first move is made
        LOSE: reveal a mine and loses
        WIN: reveals all non-mine squares and wins
        END: user decides to not play again
"""
class GameStatus(Enum):
    WELCOME = 0
    PLAYING = 2
    LOSE = 3
    WIN = 4
    END = 5

# Creates a Cell class. Each individual square on the board is a Cell.
    # Each Cell object has its own attributes which keep track of various characteristics about the cell.
class Cell:
    def __init__(self, gameManager, col, row):
        # value >= 0 --> number of mines in a 9x9 are around the cell
        self.state : None | CellState = None
        # Number of mines in adjacent cells
        self.adjacent : int = 0
        # Bool whether the cell is "hidden" or not yet visible to the player
        self.hidden : bool = True
        # Bool for whether the player currently has a flag on the cell
        self.flagged : bool = False
        # The row and column indices of the Cell. Its position on the board
        self.row = row
        self.col = col
        # The game manager object that manages the Cell
        self.manager = gameManager

    # Function returning whether the Cell has been "initialized" when the game begins
    def is_valid(self):
        return True if self.adjacent >= 0 else False
    
    # Function returning a bool corresponding to whether or not the Cell contains a mine
    def has_mine(self):
        return self.state == CellState.MINED
    
    # Function returning a bool if the Cell is still hidden from the user
    def is_hidden(self):
        return self.hidden
    
    # Function returning the number of mines in squares adjacent to the current cell
    def get_value(self):
        return self.adjacent
    
    # Overloads how a Cell is represented as a string
    def __str__(self):
        return "X" if self.hidden else "M" if self.state == CellState.MINED else str(self.adjacent)
    
    # Overloads the text representation of a Cell
    def __repr__(self):
        return str(self.adjacent)
    
    # Function returning a bool corresponding to if the cell currently has a flag on it
    def has_flag(self):
        return self.flagged

    # Function that counts how many of the Cells adjacent to the current cell have mines
    """
    def count_adjacent_cells(self):
        # Goes through all (up to) 8 adjcaent cells and counts how many of them have mines
        left_cell = self.manager.grid[(self.row)][(self.col - 1) % self.manager.cols]
        right_cell = self.manager.grid[(self.row)][(self.col + 1) % self.manager.cols]

        top_cell = self.manager.grid[(self.row - 1) % self.manager.rows][(self.col)]
        bottom_cell = self.manager.grid[(self.row + 1) % self.manager.rows][(self.col)]

        top_left_cell = self.manager.grid[(self.row - 1) % self.manager.rows][(self.col - 1) % self.manager.cols]
        top_right_cell = self.manager.grid[(self.row + 1) % self.manager.rows][(self.col - 1) % self.manager.cols]

        bottom_right_cell = self.manager.grid[(self.row + 1) % self.manager.rows][(self.col + 1) % self.manager.cols]
        bottom_left_cell = self.manager.grid[(self.row - 1) % self.manager.rows][(self.col + 1) % self.manager.cols]

        cells = [left_cell, right_cell, top_cell, bottom_cell, top_left_cell, top_right_cell, bottom_right_cell, bottom_left_cell]
    
        #self.adjacent = 0

        # If the Cell has at least one adjacent mine, update its CellState to it having adjacent mines
        if self.adjacent > 0:
            self.state = CellState.HASADJACENT
    """
    
# Class for a GameManager object which keeps track of what is and has happened in the game
class GameManager:
    def __init__(self, seed=None):
        """Constructor function for the GamerManager Class"""
        self.is_first_click = True

        self.should_quit = False

        # Save number of rows & cols on the board
        self.rows = 10
        self.cols = 10

        # Save number of mines & mines left
        # Defaults to 10. We need to call set_total_mines to actually update it.
        self.total_mines = 10
        self.remaining_mine_count = self.total_mines

        # Set default values for the number of placed flags, total flags, and remaining flags
        self.placed_flags = 0
        self.total_flags = 0
        self.remaining_flag_count = 0
        
        # Generate grid of Cell objects to create the game board
        self.grid = [[Cell(self, col,row) for col in range(self.cols)] for row in range(self.rows)]

        # Set game state to 'WELCOME'
        self.game_status = GameStatus.WELCOME
        
        # Generate Seed 
        if seed is not None:
            self.seed = seed
        else:
            self.seed = random.randrange(1 << 30)

        #self.count_adjacent_cells()

    """
    def count_adjacent_cells(self):
        for row in self.grid:
            for cell in row:
                cell.count_adjacent_cells()
    """

    # Sets the number of mines equal to the number the user gives
    def set_total_mines(self, total_mines):
        self.total_mines = total_mines
        self.remaining_mine_count = total_mines

    # Function which places a flag on a square that has yet to be revealed
    def place_flag(self, r, c):
        # Checks if the user still has flags to place and if the Cell is already flagged
            # If either is true, do not place a flag
        if self.remaining_flag_count <= 0 or self.grid[r][c].flagged:
            return

        # Change the state of the Cell to represent it being flagged and update the counts of flags placed and flags remaining
        self.grid[r][c].flagged = True
        self.placed_flags += 1
        self.remaining_flag_count -= 1

    # Function handling flag removal. Only works if the current Cell is already flagged
    def remove_flag(self, r, c):
        if not self.grid[r][c].flagged:
            return

        # Update the flagged status of the Cell and flag counts accordingly
        self.grid[r][c].flagged = False
        self.placed_flags -= 1
        self.remaining_flag_count += 1

    # Function used to reveal a Cell when it is left clicked
    def reveal_cell(self, r, c):
        # Sets the Cells status to no longer be hidden and call the remove flag function
        self.grid[r][c].hidden = False
        self.remove_flag(r,c)

    # Function which returns a bool for if a Cell at a certain position if flagged or not
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

    # Function used to change status of the game in the GameManager
    def change_state(self, status):
        match status:
            case GameStatus.WELCOME:
                self.game_status = GameStatus.WELCOME
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

    # Function which randomly generates the mine locations and places them on the grid        
    def generate_mines(self, i, j):
        """Randomly places mines on the grid"""

        # Retrieves the number of rows and columns on the game board
        rows = len(self.grid)
        cols = len(self.grid[0])

        # Use a seeded RNG if a seed was provided, otherwise use system randomness
        seed_num = random.Random(self.seed)

        # Select unique mine positions across the grid
        mine_positions = seed_num.sample(range(rows * cols), self.total_mines)

        while(sum(1 for pos in mine_positions if pos // cols == i and pos % cols == j) >= 1): # ensure we don't create mines on first click position
            mine_positions = seed_num.sample(range(rows * cols), self.total_mines)

        # Goes through all the positions where mines should be places and places a mine
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

                    # Uses a temporary row and column index to check if the cells neighbor is on the board
                        # Ex: A cell in row 0 might have a "neighbor" in row -1 which is not actually a square and must be prevented from being indexed
                    temp_row = row + adj_row
                    temp_col = col + adj_col

                    # Only update if neighbor is inside grid bounds
                    if 0 <= temp_row < rows and 0 <= temp_col < cols:
                        # Also do not update adjacent count if the cell has a mine.
                        if self.grid[temp_row][temp_col].has_mine() == False:
                            self.grid[temp_row][temp_col].adjacent += 1

    # Function which is called when the user makes their first valid left click. This places the mines and ensures mines are only generated once
    def handle_first_click(self, i, j):
            self.is_first_click = False
            self.generate_mines(i, j)

    # Main function which handles the logic of when a user left clicks on a cell and tries to reveal it
    def handle_clicked_cell(self, i, j):
        """
        Once cell is left clicked, take the appropreate action based on the current state of the cell.
            5 possible outcomes / actions
                1: A cell that has a flag on it.
                    Do nothing
                2: A cell that is already revealed is selected.
                    Do nothing
                3: A cell with a mine is picked
                    Reveal the mine, transition to game loss screen with the board fully revealed
                4: A cell with 1-8 adjacent mines is picked
                    Action: Reveal just this cell
                5: A cell with 0 adjacent mines
                    Use recursive backtracking to continually reveal all adjacent squares with 0 mines

        Order to check:
            Flagged? -> Already revealed? -> Has mine? -> Not 0 adj Mines? -> At least 1 adj mines?
        """

        # Retrieve the cell that was clicked from the grid.
        clicked_cell = (self.grid[i][j])

        # Determine whether the cell clicked on is still hidden and if it is flagged or not.
        hidden_cell = clicked_cell.is_hidden()
        is_flagged = clicked_cell.has_flag()

        # If the cell has a flag on it, ignore.
        if is_flagged == True:
            return
        
        # If this is the first left click that takes an action, change the game state to playing and take the actions for the first click (set mines, etc.)
        if(self.is_first_click == True):
            self.change_state(GameStatus.PLAYING)
            self.handle_first_click(i, j)
        
        # If the cell is already revealed, ignore.
        if hidden_cell == False:
            return

        # Checks if the cell has a mine.
        is_a_mine = clicked_cell.has_mine()

        # If the cell is a mine, reveal all the cells, change GameStatus to LOSE.
        if is_a_mine == True:
            self.reveal_all()
            self.change_state(GameStatus.LOSE)
            return

        # Reveal the cell if it has at least one adjacent mine.
        if clicked_cell.adjacent > 0:
            # Reveal the square and its bomb count.
            self.reveal_cell(i, j)
        # If it has no adjacent mines, recursively reveal other adjacent squares with 0 adjacent mines.
        else:
            self.rec_reveal(i, j)

        # After the appropreate action has been taken, check if the user has won the game.
            # If so, change status to win showing the whole board
            # If not, continue the game as normal
        if self.check_win():
            self.reveal_all()
            self.change_state(GameStatus.WIN)
            return

        return
    
    # Checks if the player has won the game
        # If every cell without a mine has been revealed they have won, otherwise they have not.
    def check_win(self):
        for row in self.grid:
            for cell in row:
                if cell.is_hidden() and not cell.has_mine():
                    return False
        return True

    def rec_reveal(self, i, j):
        # Recursively reveal all the cells around the current cell that have 0 adjacent mines in the 8 nearby directions
            # Must ensure that no out of bounds errors occur
        
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

        # This uses similar behavior to updating the mines counts, but instead of adding counts, calls rec_reveal on the adjacent squares, if their adjacent bomb count is also 0
        
        # Get the row value, col value, # of rows, # of cols
        row = i
        col = j
        rows = len(self.grid)
        cols = len(self.grid[0])

        # Check the adjacent 8 cells to the current cell to see if they are in bounds, are not revealed
            # If so, reveals it
                # Then if that cell also has 0 adjacent mines, recursively reveal it and its neighbors

        for adj_row in [-1, 0, 1]:
            for adj_col in [-1, 0, 1]:
            # Check to make sure not adjusting the count of where the mine is
                if (adj_row != 0 or adj_col != 0):
                    temp_row = row + adj_row
                    temp_col = col + adj_col
                    # Check if temp_row and temp_col are in bounds. If so, recursively reveal
                    if ((0 <= temp_row < rows) and (0 <= temp_col < cols)):
                        self.rec_reveal(temp_row, temp_col)
        return

    # Reveal all the cells on the grid. Gets called when a mine is pressed
    def reveal_all(self):
        for row in range(self.rows):
            for col in range(self.cols):
                self.reveal_cell(row, col)
        return