# Module: Ai_mode
# Description: Implements ai solver with easy, medium, and hard difficulty settings
# Inputs: Cell
# Outputs: AI_mode()
# External sources:
#   Medium solver algorithm: https://minesweepergame.com/math/a-simple-minesweeper-algorithm-2023.pdf by Mike Sheppard
# Authors: Hale Coffman, Aryan Kevat
# Creation Date: 2025-09-29

import random
from decimal import Decimal
from enum import Enum

from classes import Cell

BUFFER_VALUE = 2**6


class Mode(Enum):
    NONE = 0
    EASY = 1
    MEDIUM = 2
    HARD = 3


class Constraint:
    def __init__(self, indices, mines):
        self.indices = indices
        self.mines = mines

    def __str__(self):
        return f"Constraint({'+'.join(str(i) for i in self.indices)}={self.mines})"

    def __repr__(self):
        return self.__str__()


class AI_mode:
    def __init__(self, game_manager):
        self.mode = Mode(0)
        self.is_turn = False
        self.game_manager = game_manager
        self.is_automatic_solver = False

    def set_mode_easy(self):
        self.mode = Mode.EASY

    def set_mode_medium(self):
        self.mode = Mode.MEDIUM

    def set_mode_hard(self):
        self.mode = Mode.HARD

    def change_turn(self):
        if self.is_automatic_solver:
            return
        else:
            if self.game_manager.game_status.name == "PLAYING":
                self.is_turn = not self.is_turn

    def ai_turn(self):
        if self.mode.name == "EASY":
            return self.easy_ai_turn()
        elif self.mode.name == "MEDIUM":
            return self.medium_ai_turn()
        elif self.mode.name == "HARD":
            return self.hard_ai_turn()

    def easy_ai_turn(self):
        valid_moves = []
        for r in range(10):
            for c in range(10):
                cell = self.game_manager.grid[r][c]
                if cell.is_hidden() and not cell.has_flag():
                    valid_moves.append((r, c))

        if len(valid_moves) > 0:
            index = random.randint(0, len(valid_moves) - 1)
            r_rand, c_rand = valid_moves[index]
            self.game_manager.handle_clicked_cell(r_rand, c_rand)
            return (r_rand, c_rand)

        return (0, 0)

    def get_indices_from_cells(self, cells: list[Cell]) -> list[int]:
        """converts a list of cells to a list of their indices"""
        return [cell.row * 10 + cell.col for cell in cells]

    def get_covered(self) -> list[Cell]:
        """get all covered cells on the grid"""
        cells = []
        for row in self.game_manager.grid:
            for cell in row:
                if cell.is_hidden():
                    cells.append(cell)
        return cells

    def get_remaining_adjacent(self, cell: Cell) -> list[int]:
        """get all covered cells adjacent to cell"""
        cells = []

        rows, cols = self.game_manager.rows, self.game_manager.cols
        row, col = cell.row, cell.col
        minRow, minCol = max(0, row - 1), max(0, col - 1)
        maxRow, maxCol = min(rows, row + 2), min(cols, col + 2)

        for row in range(minRow, maxRow):
            for col in range(minCol, maxCol):
                if cell.row == row and cell.col == col:
                    continue
                if self.game_manager.grid[row][col].is_hidden():
                    cells.append(row * 10 + col)
        return cells

    def generate_constraints(self, covered):
        """generate a list of constraints for the board"""
        constraints: list[Constraint] = []

        # get all uncovered cells with adjacent mines
        hints: list[int] = []
        for row in self.game_manager.grid:
            for cell in row:
                if not cell.is_hidden() and cell.adjacent > 0:
                    hints.append(cell)

        # add global constraint for number of mines on the board
        remaining = self.get_indices_from_cells(covered)
        constraints.append(Constraint(remaining, self.game_manager.total_mines))

        # add local constraint for each hint
        for cell in hints:
            remaining = self.get_remaining_adjacent(cell)
            constraints.append(Constraint(remaining, cell.adjacent))

        return constraints

    def medium_ai_turn(self) -> tuple[int, int]:
        """
        pick the best cell to uncover
        https://minesweepergame.com/math/a-simple-minesweeper-algorithm-2023.pdf
        """

        covered = self.get_covered()

        # if board is fully covered,
        # the best choice is to pick a corner
        if len(covered) == self.game_manager.rows * self.game_manager.cols:
            self.game_manager.handle_clicked_cell(0, 0)
            return 0, 0

        # initialize probability table for mines and safe cells
        p_mines: dict[int, Decimal] = dict()
        p_safe: dict[int, Decimal] = dict()
        for cell in covered:
            index = cell.row * 10 + cell.col
            p_mines[index] = Decimal(1.0)
            p_safe[index] = Decimal(1.0)

        # initialize list of constraints
        constraints = self.generate_constraints(covered)

        # end when candidates have been the same for `buffer` iterations
        buffer = BUFFER_VALUE
        candidates: list[int] = []
        while buffer:
            for constraint in constraints:
                # scale prob_mines values to total to number of mines
                p_mines_sum: Decimal = sum(p_mines[i] for i in constraint.indices)
                if p_mines_sum != constraint.mines:
                    for i in constraint.indices:
                        p_mines[i] *= constraint.mines / p_mines_sum

                # scale prob_safe values to total to number of safe cells
                p_safe_sum: Decimal = sum(p_safe[i] for i in constraint.indices)
                num_safe = len(constraint.indices) - constraint.mines
                if p_safe_sum != num_safe:
                    for i in constraint.indices:
                        p_safe[i] *= num_safe / p_safe_sum

            # normalize probalities for mine and safe to equal 1
            for i in p_mines.keys():
                total = p_mines[i] + p_safe[i]
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
                # update candidates and reset buffer
                candidates = new_candidates
                buffer = BUFFER_VALUE

        # pick random candidate
        index = candidates[0]
        row, col = (index // 10, index % 10)
        self.game_manager.handle_clicked_cell(row, col)
        return row, col

    def hard_ai_turn(self):
        valid_moves = []
        for r in range(10):
            for c in range(10):
                cell = self.game_manager.grid[r][c]
                if cell.is_hidden() and not cell.has_mine():
                    valid_moves.append((r, c))

        if len(valid_moves) > 0:
            index = random.randint(0, len(valid_moves) - 1)
            r_rand, c_rand = valid_moves[index]
            self.game_manager.handle_clicked_cell(r_rand, c_rand)
            return (r_rand, c_rand)

        return (0, 0)
