import curses
import platform
from ..classes import GameManager, Cell, CellState

ROWS, COLS = 10, 10
CELL_W, CELL_H = 3, 1   # 3 chars per cell, 1 row high

class Front():
    def __init__(self, stdscr, game_manager):
        self.stdscr = stdscr
        self.game_manager = game_manager
        self.cur_r = 0
        self.cur_c = 0

    def center_offsets(self, scr_h, scr_w, rows, cols, cw, ch):
        board_w = cols * cw
        board_h = rows * ch
        off_y = max((scr_h - board_h) // 2, 0)
        off_x = max((scr_w - board_w) // 2, 0)
        return off_y, off_x

    def correct_terminal_size(self, scr_h, sch_w, required_h = (ROWS + 1) * CELL_H + 3, required_w = (COLS + 1) * CELL_W):
        if scr_h < required_h or sch_w < required_w: 
            return False
        return True

    def display_size_warning(self):
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

<<<<<<< HEAD
        while not self.correct_terminal_size(sh, sw):
            self.display_size_warning()
            sh, sw = self.stdscr.getmaxyx()
            self.correct_terminal_size(sh, sw)
=======
    while not correct_terminal_size(sh, sw):
        display_size_warning(stdscr)
        sh, sw = stdscr.getmaxyx()
>>>>>>> d31cba2 (Remove redundant check)

        off_y, _ = self.center_offsets(sh, sw, ROWS, COLS, CELL_W, CELL_H)

        title = "MINESWEEPER"
        prompt = f"Press {start_key} to start with 10 mines, or 'm' to set custom mines"
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

    def init_start_screen(self):
        self.draw_start_screen()
        self.stdscr.erase()

        sh, sw = self.stdscr.getmaxyx()
        off_y, _ = self.center_offsets(sh, sw, ROWS, COLS, CELL_W, CELL_H)

        mode = "menu"
        while True: 
            self.stdscr.erase()

            if mode == "menu":
                self.draw_start_screen()

<<<<<<< HEAD
                ch = self.stdscr.getch()
                if ch in (ord('\n'), ord('\r')): 
                    return 10
                elif ch in (ord('m'), ord('M')):
                    mode = "input"
                elif ch in (ord('q'), ord('Q')): 
                    return None
                else: 
=======
            ch = stdscr.getch()
            if ch in (ord('\n'), ord('\r')): 
                return 10
            elif ch in (ord('m'), ord('M')):
                mode = "input"
            elif ch in (ord('q'), ord('Q')): 
                return None
            else: 
                continue

        elif mode == "input":
            stdscr.erase()

            # Check size
            sh, sw = stdscr.getmaxyx()
            while not correct_terminal_size(sh, sw, 1):
                display_size_warning(stdscr)
                sh, sw = stdscr.getmaxyx()
            
            prompt = f"Enter number of mines (10-20), b=Back: " # -1 since first click can't be a mine
            prompt_left_padding = max((sw - len(prompt)) // 2, 0)
            stdscr.addstr(off_y + 2, prompt_left_padding, prompt)
            stdscr.refresh()

            curses.echo()
            try: 
                # Read up to 3 chars after prompt
                s = stdscr.getstr(off_y + 2, prompt_left_padding + len(prompt), 3).decode()
            
                if s.lower() == 'b': 
                    mode = "menu"
>>>>>>> d31cba2 (Remove redundant check)
                    continue

            elif mode == "input":
                self.stdscr.erase()

                # Check size
                sh, sw = self.stdscr.getmaxyx()
                while not self.correct_terminal_size(sh, sw, 1):
                    self.display_size_warning()
                    sh, sw = self.stdscr.getmaxyx()
                    self.correct_terminal_size(sh, sw, 1)
                
                prompt = f"Enter number of mines (10-20), b=Back: " # -1 since first click can't be a mine
                prompt_left_padding = max((sw - len(prompt)) // 2, 0)
                self.stdscr.addstr(off_y + 2, prompt_left_padding, prompt)
                self.stdscr.refresh()

                curses.echo()
                try: 
                    # Read up to 3 chars after prompt
                    s = self.stdscr.getstr(off_y + 2, prompt_left_padding + len(prompt), 3).decode()
                
                    if s.lower() == 'b': 
                        mode = "menu"
                        continue

                    mines = int(s)
                    if not (10 <= mines <= 20):
                        raise ValueError("Out of range")
                    
                    return mines
            
                except Exception:
                    curses.noecho()
                    error_message = "Invalid input. Press any key..."
                    error_left_padding = max((sw - len(error_message))//2, 0)
                    
                    self.stdscr.addstr(off_y + 4, error_left_padding, error_message)
                    self.stdscr.refresh()
                    self.stdscr.getch()
                    continue
                finally: 
                    curses.noecho()

    def draw_board(self):
        self.stdscr.erase()
        sh, sw = self.stdscr.getmaxyx()

        if not self.correct_terminal_size(sh, sw):
            self.display_size_warning()
            return

        off_y, off_x = self.center_offsets(sh, sw, ROWS, COLS, CELL_W, CELL_H)

        for r in range(ROWS+1):
            alphabet = "abcdefghijklmnopqrstuvwxyz"
            for c in range(COLS+1):
                y = off_y + r * CELL_H
                x = off_x + c * CELL_W

                # DRAWING BOARD EDGES
                if (c == 0 and r == 0):
                    self.stdscr.addstr(y,x," ")
                    continue
                elif (c == 0):
                    self.stdscr.addstr(y,x, f"{alphabet[r-1]}")
                    continue
                elif (r == 0):
                    self.stdscr.addstr(y,x,f"{c}")
                    continue

                # Get cell and render output depending on cell status
                cell = self.game_manager.grid[r % ROWS][c % COLS]

                if cell.flagged:
                    ch = "⚑"

                if cell.hidden and not cell.flagged:
                    ch = "H"
                elif cell.state == CellState.MINED:
                    ch = "0" 
                elif cell.state == CellState.HASADJACENT:
                    ch = cell.adjacent
                elif cell.state == CellState.MINE:
                    ch = "X"
                elif cell.state == CellState.NONEADJACENT:
                    ch = " "
                elif cell.state is None and not cell.flagged:
                    ch = " "

                # highlight cursor
                if (self.cur_r, self.cur_c) == (r, c):
                    self.stdscr.attron(curses.A_REVERSE)
                    self.stdscr.addstr(y, x, f"[{ch}]")
                    self.stdscr.attroff(curses.A_REVERSE)
                else:
                    self.stdscr.addstr(y, x, f"[{ch}]")

        # Simple help bar
        self.stdscr.addstr(sh-1, 0,
            f"Remaining Mines: {self.game_manager.remaining_mine_count}"
        )
        self.stdscr.addstr(sh-2, 0,
            f"Game State: {self.game_manager.game_status}"
        )
        self.stdscr.addstr(sh-3, 0,
            "Arrows=move  Space=Reveal  f=Flag  Mouse: Left=Reveal Right=Flag  q=Quit  ",
        )
        self.stdscr.clrtoeol()
        self.stdscr.refresh()

    def mouse_to_cell(self, mx, my):
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
        self.game_manager.hide_cell(r, c)

    def handle_right_click(self, r, c):
        if self.game_manager.is_flagged(r, c):
            self.game_manager.remove_flag(r, c)
        else:
            self.game_manager.place_flag(r, c)

    def get_input(self):
        return self.stdscr.getch()
    
    def process_input(self, ch):
        if ch == ord('q'):
            self.game_manager.should_quit = True
            return False

        if ch == curses.KEY_RESIZE:
            self.draw_board(self.stdscr)
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

            # Right-click
            elif bstate & curses.BUTTON3_CLICKED or bstate & curses.BUTTON3_PRESSED:
                self.handle_right_click(r, c)

            self.draw_board()
            return True

        # Keyboard navigation
        if ch in (curses.KEY_UP, ord('k')):   self.cur_r = (self.cur_r - 1) % ROWS
        elif ch in (curses.KEY_DOWN, ord('j')): self.cur_r = (self.cur_r + 1) % ROWS
        elif ch in (curses.KEY_LEFT, ord('h')): self.cur_c = (self.cur_c - 1) % COLS
        elif ch in (curses.KEY_RIGHT, ord('l')): self.cur_c = (self.cur_c + 1) % COLS
        elif ch in (ord(' '), ord('\n')):     self.handle_left_click(self.cur_r, self.cur_c)
        elif ch in (ord('f'), ord('F')):      self.handle_left_click(self.cur_r, self.cur_c)
        return True
