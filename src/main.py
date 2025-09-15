import curses
from src.classes import GameStatus, GameManager
from src.tui.run_tui import Front

def setup_curses(stdscr):
    curses.curs_set(0)
    stdscr.keypad(True)
    curses.mousemask(curses.ALL_MOUSE_EVENTS | curses.REPORT_MOUSE_POSITION)
    curses.mouseinterval(150)

def main(stdscr):
    ### Initialize
    setup_curses(stdscr)
    manager = GameManager() 
    frontend = Front(stdscr, manager)

    # Show start screen and get mine count
    mine_count = frontend.init_start_screen()
    if mine_count is None: 
        return 
    manager.set_total_mines(mine_count)
    
    frontend.draw_board()

    ### Main loop
    # Get user input, process that input, output the new grid data
    while True:
        success = frontend.process_input(frontend.get_input())
        if manager.should_quit or not success:
            break
        else:
            frontend.draw_board()

if __name__ == "__main__":
    curses.wrapper(main)
