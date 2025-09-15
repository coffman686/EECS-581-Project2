import curses
import platform
from src.classes import GameManager, Cell, CellState, GameStatus

ROWS, COLS = 10, 10
CELL_W, CELL_H = 3, 1   # 3 chars per cell, 1 row high


def center_offsets(scr_h, scr_w, rows, cols, cw, ch):
    board_w = cols * cw
    board_h = rows * ch
    off_y = max((scr_h - board_h) // 2, 0)
    off_x = max((scr_w - board_w) // 2, 0)
    return off_y, off_x


def correct_terminal_size(scr_h, scr_w, required_h=(ROWS + 1) * CELL_H + 3,
                          required_w=(COLS + 1) * CELL_W):
    if scr_h < required_h or scr_w < required_w:
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
            while not correct_terminal_size(sh, sw, 3):
                display_size_warning(stdscr)
                sh, sw = stdscr.getmaxyx()

            prompt = f"Enter number of mines (10-20), b=Back: "
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
                error_left_padding = max((sw - len(error_message)) // 2, 0)

                stdscr.addstr(off_y + 4, error_left_padding, error_message)
                stdscr.refresh()
                stdscr.getch()
                continue
            finally:
                curses.noecho()


def draw_board(stdscr, grid, gameManager, cursor=None):
    """Draw the game board on the screen"""

    # Clear the screen
    stdscr.erase()

    # Get Screen height & width
    sh, sw = stdscr.getmaxyx()
    off_y, off_x = center_offsets(sh, sw, ROWS, COLS, CELL_W, CELL_H)

    # Row labels
    alphabet = "abcdefghijklmnopqrstuvwxyz"

    # Draw column numbers
    for c in range(COLS):
        x = off_x + c * CELL_W
        stdscr.addstr(off_y - 1, x + 1, f"{c+1}")

    # Draw row letters
    for r in range(ROWS):
        y = off_y + r * CELL_H
        stdscr.addstr(y, off_x - 2, f"{alphabet[r]}")

    # Draw the cells
    for r in range(ROWS):
        for c in range(COLS):
            cell = grid[r][c]

            if cell.flagged:
                ch = "⚑"
            #elif cell.hidden:
            #    ch = "H"
            elif cell.state == CellState.MINED:
                ch = "M"
            elif cell.state == CellState.HASADJACENT:
                ch = str(cell.adjacent)
            elif cell.state == CellState.NONEADJACENT:
                ch = " "
            elif cell.state is None and not cell.flagged:
                ch = " "

            # Calculate screen coordinates for this cell
            y = off_y + r * CELL_H
            x = off_x + c * CELL_W

            # Highlight the cursor position if applicable
            if cursor == (r, c):
                stdscr.attron(curses.A_REVERSE)
                stdscr.addstr(y, x, f"[{ch}]")
                stdscr.attroff(curses.A_REVERSE)
            else:
                stdscr.addstr(y, x, f"[{ch}]")

    # Footer info
    stdscr.addstr(sh - 1, 0,
        f"Remaining Mines: {gameManager.remaining_mine_count}"
    )
    stdscr.addstr(sh - 2, 0,
        f"Game State: {gameManager.game_status.name}"
    )
    stdscr.addstr(sh - 3, 0,
        "Arrows=move  Space=Reveal  f=Flag  Mouse: Left=Reveal Right=Flag  q=Quit"
    )

    # Clear rest of line
    stdscr.clrtoeol()
    stdscr.refresh()


def mouse_to_cell(stdscr, mx, my):
    """Processes user clicks on cells"""
    
    # Get Screen height & width
    sh, sw = stdscr.getmaxyx()
    off_y, off_x = center_offsets(sh, sw, ROWS, COLS, CELL_W, CELL_H)

    # Check if click is inside the board area
    if my < off_y or mx < off_x:
        return None
    if my >= off_y + ROWS * CELL_H or mx >= off_x + COLS * CELL_W:
        return None

    # Convert screen coordinates -> grid indices
    r = (my - off_y) // CELL_H
    c = (mx - off_x) // CELL_W

    # Only return valid cells
    if 0 <= r < ROWS and 0 <= c < COLS:
        return (r, c)

    return None


def main(stdscr):
    curses.curs_set(0)
    stdscr.keypad(True)
    curses.mousemask(curses.ALL_MOUSE_EVENTS | curses.REPORT_MOUSE_POSITION)
    curses.mouseinterval(150)

    # Show start screen and get mine count
    mine_count = init_start_screen(stdscr)
    if mine_count is None:
        return

    stdscr.clear()
    stdscr.refresh()

    # Build grid with chosen mine count
    gameManager = GameManager(ROWS, COLS, mine_count)
    grid = gameManager.grid
    cur_r, cur_c = 0, 0
    clicked_cells = []

    while True:
        # 1. Draw board (this clears screen)
        draw_board(stdscr, grid, gameManager, (cur_r, cur_c))

        # 2. Print clicked cells at the top (after board draw)
        sh, sw = stdscr.getmaxyx()
        clicks_str = "Clicked: " + ", ".join([f"({r},{c})" for r, c in clicked_cells])
        stdscr.addstr(0, 0, clicks_str[:sw-1])  # top row
        stdscr.clrtoeol()
        stdscr.refresh()

        # 3. Wait for input
        ch = stdscr.getch()
        if ch == ord('q'):
            break

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

            if bstate & (curses.BUTTON1_CLICKED | curses.BUTTON1_PRESSED):
                clicked_cells.append((r, c))  # add clicked cell

if __name__ == "__main__":
    curses.wrapper(main)
