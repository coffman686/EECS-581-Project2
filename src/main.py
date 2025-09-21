"""
File: main.py
Module: src
Function: Start the initial game environment and pass control to the frontend. 
Inputs:
    - None
Outputs:
    - None
Authors: 
    Blake Carlson
    Logan Smith
    Jack Bauer
    Delroy Wright
    Nifemi Lawal
Date: 9/3/2025
NOTE: All code in the file was authored by 1 or more of the authors. No outside sources were used for code
"""
import curses # This is our terminal interface library. It's how we setup our UI.
from src.tui.run_tui import Frontend # This class "runs" the actual game.

def setup_curses(stdscr):
    """Setup some basic curses settings that are required for our app to function."""
    # Disable blinking cursor.
    curses.curs_set(0)
    # Enable keypad mode. This allows easier usage of special keys that are normally multibyte sequences.
    stdscr.keypad(True)
    # NOTE: Mouse support is highly dependent on which terminal is being used. 
    curses.mousemask(curses.ALL_MOUSE_EVENTS | curses.REPORT_MOUSE_POSITION)
    curses.mouseinterval(150)

def main(stdscr):
    """Initialize the UI environment and pass control to the frontend."""
    # Setup curses, create the Frontend object, set the number of mines for the game, 
    # refresh the UI, and start the game.
    setup_curses(stdscr)
    frontend = Frontend(stdscr)
    frontend.set_num_mines()
    stdscr.refresh()
    frontend.start_game()

# Actually run the program.
if __name__ == "__main__":
    # Use a curses handler function so that terminal state is restored properly on application exit.
    curses.wrapper(main)