import curses
from src.classes import GameStatus, GameManager
from src.tui.run_tui import Frontend

def setup_curses(stdscr):
    curses.curs_set(0)
    stdscr.keypad(True)
    curses.mousemask(curses.ALL_MOUSE_EVENTS | curses.REPORT_MOUSE_POSITION)
    curses.mouseinterval(150)

def main(stdscr):
    ### Initialize

    # Show start screen and get mine count

    setup_curses(stdscr)

    frontend = Frontend(stdscr)
    frontend.set_num_mines()
    
    stdscr.refresh()
    frontend.start_game()


if __name__ == "__main__":
    curses.wrapper(main)