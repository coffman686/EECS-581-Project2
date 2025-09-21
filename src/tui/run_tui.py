"""
File: run_tui.py
Function: Provides the terminal-based (curses) text user interface (TUI) for the Minesweeper game.
Inputs:
    - User keystrokes (arrow keys = move, space = reveal, f/F = flag, Enter = next/reveal, q = quit)
    - User mouse clicks (left = reveal, right = flag)
Outputs:
    - Updates the screen (board, flags, messages)
    - Updates to GameManager state
Authors: 
    Blake Carlson
    Logan Smith
    Jack Bauer
    Delroy Wright
    Nifemi Lawal
Date: 9/14/2025
NOTE: All code in the file was authored by 1 or more of the authors. No outside sources were used for code
"""

# Imports:
import curses
from curses.textpad import Textbox, rectangle
import platform
from src.classes import GameManager, Cell, CellState, GameStatus

# Global variables:
ROWS, COLS = 10, 10     # 10 rows & columns to create 10x10 board
CELL_W, CELL_H = 3, 1   # 3 chars per cell, 1 row high

class Frontend():
    """
    Frontend Class:
        Manages the terminal based UI using the curses library
        Interfaces between player input and the GameManager backend    
    """
    def __init__(self, stdscr):
        """Constructor function for the Frontend class"""
        self.stdscr = stdscr
        self.game_manager = GameManager()
        self.cur_r = 0
        self.cur_c = 0
        self.alphabet = "abcdefghijklmnopqrstuvwxyz"

    def draw_game_status(self):
        """Display the current game status"""
        
        # Get terminal dimensions
        sh, sw = self.stdscr.getmaxyx()

        # Display the game status above game board
        self.stdscr.addstr(3, sw // 2 - 10,
            f"Game State: {str(self.game_manager.game_status)[11:]}"
        )

    def set_num_mines(self):
        """Prompt the player to enter the number of mines for this game"""

        # Clear the screen
        self.stdscr.erase()
        sh, sw = self.stdscr.getmaxyx()

        # Keep checking until terminal size is large enough
        while not self.correct_terminal_size(sh, sw):
            self.display_size_warning()         # Show terminal size warning
            sh, sw = self.stdscr.getmaxyx()     # Get updated terminal height and width
            self.stdscr.refresh()               # Redraw screen so warning is visible
            curses.napms(100)                   # pause briefly
            self.stdscr.erase()                 # clear and retry

        # Show prompt message at top
        self.stdscr.addstr(0, 0, "Enter the number of mines for this game: (Press Enter to send)")

        # Create an input box window (5 rows tall, 30 cols wide)
        editwin = curses.newwin(5, 30, 2, 1)

        # Draw a rectangle around the input box
        rectangle(self.stdscr, 1, 0, 1 + 5 + 1, 1 + 30 + 1)
        self.stdscr.refresh()

        # Initialize a Textbox object inside the input window
        box = Textbox(editwin)

        # Remap Enter to submit instead of Ctrl-G
        def enter_terminate(ch):
            if ch == 10:
                return 7
            return ch

        # Wait for user input with the remapped Enter behavior
        box.edit(enter_terminate)

        # Get resulting contents
        num_mines = box.gather().strip()
       
       # Try converting mine count input to integer
        try:
            num_mines = int(num_mines)

            # Check valid range [10-20]
            if num_mines < 10 or num_mines > 20:
                raise ValueError("Invalid number of mines.")
            
            # Update game settings in backend
            self.game_manager.set_total_mines(num_mines)
            self.game_manager.total_flags = num_mines
            self.game_manager.remaining_flag_count = num_mines

        # If the value entered cannot be converted, display error
        except ValueError:
            self.stdscr.addstr(8, 0, "Error: Please enter a valid number between 1 and {}.".format(ROWS * COLS - 1))
            self.stdscr.refresh()
            curses.napms(1500)

            # Restart input prompt
            self.set_num_mines()

    def center_offsets(self, scr_h, scr_w, rows, cols, cw, ch):
        """Calculate vertical and horizontal offsets to center the board on screen"""

        # Total width and height required for the board
        board_w = cols * cw
        board_h = rows * ch

        # Center the board vertically
        off_y = max((scr_h - board_h) // 2, 0)

        # Center the board horizontally
        off_x = max((scr_w - board_w) // 2, 0)

        # Return the offsets used for board drawing
        return off_y, off_x

    def correct_terminal_size(self, scr_h, sch_w, required_h = (ROWS + 1) * CELL_H + 9, required_w = (COLS + 1) * CELL_W):
        """Return whether the terminal window is large enough to display the game"""
        if scr_h < required_h or sch_w < required_w:
            return False
        return True

    def display_size_warning(self):
        """Display a warning message when the terminal window is too small"""

        # Clear the screen before drawing
        self.stdscr.erase()

        # Create warning message
        warning = "Terminal too small! Please resize window."
        
        # Put warning text on screen
        self.stdscr.addstr(0, 0, warning)

        # Redraw the screen
        self.stdscr.refresh()

    def find_start_key(self):
        """Determine the correct label for the Enter/Return key based on OS"""

        # Get the OS of the player
        os_name = platform.system()

        # If the OS is Darwin, use "Return"
        if os_name == "Darwin": 
            return "Return"
        # Otherwise, use enter
        return "Enter"

    def draw_start_screen(self): 
        """Draw the initial start screen for Minesweeper"""

        # Clear the screen before drawing
        self.stdscr.erase()

        # Get current terminal height
        sh, sw = self.stdscr.getmaxyx()

        # Find the key label for "Enter" (depends on OS)
        start_key = self.find_start_key()

        # Draw the current game status (WELCOME)
        self.draw_game_status()

        # If the terminal is too small, show warning and fail
        if not self.correct_terminal_size(sh, sw):
            self.display_size_warning()
            return False

        # Calculate vertical offset for centering
        off_y, _ = self.center_offsets(sh, sw, ROWS, COLS, CELL_W, CELL_H)

        # Text for title, prompt, and controls
        title = "MINESWEEPER"
        prompt = f"Press {start_key} to start with {self.game_manager.total_mines} mines"
        controls = "Arrows=move  Space=Reveal  f=Flag  Mouse: Left=Reveal Right=Flag  q=Quit"

        # Calculate starting locations on x-axis (padding)
        title_scr_x = max((sw - len(title)) // 2, 0)
        prompt_scr_x = max((sw - len(prompt)) // 2, 0)
        controls_scr_x = max((sw - len(controls)) // 2, 0)

        # Display centered text
        self.stdscr.addstr(off_y, title_scr_x, title)
        self.stdscr.addstr(off_y + 2, prompt_scr_x, prompt)
        self.stdscr.addstr(off_y + 4, controls_scr_x, controls)

        # Refresh to show everything drawn
        self.stdscr.refresh()
        
        return True
    
    def start_game(self):
        """Display the start screen and wait for the player to begin or quit"""
        
        while True:
            if not self.draw_start_screen(): # Try to draw the start screen
                ch = self.get_input()
                if ch == curses.KEY_RESIZE:  # If screen draw fails, wait for input
                    continue  # on resize, try again
                continue      # otherwise keep looping
            
            # If the start screen is successfully drawn, wait for input
            ch = self.get_input()

            # If Enter or Return is pressed → start game (exit loop)
            if ch in (ord('\n'), ord('\r')):
                break

            # If 'q' is pressed → quit game and return immediately
            elif ch == ord('q'):
                self.game_manager.should_quit = True
                return
            
             # If terminal is resized → redraw start screen
            elif ch == curses.KEY_RESIZE:
                continue

            # For any other input, just loop again
            continue

        # Draw initial board
        self.draw_board()

        # Main game loop
        while True:
            ch = self.get_input()
            success = self.process_input(ch)
            self.draw_board()
            if self.game_manager.should_quit or not success:
                break      

    def draw_board(self):
        """Draw the game board on the screen"""

        # Clear the screen for fresh drawing
        self.stdscr.erase()
        sh, sw = self.stdscr.getmaxyx()
        self.draw_game_status()

        # Handle incorrect terminal size
        if not self.correct_terminal_size(sh, sw):
            self.display_size_warning()
            return

        # Calculate offsets for centering board
        off_y, off_x = self.center_offsets(sh, sw, ROWS, COLS, CELL_W, CELL_H)

        # Draw column letters
        for c in range(COLS):
            x = off_x + c * CELL_W
            self.stdscr.addstr(off_y - 1, x + 1, f"{self.alphabet[c]}")

        # Draw row numbers
        for r in range(ROWS):
            y = off_y + r * CELL_H
            self.stdscr.addstr(y, off_x - 2, f"{r+1}")

        # Draw the cells of the board
        for r in range(ROWS):
            for c in range(COLS):
                # Get cell and render output depending on cell status
                cell = self.game_manager.grid[r % ROWS][c % COLS]

                # Calculate screen coordinates for this cell
                y = off_y + r * CELL_H
                x = off_x + c * CELL_W

                # Handle per-cell display
                if cell.flagged:
                    ch = "⚑"
                elif cell.hidden:
                    ch = "H"
                elif cell.state == CellState.MINED:
                    ch = "M"
                elif cell.adjacent != 0:
                    ch = str(cell.adjacent)
                elif cell.state == CellState.NONEADJACENT:
                    ch = " "
                elif cell.state is None:
                    ch = " "

                # Highlight cursor (mostly for keyboard input)
                if (self.cur_r, self.cur_c) == (r, c):
                    self.stdscr.attron(curses.A_REVERSE)   # turn on reverse video
                    self.stdscr.addstr(y, x, f"[{ch}]")    # draw highlighted cell
                    self.stdscr.attroff(curses.A_REVERSE)  # turn highlight back off
                else:
                    self.stdscr.addstr(y, x, f"[{ch}]")    # draw normal cell

        # Show remaining mines counter
        self.stdscr.addstr(sh - 1, 0,
            f"Remaining Mines: {self.game_manager.remaining_mine_count}"
        )
        # Show remaining flags counter
        self.stdscr.addstr(sh - 2, 0,
            f"Remaining Flags: {self.game_manager.remaining_flag_count}"
        )
         # Show control instructions
        self.stdscr.addstr(sh - 4, 0,
            "Arrows=move  Space=Reveal  f=Flag  Mouse: Left=Reveal Right=Flag  q=Quit  ",
        )
        self.stdscr.clrtoeol()  # Clear the rest of the line to keep output clean
        self.stdscr.refresh()   # Refresh the screen to apply all drawing operations

        # AFTER drawing the board, check if game over
        result = self.check_game_status()

        if result == 'quit':
            self.game_manager.should_quit = True
            return False # Exit game
        
        elif result == 'play_again':
            self.reset_game()
            return True # Restart game loop

    def mouse_to_cell(self, mx, my):
        """Processes player any-click on cell"""

        # Get the screen height/width
        sh, sw = self.stdscr.getmaxyx()

        # Calculate offsets to determine where the board is centered
        off_y, off_x = self.center_offsets(sh, sw, ROWS, COLS, CELL_W, CELL_H)

        # Check if the mouse position is above/left of the board 
        if my < off_y or mx < off_x:
            return None
        
        # Check if the mouse position is below/right of the board
        if my >= off_y + ROWS * CELL_H or mx >= off_x + COLS * CELL_W:
            return None
        
        # Convert screen coordinates to cell indices
        r = (my - off_y) // CELL_H
        c = (mx - off_x) // CELL_W

        # Return the cell indices if they are valid
        if 0 <= r < ROWS and 0 <= c < COLS:
            return (r, c)
        
        return None

    def handle_left_click(self, r, c):
        """Handle a left-click on the game board"""
        self.game_manager.handle_clicked_cell(r, c)

    def handle_right_click(self, r, c):
        """Handle a right-click action on the game board"""

        # If the cell has a flag, right click can only remove it
        if self.game_manager.is_flagged(r, c):
            self.game_manager.remove_flag(r, c)

        # If the cell does not have a flag, right click will place a flag on that cell.
        else:
            self.game_manager.place_flag(r, c)
        
        return None

    def get_input(self):
        """Capture player keyboard input / mouse event"""
        return self.stdscr.getch()
    
    def check_game_status(self):
        """Change screens on player win/loss"""

        # If the game is in the "WIN" state, display the win screen
        if self.game_manager.game_status == GameStatus.WIN: 
            return self.display_win_screen()
        
        # If the game is in the "LOSE" state, display the loss screen
        elif self.game_manager.game_status == GameStatus.LOSE:
            return self.display_loss_screen()
        
        return None
    
    def process_input(self, ch):
        """Handle player input from keyboard or mouse"""

        # Quit the game if 'q' is pressed
        if ch == ord('q'):
            self.game_manager.should_quit = True
            return False

        # Redraw board if the terminal window is resized
        if ch == curses.KEY_RESIZE:
            self.draw_board()
            return True

        # Handle mouse input
        if ch == curses.KEY_MOUSE:
            # Get mouse event info (x,y coords + button state)
            try:
                _, mx, my, _, bstate = curses.getmouse() 
           
           # Ignore errors if no mouse event captured
            except curses.error:
                return True 

            # Convert mouse position to board coordinates
            pos = self.mouse_to_cell(mx, my)
            if not pos:
                return True

            # Update cursor position to clicked cell
            r, c = pos
            self.cur_r, self.cur_c = r, c

            # Left-click (terminals vary: check CLICKED/PRESSED)
            if bstate & curses.BUTTON1_CLICKED or bstate & curses.BUTTON1_PRESSED:
                self.handle_left_click(r, c)

            # Right-click
            elif bstate & curses.BUTTON3_CLICKED or bstate & curses.BUTTON3_PRESSED:
                self.handle_right_click(r, c)

            return True

        # Keyboard navigation
        if ch in (curses.KEY_UP, ord('k')): self.cur_r = (self.cur_r - 1) % ROWS            # Up or 'k'
        elif ch in (curses.KEY_DOWN, ord('j')): self.cur_r = (self.cur_r + 1) % ROWS        # Down or 'j'
        elif ch in (curses.KEY_LEFT, ord('h')): self.cur_c = (self.cur_c - 1) % COLS        # Left or 'h'
        elif ch in (curses.KEY_RIGHT, ord('l')): self.cur_c = (self.cur_c + 1) % COLS       # Right or 'l'
        elif ch in (ord(' '), ord('\n')): self.handle_left_click(self.cur_r, self.cur_c)    # Reveal cell at cursor with space or Enter
        elif ch in (ord('f'), ord('F')): self.handle_right_click(self.cur_r, self.cur_c)    # Flag/unflag cell at cursor with 'f/F'

        return True
    
    def reset_game(self):
        """Reset the game frontend & backend to its initial state"""
        self.stdscr.erase()
        self.game_manager = GameManager()
        self.cur_r = 0
        self.cur_c = 0
        self.set_num_mines()
        self.draw_board()

    def display_game_update(self, message_object):
        """
        Display a game update screen (Win or Loss) below the board
        Shows:
          - main_message: primary status message ("You Win" / "You Lost")
          - sub_message: secondary description line
          - control_options: instructions for player input ("p=Play Again q=Quit")
        
        Waits for player input:
          - 'q' quits the game (returns 'quit')
          - 'p' restarts the game (returns 'play_again')
        Loop continues until a valid option is selected.
        """

        # Define messages & control options
        main_message = message_object['main_message']
        sub_message = message_object['sub_message']
        control_options = message_object['control_options']

        # Loop until player provides valid input
        while True:
            sh, sw = self.stdscr.getmaxyx() # Get current terminal size
            
            # Handle case where terminal is too small
            if not self.correct_terminal_size(sh, sw):
                self.display_size_warning()
                self.stdscr.refresh()
                ch = self.stdscr.getch()
                if ch == curses.KEY_RESIZE:
                    continue  # If resize event, recheck terminal size
                continue      # Otherwise, keep looping
            
            # Calculate vertical offset to center board + messages
            off_y, _ = self.center_offsets(sh, sw, ROWS, COLS, CELL_W, CELL_H)

            # Place messages just below the board
            msg_y = off_y + ROWS * CELL_H + 1

            # Calculate x-coordinates to center each message line
            main_message_x = max((sw - len(main_message)) // 2, 0)
            sub_message_x = max((sw - len(sub_message)) // 2, 0)
            control_options_x = max((sw - len(control_options)) // 2, 0)

            try:
                # Draw the three message lines on the screen
                self.stdscr.addstr(msg_y, main_message_x, main_message)
                self.stdscr.addstr(msg_y + 1, sub_message_x, sub_message)
                self.stdscr.addstr(msg_y + 2, control_options_x, control_options)
                self.stdscr.refresh()

                # Wait for player input
                ch = self.get_input()

                # If player presses 'q' → quit game
                if ch == ord('q'):
                    return 'quit'
                
                # If player presses 'p' → play again
                elif ch == ord('p'):
                    curses.noecho()
                    return 'play_again'
                
                # If terminal resized → redraw loop
                elif ch == curses.KEY_RESIZE:
                    continue

            except Exception: 
                curses.noecho()

                # Display error message for invalid input
                error_message = "Invalid input. Please try again"
                error_left_padding = max((sw - len(error_message)) // 2, 0)
                error_y = min(msg_y + 4, sh - 1)  # clamp to last row

                # Show error text on screen
                self.stdscr.addstr(error_y, error_left_padding, error_message[:sw-1])
                self.stdscr.refresh()
                continue # Keep waiting for valid input

                
    def display_win_screen(self):
        """Sends the win message to display_game_update"""
        msg_obj = { 
            'main_message': "Congratulations -- You Win!", 
            'sub_message': "Great job, Champion! You're a force to be reckoned with!",
            'control_options': "p=Play Again  q=Quit: ",
        }
        return self.display_game_update(msg_obj)
        
    def display_loss_screen(self):
        """Sends the loss message to display_game_update"""
        msg_obj = { 
            'main_message': "Sorry :( -- You Lost! ", 
            'sub_message': "This one wasn't your game...",
            'control_options': "p=Play Again  q=Quit: ",
        }
        return self.display_game_update(msg_obj)
