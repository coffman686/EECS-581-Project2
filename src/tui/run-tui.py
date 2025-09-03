from rich import print
from rich.console import Console
from rich.layout import Layout
from rich.panel import Panel
from rich.live import Live

# from game import gameState 
class GameState:
    total_mine_count : int = 10 
    remaining_mine_count : int = total_mine_count
    game_statuses = ["Game Loss" , "Playing" , "Victory"]
    def __init__(self):
        self.game_status = self.game_statuses[1]


MIN_MAP_WIDTH = 80

console = Console()

# build layout - this stuff is kinda weird - https://rich.readthedocs.io/en/stable/layout.html#fixed-size

root = Layout()
root.split_column(
    Layout(name="upper"),       # map row
    Layout(name="lower", size=3)  # status bars
)

root["upper"].split_row(
    Layout(name="map"),
    Layout(name="sidebar", ratio=1)
)

root["lower"].split_row(
        Layout(name="remaining_mines"),
        Layout(name="game_status")
        )

root["map"].minimum_size = MIN_MAP_WIDTH
root["sidebar"].visible = False

game = GameState()

def render():
    width = console.size.width
    if width < MIN_MAP_WIDTH:
        root["map"].update(Panel(f"Terminal is too narrow"))
    else:
        map_str = "MAP"
        root["map"].update(Panel(map_str, title=f"Map ({width} cols)"))
        root["remaining_mines"].update(Panel(f"Remaining Mines: {game.remaining_mine_count}"))
        root["game_status"].update(Panel(f"Game Status: {game.game_status}"))


with Live(root, console=console, screen=True, refresh_per_second=10):
    while True:
        render()
