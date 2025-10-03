# vim: set softtabstop=4 shiftwidth=4 :
from classes import Cell, GameManager, GameStatus

BUFFER_VALUE = 64


class Constraint:
    def __init__(self, indices, mines):
        self.indices = indices
        self.mines = mines

    def __str__(self):
        return f"Constraint({'+'.join(str(i) for i in self.indices)}={self.mines})"

    def __repr__(self):
        return self.__str__()


class SimpleSolver:
    def __init__(self, game: GameManager) -> None:
        self.game = game

    def print_grid(self):
        for row in self.game.grid:
            for cell in row:
                character = ""
                # if cell.has_mine():
                #     character = " "
                if cell.is_hidden():
                    character = " "
                else:
                    character = f"{cell.adjacent} "
                print(character, end="")
            print()

    def get_indices_from_cells(self, cells: list[Cell]) -> list[int]:
        """converts a list of cells to a list of their indices"""
        return [cell.row * self.game.rows + cell.col for cell in cells]

    def get_covered(self) -> list[Cell]:
        """get all covered cells on the grid"""
        cells = []
        for row in self.game.grid:
            for cell in row:
                if cell.is_hidden():
                    cells.append(cell)
        return cells

    def get_remaining_adjacent(self, cell: Cell) -> list[int]:
        """get all covered cells adjacent to cell"""
        cells = []

        rows, cols = self.game.rows, self.game.cols
        row, col = cell.row, cell.col
        minRow, minCol = max(0, row - 1), max(0, col - 1)
        maxRow, maxCol = min(rows, row + 2), min(cols, col + 2)

        for row in range(minRow, maxRow):
            for col in range(minCol, maxCol):
                if cell.row == row and cell.col == col:
                    continue
                if self.game.grid[row][col].is_hidden():
                    cells.append(row * self.game.rows + col)
        return cells

    def generate_constraints(self, covered):
        """generate a list of constraints for the board"""
        constraints: list[Constraint] = []

        # get all uncovered cells with adjacent mines
        hints: list[int] = []
        for row in self.game.grid:
            for cell in row:
                if not cell.is_hidden() and cell.adjacent > 0:
                    hints.append(cell)

        # add global constraint for number of mines on the board
        remaining = self.get_indices_from_cells(covered)
        constraints.append(Constraint(remaining, self.game.total_mines))

        # add local constraint for each hint
        for cell in hints:
            remaining = self.get_remaining_adjacent(cell)
            constraints.append(Constraint(remaining, cell.adjacent))

        return constraints

    # https://minesweepergame.com/math/a-simple-minesweeper-algorithm-2023.pdf
    def pick(self) -> tuple[int, int]:
        """pick the best cell to uncover"""

        covered = self.get_covered()

        # if board is fully covered,
        # the best choice is to pick the center
        if len(covered) == self.game.rows * self.game.cols:
            return 0, 0

        # initialize probability table for mines and safe cells
        p_mines: dict[int, float] = dict()
        p_safe: dict[int, float] = dict()
        for cell in covered:
            index = cell.row * self.game.rows + cell.col
            p_mines[index] = 1.0
            p_safe[index] = 1.0

        # initialize list of constraints
        constraints = self.generate_constraints(covered)

        # end when candidates have been the same for `buffer` iterations
        buffer = BUFFER_VALUE
        candidates: list[int] = []
        while buffer:
            for constraint in constraints:
                # scale prob_mines values to total to number of mines
                p_mines_sum: float = sum(p_mines[i] for i in constraint.indices)
                if p_mines_sum != constraint.mines and p_mines_sum != 0:
                    for i in constraint.indices:
                        p_mines[i] *= constraint.mines / p_mines_sum

                # scale prob_safe values to total to number of safe cells
                p_safe_sum: float = sum(p_safe[i] for i in constraint.indices)
                num_safe = len(constraint.indices) - constraint.mines
                if p_safe_sum != num_safe and p_safe_sum != 0:
                    for i in constraint.indices:
                        p_safe[i] *= num_safe / p_safe_sum

            # normalize probalities for mine and safe to equal 1
            for i in p_mines.keys():
                total = p_mines[i] + p_safe[i]
                if total != 0:
                    p_mines[i] /= total
                    p_safe[i] /= total

            # get lowest probability of a mine
            min_value = min(p_mines.values())

            # get all indices with the same probability
            new_candidates = [i for i in p_mines.keys() if p_mines[i] == min_value]

            # decrement buffer if the candidates are the same
            if new_candidates == candidates:
                buffer -= 1
            else:
                candidates = new_candidates

        # pick random candidate
        index = candidates[0]
        row, col = (index // self.game.rows, index % self.game.rows)
        return row, col


match 3:
    case 0:
        mines, rows, cols = 10, 10, 10
    case 1:
        mines, rows, cols = 50, 20, 20
    case 2:
        mines, rows, cols = 135, 30, 30
    case 3:
        mines, rows, cols = 320, 40, 40


def run_game():
    game = GameManager(rows=rows, cols=cols)
    game.set_total_mines(mines)

    solver = SimpleSolver(game)

    while True:
        solver.print_grid()
        coord = solver.pick()
        print(coord)
        game.handle_clicked_cell(*coord)
        if game.game_status != GameStatus.PLAYING:
            break

    solver.print_grid()
    print(game.game_status)


run_game()

# statistics!
