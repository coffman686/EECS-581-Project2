import curses
from ..main import GameState, Cell, CellState

ROWS, COLS = 10, 10
CELL_W, CELL_H = 3, 1   # 3 chars per cell, 1 row high

def center_offsets(scr_h, scr_w, rows, cols, cw, ch):
    board_w = cols * cw
    board_h = rows * ch
    off_y = max((scr_h - board_h) // 2, 0)
    off_x = max((scr_w - board_w) // 2, 0)
    return off_y, off_x

def draw_board(stdscr, grid, gameState, cursor=None):
    stdscr.erase()
    sh, sw = stdscr.getmaxyx()
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
        f"Remaining Mines: {gameState.remaining_mine_count}"
    )
    stdscr.addstr(sh-2, 0,
        f"Game State: {gameState.game_status}"
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

def handle_left_click(gameState, r, c):
    gameState.grid[r][c].hidden = False
    return gameState

def handle_right_click(gameState, r, c):
    if (gameState.grid[r][c].flagged == True):
        gameState.grid[r][c].flagged =  False
    else:
        gameState.grid[r][c].flagged = True
    return gameState


def main(stdscr):
    curses.curs_set(0)
    stdscr.keypad(True)
    curses.mousemask(curses.ALL_MOUSE_EVENTS | curses.REPORT_MOUSE_POSITION)
    curses.mouseinterval(150)

    # build grid
    gameState = GameState()
    grid = gameState.grid
    cur_r, cur_c = 0, 0

    draw_board(stdscr, grid,gameState, (cur_r, cur_c))

    while True:
        ch = stdscr.getch()

        if ch == ord('q'):
            break

        if ch == curses.KEY_RESIZE:
            draw_board(stdscr, grid, gameState,  (cur_r, cur_c))
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

                gameState = handle_left_click(gameState, r, c)
            # Right-click
            elif bstate & curses.BUTTON3_CLICKED or bstate & curses.BUTTON3_PRESSED:

                gameState = handle_right_click(gameState, r, c)

            draw_board(stdscr, grid, gameState, (cur_r, cur_c))
            continue

        # Keyboard navigation
        if ch in (curses.KEY_UP, ord('k')):   cur_r = (cur_r - 1) % ROWS
        elif ch in (curses.KEY_DOWN, ord('j')): cur_r = (cur_r + 1) % ROWS
        elif ch in (curses.KEY_LEFT, ord('h')): cur_c = (cur_c - 1) % COLS
        elif ch in (curses.KEY_RIGHT, ord('l')): cur_c = (cur_c + 1) % COLS
        elif ch in (ord(' '), ord('\n')):     handle_left_click(gameState, cur_r, cur_c)
        elif ch in (ord('f'), ord('F')):      handle_left_click(gameState, cur_r, cur_c)

        draw_board(stdscr, grid, gameState,(cur_r, cur_c))

if __name__ == "__main__":
    curses.wrapper(main)

