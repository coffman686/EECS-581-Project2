# pip install pytermgui
import time
import threading
import shutil

import pytermgui as ptg
from src.main import GameState

MIN_MAP_WIDTH = 80
game = GameState()

# --- Widgets ---------------------------------------------------------------

map_label = ptg.Label("")                 # top "map" panel body
remaining_label = ptg.Label("")           # bottom-left status
status_label = ptg.Label("")              # bottom-right status

# Make a framed "map box" with a visible border
map_box = ptg.Window(map_label, box="DOUBLE")
map_box.set_title("Map", position=0)

# Bottom row: two statuses side-by-side, also framed
remaining_box = ptg.Window(remaining_label, box="SINGLE")
status_box = ptg.Window(status_label, box="SINGLE")

bottom_row = ptg.Splitter(
    remaining_box,
    status_box,
)

# Root content: map (top) + bottom row (bottom)
root = ptg.Container(
    map_box,        # <-- framed map on top
    bottom_row,     # statuses with frames
)
map_box.height = 30

# Wrap in an outer window so we get a main frame/title
main_win = ptg.Window(root, box="HEAVY")
main_win.width = ptg.get_terminal().width
main_win.height = ptg.get_terminal().height
main_win.set_title("Minesweeper", position=0)

# --- Render/update loop ----------------------------------------------------

def render():
    """Update widget text based on terminal width & game state."""
    width = ptg.get_terminal().width  # terminal size from PTG
    if width < MIN_MAP_WIDTH:
        map_label.value = "[bold red]Terminal is too narrow[/]"
    else:
        # You can substitute your actual rendered map string here
        map_str = "MAP"
        map_label.value = f"[bold]Map ({width} cols)[/]\n{map_str}"

    remaining_label.value = f"[bold]Remaining Mines:[/] {game.remaining_mine_count}"
    status_label.value = f"[bold]Game Status:[/] {game.game_status}"

def start_updater(manager: ptg.WindowManager, fps: int = 10):
    """Kick off a background thread that updates labels periodically."""
    interval = 1.0 / fps

    def _loop():
        while manager._is_running:          # manager flag; okay to read
            render()
            # Mark the window as dirty to ensure redraw this frame
            main_win.is_dirty = True
            time.sleep(interval)

    t = threading.Thread(target=_loop, daemon=True)
    t.start()

# --- Run -------------------------------------------------------------------

if __name__ == "__main__":
    render()  # initial paint

    # WindowManager handles the draw loop & input; we add our window and run.
    with ptg.WindowManager(autorun=False) as manager:
        manager += main_win.center()

        # Optional: constrain minimum width visually by padding the window
        main_win.min_width = MIN_MAP_WIDTH

        start_updater(manager, fps=10)
        manager.run()

