import curses
import platform
from ..classes import GameManager, Cell, CellState

ROWS, COLS = 10, 10
CELL_W, CELL_H = 3, 1   # 3 chars per cell, 1 row high

def run():
    curses.wrapper(main)

def center_offsets(scr_h, scr_w, rows, cols, cw, ch):
    board_w = cols * cw
    board_h = rows * ch
    off_y = max((scr_h - board_h) // 2, 0)
    off_x = max((scr_w - board_w) // 2, 0)
    return off_y, off_x

def correct_terminal_size(scr_h, sch_w, required_h = (ROWS + 1) * CELL_H + 3, required_w = (COLS + 1) * CELL_W):
    if scr_h < required_h or sch_w < required_w: 
        return False
    return True

def display_size_warning(stdscr):
    warning = "Terminal too small! Please resize window."
    stdscr.addstr(0, 0, warning)
    stdscr.refresh()

def find_start_key(): 
    os_name = platform.system()
    if os_name == "Darwin": 
        return "Return"
    
    return "Enter"

def draw_start_screen(stdscr): 
    stdscr.erase()
    sh, sw = stdscr.getmaxyx()
    start_key = find_start_key()

    while not correct_terminal_size(sh, sw):
        display_size_warning(stdscr)
        sh, sw = stdscr.getmaxyx()

    off_y, _ = center_offsets(sh, sw, ROWS, COLS, CELL_W, CELL_H)

    title = "MINESWEEPER"
    prompt = f"Press {start_key} to start with 10 mines, or 'm' to set custom mines"
    controls = "Arrows=move  Space=Reveal  f=Flag  Mouse: Left=Reveal Right=Flag  q=Quit"

    # Calculate starting locations on x-axis (padding)
    title_scr_x = max((sw - len(title)) // 2, 0)
    prompt_scr_x = max((sw - len(prompt)) // 2, 0)
    controls_scr_x = max((sw - len(controls)) // 2, 0)

    # Display centered text
    stdscr.addstr(off_y, title_scr_x, title)
    stdscr.addstr(off_y + 2, prompt_scr_x, prompt)
    stdscr.addstr(off_y + 4, controls_scr_x, controls)
    stdscr.refresh()

def init_start_screen(stdscr):
    draw_start_screen(stdscr)
    stdscr.erase()

    sh, sw = stdscr.getmaxyx()
    off_y, _ = center_offsets(sh, sw, ROWS, COLS, CELL_W, CELL_H)

    mode = "menu"
    while True: 
        stdscr.erase()

        if mode == "menu":
            draw_start_screen(stdscr)

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
                    continue

                mines = int(s)
                if not (10 <= mines <= 20):
                    raise ValueError("Out of range")
                
                return mines
        
            except Exception:
                curses.noecho()
                error_message = "Invalid input. Press any key..."
                error_left_padding = max((sw - len(error_message))//2, 0)
                
                stdscr.addstr(off_y + 4, error_left_padding, error_message)
                stdscr.refresh()
                stdscr.getch()
                continue
            finally: 
                curses.noecho()

def draw_board(stdscr, grid, gameManager, cursor=None):
    stdscr.erase()
    sh, sw = stdscr.getmaxyx()

    if not correct_terminal_size(sh, sw):
        display_size_warning(stdscr)
        return
    
    off_y, off_x = center_offsets(sh, sw, ROWS, COLS, CELL_W, CELL_H)

    for r in range(ROWS+1):
        alphabet = "abcdefghijklmnopqrstuvwxyz"
        for c in range(COLS+1):
            y = off_y + r * CELL_H
            x = off_x + c * CELL_W

            # DRAWING BOARD EDGES
            if (c == 0 and r == 0):
                stdscr.addstr(y,x," ")
                continue
            elif (c == 0):
                stdscr.addstr(y,x, f"{alphabet[r-1]}")
                continue
            elif (r == 0):
                stdscr.addstr(y,x,f"{c}")
                continue

            # Get cell and render output depending on cell status
            cell = grid[r % ROWS][c % COLS]

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
            if cursor == (r, c):
                stdscr.attron(curses.A_REVERSE)
                stdscr.addstr(y, x, f"[{ch}]")
                stdscr.attroff(curses.A_REVERSE)
            else:
                stdscr.addstr(y, x, f"[{ch}]")

    # Simple help bar
    stdscr.addstr(sh-1, 0,
        f"Remaining Mines: {gameManager.remaining_mine_count}"
    )
    stdscr.addstr(sh-2, 0,
        f"Game State: {gameManager.game_status}"
    )
    stdscr.addstr(sh-3, 0,
        "Arrows=move  Space=Reveal  f=Flag  Mouse: Left=Reveal Right=Flag  q=Quit  ",
    )
    stdscr.clrtoeol()
    stdscr.refresh()

def mouse_to_cell(stdscr, mx, my):
    sh, sw = stdscr.getmaxyx()
    off_y, off_x = center_offsets(sh, sw, ROWS, COLS, CELL_W, CELL_H)
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

def handle_left_click(gameManager, r, c):
    gameManager.grid[r][c].hidden = False
    return gameManager

def handle_right_click(gameManager, r, c):
    if (gameManager.grid[r][c].flagged == True):
        gameManager.grid[r][c].flagged =  False
    else:
        gameManager.grid[r][c].flagged = True
    return gameManager


def main(stdscr):
    curses.curs_set(0)
    stdscr.keypad(True)
    curses.mousemask(curses.ALL_MOUSE_EVENTS | curses.REPORT_MOUSE_POSITION)
    curses.mouseinterval(150)

    # Show start screen and get mine count
    mine_count = init_start_screen(stdscr)
    if mine_count is None: 
        return 

    # Build grid with chosen mine count
    gameManager = GameManager(mine_count)
    grid = gameManager.grid
    cur_r, cur_c = 0, 0

    draw_board(stdscr, grid,gameManager, (cur_r, cur_c))

    while True:
        ch = stdscr.getch()

        if ch == ord('q'):
            break

        if ch == curses.KEY_RESIZE:
            draw_board(stdscr, grid, gameManager,  (cur_r, cur_c))
            continue

        if ch == curses.KEY_MOUSE:
            try:
                _, mx, my, _, bstate = curses.getmouse()
            except curses.error:
                continue

            pos = mouse_to_cell(stdscr, mx, my)
            if not pos:
                continue
            r, c = pos
            cur_r, cur_c = r, c
            # Left-click (terminals vary: check CLICKED/PRESSED)
            if bstate & curses.BUTTON1_CLICKED or bstate & curses.BUTTON1_PRESSED:

                gameManager = handle_left_click(gameManager, r, c)
            # Right-click
            elif bstate & curses.BUTTON3_CLICKED or bstate & curses.BUTTON3_PRESSED:

                gameManager = handle_right_click(gameManager, r, c)

            draw_board(stdscr, grid, gameManager, (cur_r, cur_c))
            continue

        # Keyboard navigation
        if ch in (curses.KEY_UP, ord('k')):   cur_r = (cur_r - 1) % ROWS
        elif ch in (curses.KEY_DOWN, ord('j')): cur_r = (cur_r + 1) % ROWS
        elif ch in (curses.KEY_LEFT, ord('h')): cur_c = (cur_c - 1) % COLS
        elif ch in (curses.KEY_RIGHT, ord('l')): cur_c = (cur_c + 1) % COLS
        elif ch in (ord(' '), ord('\n')):     handle_left_click(gameManager, cur_r, cur_c)
        elif ch in (ord('f'), ord('F')):      handle_left_click(gameManager, cur_r, cur_c)

        draw_board(stdscr, grid, gameManager,(cur_r, cur_c))

if __name__ == "__main__":
    curses.wrapper(main)

