# pip install textual
from textual.app import App, ComposeResult
from textual.containers import Grid
from textual.widgets import Button, Label

ROWS, COLS = 10, 10

class Minesweeper(App):
    CSS = f"""
    #board {{
        grid-size: {COLS+1} {ROWS+1};   /* +1 for headers */
        grid-gutter: 0 0;
    }}

    Button {{
        width: 5;               /* columns */
        height: 10;              /* rows (cell lines) */
        content-align: center middle;
        border: round;          /* visible tile edges */
    }}

    Label {{
        content-align: center middle;
    }}
    """

    def compose(self) -> ComposeResult:
        yield Grid(id="board")

    def on_mount(self) -> None:
        board = self.query_one("#board", Grid)

        # Top-left empty corner
        board.mount(Label(""))

        # Column headers
        for c in range(COLS):
            board.mount(Label(str(c), id=f"col-{c}"))

        # Rows + cells
        for r in range(ROWS):
            board.mount(Label(str(r), id=f"row-{r}"))
            for c in range(COLS):
                board.mount(Button("·", id=f"cell-{r}-{c}"))

    def on_button_pressed(self, event: Button.Pressed) -> None:
        r, c = map(int, event.button.id.split("-")[1:])
        event.button.label = "X" if event.button.label == "·" else "·"
        self.log(f"Clicked cell {r},{c}")

if __name__ == "__main__":
    Minesweeper().run()

