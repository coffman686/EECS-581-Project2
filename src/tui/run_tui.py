import curses
from curses.textpad import Textbox, rectangle
import platform
from src.classes import GameManager, Cell, CellState, GameStatus

ROWS, COLS = 10, 10
CELL_W, CELL_H = 3, 1   # 3 chars per cell, 1 row high

class Frontend():
    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.game_manager = GameManager()
        self.cur_r = 0
        self.cur_c = 0
        self.clicked_cells = []
        self.alphabet = "abcdefghijklmnopqrstuvwxyz"

    def draw_game_status(self):
        sh, sw = self.stdscr.getmaxyx()

        self.stdscr.addstr(3, sw // 2 - 10,
            f"Game State: {str(self.game_manager.game_status)[11:]}"
        )

    def set_num_mines(self):
        self.stdscr.erase()
        sh, sw = self.stdscr.getmaxyx()

        while not self.correct_terminal_size(sh, sw):
            self.display_size_warning()
            sh, sw = self.stdscr.getmaxyx()
            self.stdscr.refresh()
            curses.napms(100)
            self.stdscr.erase()

        self.stdscr.addstr(0, 0, "Enter the number of mines for this game: (Press Enter to send)")

        editwin = curses.newwin(5, 30, 2, 1)
        rectangle(self.stdscr, 1, 0, 1 + 5 + 1, 1 + 30 + 1)
        self.stdscr.refresh()

        box = Textbox(editwin)

        # Remap Enter to submit instead of Ctrl-G
        def enter_terminate(ch):
            if ch == 10:
                return 7
            return ch

        box.edit(enter_terminate)

        # Get resulting contents
        num_mines = box.gather().strip()
        try:
            num_mines = int(num_mines)
            if num_mines < 1 or num_mines >= ROWS * COLS:
                raise ValueError("Invalid number of mines.")
            
            self.game_manager.set_total_mines(num_mines)
            self.game_manager.total_flags = num_mines
            self.game_manager.remaining_flag_count = num_mines
        except ValueError:
            self.stdscr.addstr(8, 0, "Error: Please enter a valid number between 1 and {}.".format(ROWS * COLS - 1))
            self.stdscr.refresh()
            curses.napms(1500)
            self.set_num_mines()

    def center_offsets(self, scr_h, scr_w, rows, cols, cw, ch):
        board_w = cols * cw
        board_h = rows * ch
        off_y = max((scr_h - board_h) // 2, 0)
        off_x = max((scr_w - board_w) // 2, 0)
        return off_y, off_x

    def correct_terminal_size(self, scr_h, sch_w, required_h = (ROWS + 1) * CELL_H + 9, required_w = (COLS + 1) * CELL_W):
        if scr_h < required_h or sch_w < required_w: 
            return False
        return True

    def display_size_warning(self):
        self.stdscr.erase()
        warning = "Terminal too small! Please resize window."
        self.stdscr.addstr(0, 0, warning)
        self.stdscr.refresh()

    def find_start_key(self): 
        os_name = platform.system()
        if os_name == "Darwin": 
            return "Return"
        
        return "Enter"

    def draw_start_screen(self): 
        self.stdscr.erase()
        sh, sw = self.stdscr.getmaxyx()
        start_key = self.find_start_key()
        self.draw_game_status()

        if not self.correct_terminal_size(sh, sw):
            self.display_size_warning()
            return False

        off_y, _ = self.center_offsets(sh, sw, ROWS, COLS, CELL_W, CELL_H)

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
        self.stdscr.refresh()
        
        return True
    
    def start_game(self):
        while True:
            if not self.draw_start_screen():    
                ch = self.get_input()
                if ch == curses.KEY_RESIZE:
                    continue    
                continue
            
            ch = self.get_input()
            if ch in (ord('\n'), ord('\r')):
                break
            elif ch == ord('q'):
                self.game_manager.should_quit = True
                return
            elif ch == curses.KEY_RESIZE:
                continue
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

        # Print clicked cells at the top (currently commented out)
        # clicks_str = "Clicked: " + ", ".join(
        #     [f"({self.alphabet[c]},{r+1}) ADJ: {self.game_manager.grid[c][r].adjacent}" for r, c in self.clicked_cells]
        # )
        # self.stdscr.addstr(0, 0, clicks_str[:sw-1])  # top row

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

                if cell.flagged:
                    ch = "⚑"
                elif cell.hidden:
                    ch = "H"
                elif cell.state == CellState.MINED:
                    ch = "M"
                elif cell.adjacent != 0:
                    ch = str(cell.adjacent)
                elif cell.state == CellState.MINE:
                    ch = "X"
                elif cell.state == CellState.NONEADJACENT:
                    ch = " "
                elif cell.state is None:
                    ch = " "

                # Highlight cursor
                if (self.cur_r, self.cur_c) == (r, c):
                    self.stdscr.attron(curses.A_REVERSE)
                    self.stdscr.addstr(y, x, f"[{ch}]")
                    self.stdscr.attroff(curses.A_REVERSE)
                else:
                    self.stdscr.addstr(y, x, f"[{ch}]")

        # Simple help bar
        self.stdscr.addstr(sh - 1, 0,
            f"Remaining Mines: {self.game_manager.remaining_mine_count}"
        )
        self.stdscr.addstr(sh - 2, 0,
            f"Remaining Flags: {self.game_manager.remaining_flag_count}"
        )
        self.stdscr.addstr(sh - 4, 0,
            "Arrows=move  Space=Reveal  f=Flag  Mouse: Left=Reveal Right=Flag  q=Quit  ",
        )
        self.stdscr.clrtoeol()
        self.stdscr.refresh()

        # AFTER drawing the board, check if game over
        result = self.check_game_status()
        if result == 'quit':
            self.game_manager.should_quit = True
            return False
        elif result == 'play_again':
            self.reset_game()
            return True

    def mouse_to_cell(self, mx, my):
        """Processes user clicks on cells"""
        sh, sw = self.stdscr.getmaxyx()
        off_y, off_x = self.center_offsets(sh, sw, ROWS, COLS, CELL_W, CELL_H)
        # inside board?
        if my < off_y or mx < off_x:
            return None
        if my >= off_y + ROWS * CELL_H or mx >= off_x + COLS * CELL_W:
            return None
        r = (my - off_y) // CELL_H
        c = (mx - off_x) // CELL_W
        if 0 <= r < ROWS and 0 <= c < COLS:
            return (r, c)
        return None

    def handle_left_click(self, r, c):
        self.game_manager.handle_clicked_cell(r, c)

    def handle_right_click(self, r, c):
        if self.game_manager.is_flagged(r, c):
            self.game_manager.remove_flag(r, c)
        else:
            self.game_manager.place_flag(r, c)

    def get_input(self):
        return self.stdscr.getch()
    
    def check_game_status(self):
        if self.game_manager.game_status == GameStatus.WIN: 
            return self.display_win_screen()
        elif self.game_manager.game_status == GameStatus.LOSE:
            return self.display_loss_screen()
        return None
    
    def process_input(self, ch):
        if ch == ord('q'):
            self.game_manager.should_quit = True
            return False

        if ch == curses.KEY_RESIZE:
            self.draw_board()
            return True

        if ch == curses.KEY_MOUSE:
            try:
                _, mx, my, _, bstate = curses.getmouse()
            except curses.error:
                return True

            pos = self.mouse_to_cell(mx, my)
            if not pos:
                return True
            r, c = pos
            self.cur_r, self.cur_c = r, c

            # Left-click (terminals vary: check CLICKED/PRESSED)
            if bstate & curses.BUTTON1_CLICKED or bstate & curses.BUTTON1_PRESSED:
                self.handle_left_click(r, c)
                self.clicked_cells.append((r, c))  # add clicked cell

                # testing this
                self.game_manager.handle_clicked_cell(r, c)


            # Right-click
            elif bstate & curses.BUTTON3_CLICKED or bstate & curses.BUTTON3_PRESSED:
                self.handle_right_click(r, c)

            return True

        # Keyboard navigation
        if ch in (curses.KEY_UP, ord('k')):   self.cur_r = (self.cur_r - 1) % ROWS
        elif ch in (curses.KEY_DOWN, ord('j')): self.cur_r = (self.cur_r + 1) % ROWS
        elif ch in (curses.KEY_LEFT, ord('h')): self.cur_c = (self.cur_c - 1) % COLS
        elif ch in (curses.KEY_RIGHT, ord('l')): self.cur_c = (self.cur_c + 1) % COLS
        elif ch in (ord(' '), ord('\n')):     
            self.handle_left_click(self.cur_r, self.cur_c)
            self.clicked_cells.append((self.cur_r, self.cur_c)) 
        elif ch in (ord('f'), ord('F')):      self.handle_right_click(self.cur_r, self.cur_c)
        return True
    
    def reset_game(self):
        self.stdscr.erase()
        self.game_manager = GameManager()
        self.cur_r = 0
        self.cur_c = 0
        self.clicked_cells = []
        self.set_num_mines()
        self.draw_board()

    def display_game_update(self, message_object):
        main_message = message_object['main_message']
        sub_message = message_object['sub_message']
        control_options = message_object['control_options']

        while True:
            sh, sw = self.stdscr.getmaxyx()

            if not self.correct_terminal_size(sh, sw):
                self.display_size_warning()
                self.stdscr.refresh()
                ch = self.stdscr.getch()
                if ch == curses.KEY_RESIZE:
                    continue
                continue
            
            off_y, _ = self.center_offsets(sh, sw, ROWS, COLS, CELL_W, CELL_H)

            # Place messages just below the board
            msg_y = off_y + ROWS * CELL_H + 1

            main_message_x = max((sw - len(main_message)) // 2, 0)
            sub_message_x = max((sw - len(sub_message)) // 2, 0)
            control_options_x = max((sw - len(control_options)) // 2, 0)

            try:
                self.stdscr.addstr(msg_y, main_message_x, main_message)
                self.stdscr.addstr(msg_y + 1, sub_message_x, sub_message)
                self.stdscr.addstr(msg_y + 2, control_options_x, control_options)
                self.stdscr.refresh()

                ch = self.get_input()
                if ch == ord('q'):
                    return 'quit'
                elif ch == ord('p'):
                    curses.noecho()
                    return 'play_again'
                else:
                    raise Exception

            except Exception: 
                curses.noecho()

                error_message = "Invalid input. Please try again"
                error_left_padding = max((sw - len(error_message)) // 2, 0)

                error_y = min(msg_y + 4, sh - 1)  # clamp to last row
                self.stdscr.addstr(error_y, error_left_padding, error_message[:sw-1])
                self.stdscr.refresh()
                continue

                
    def display_win_screen(self):
        msg_obj = { 
            'main_message': "Congratulations -- You Win!", 
            'sub_message': "Great job, Champion! You're a force to be reckoned with!",
            'control_options': "p=Play Again  q=Quit: ",
        }
        return self.display_game_update(msg_obj)
        
    def display_loss_screen(self):
        msg_obj = { 
            'main_message': "Sorry :( -- You Lost! ", 
            'sub_message': "This one wasn't your game...",
            'control_options': "p=Play Again  q=Quit: ",
        }
        return self.display_game_update(msg_obj)
