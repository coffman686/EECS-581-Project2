from textual.app import App, ComposeResult
from textual.containers import Grid, Horizontal
from textual.widgets import Button, Label

ROWS, COLS = 15, 15

class Minesweeper(App):
    CSS = f"""
    Screen {{
        align: center middle;
    }}

    #topbar {{
        dock: top;
        height: 3;
        background: $boost;
        content-align: center middle;
    }}

    #bottombar {{
        dock: bottom;
        height: 3;
        background: $boost;
        content-align: center middle;
    }}

    #board {{
        grid-size: {COLS+1} {ROWS+1};  /* +1 for headers */
        grid-gutter: 0 0;
    }}

    Button {{
        width: 3;
        height: 5;
        content-align: center middle;
        border: round;
    }}

    Label {{
        content-align: center middle;
    }}
    """

    def compose(self) -> ComposeResult:
        # Top status row
        yield Horizontal(
            Label("Remaining Mines: 99", id="mines"),
            Label("Game Status: Running", id="status"),
            id="topbar",
        )

        # Main board grid
        yield Grid(id="board")

        # Bottom bar (optional)
        yield Horizontal(
            Label("Timer: 0s", id="timer"),
            id="bottombar",
        )

    def on_mount(self) -> None:
        board = self.query_one("#board", Grid)

        # Top-left empty corner
        board.mount(Label(""))

        alphabet = "abcdefghijklmnopqrstuvwxyz"
        # Column headers
        for c in range(COLS):
            board.mount(Label(f"     {alphabet[c]}"))

        # Rows + cells
        for r in range(ROWS):
            board.mount(Label(f"\n{r}"))
            for c in range(COLS):
                board.mount(Button("·", id=f"cell-{r}-{c}"))

    def on_button_pressed(self, event: Button.Pressed) -> None:
        rows, cols = map(int, event.button.id.split("-")[1:])
        event.button.label = "X"

        # Update status labels
        self.query_one("#mines", Label).update(f"Remaining Mines: {ROWS*COLS - (rows*COLS+cols+1)}")
        self.query_one("#status", Label).update("Game Status: Playing")

if __name__ == "__main__":
    Minesweeper().run()

