import curses
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

    def draw_board(self):
        self.stdscr.erase()
        sh, sw = self.stdscr.getmaxyx()
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
                game_manager = self.handle_left_click(r, c)

            # Right-click
            elif bstate & curses.BUTTON3_CLICKED or bstate & curses.BUTTON3_PRESSED:
                game_manager = self.handle_right_click(r, c)

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

def main(stdscr):
    curses.curs_set(0)
    stdscr.keypad(True)
    curses.mousemask(curses.ALL_MOUSE_EVENTS | curses.REPORT_MOUSE_POSITION)
    curses.mouseinterval(150)

    # build grid
    game_manager = GameManager()
    front = Front(stdscr, game_manager)
    front.draw_board()

    while True:
        ch = front.get_input()
        success = front.process_input(ch)
        if not success:
            break
        else: 
            front.draw_board()

if __name__ == "__main__":
    curses.wrapper(main)

