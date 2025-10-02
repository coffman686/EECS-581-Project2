from classes import Cell
from enum import Enum
import random

from functools import partial
from itertools import product

class Mode(Enum):
    NONE = 0
    EASY = 1
    MEDIUM = 2
    HARD = 3


class AI_mode():
    def __init__(self, game_manager):
        self.mode = Mode(0)
        self.is_turn = False
        self.game_manager = game_manager

    def set_mode_easy(self):
        self.mode = Mode.EASY

    def set_mode_medium(self):
        self.mode = Mode.MEDIUM

    def set_mode_hard(self):
        self.mode = Mode.HARD

    def change_turn(self):
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

        return (0,0)

    def medium_ai_turn(self):
      class CellPred(Enum):
        PRED_SAFE = 0
        PRED_MINE = 1
        COVERED = 2
        KNOWN_MINE = 3

      # Flattened list of cells
      def get_cells() -> list[Cell]:
        return [cell for row in self.game_manager.grid for cell in row]

      def is_covered(cell: Cell):
        return cell.is_hidden()

      def is_uncovered(cell: Cell):
        return not cell.is_hidden()

      # Get most centered cell (worst random candidate allegedly)
      def random_key(cell: Cell) -> int:
        middle_row = (self.game_manager.rows - 1) / 2
        middle_col = (self.game_manager.cols - 1) / 2

        dist_mid_row = abs(middle_row - cell.row)
        dist_mid_col = abs(middle_col - cell.col)

        return dist_mid_row + dist_mid_col

      # Get all neighbors of a cell with an optional filter
      def get_neighbors(cell: Cell, filter=lambda x: True) -> list[Cell]:
        neighbors = []
        for row in range(cell.row - 1, cell.row + 2):
          for col in range(cell.col - 1, cell.col + 2):
            if 0 <= row < self.game_manager.rows and 0 <= col < self.game_manager.cols:
              target = self.game_manager.grid[row][col]
              if filter(target):
                neighbors.append(self.game_manager.grid[row][col])
        return neighbors

      # Get whether the cell has extra bordering cells than adjacent mines
      def has_extra_cells(cell: Cell):
        covered_neighbors = get_neighbors(cell, is_covered)
        return len(covered_neighbors) > 0 and (len(covered_neighbors) - cell.adjacent) > 0

      def get_num_extra_cells(cell: Cell):
        covered_neighbors = get_neighbors(cell, is_covered)
        return len(covered_neighbors) - cell.adjacent

      def get_edge_cells(edge_covered: list[Cell]) -> list[Cell]:
        edge = []
        for cell in edge_covered:
          for neighbor in get_neighbors(cell, is_covered):
            if neighbor not in edge:
              edge.append(neighbor)
        return edge

      def make_cluster(cell: Cell, edge_cells: list):
        cluster: list[Cell] = []
        for nb in get_neighbors(cell, is_covered):
          if nb in edge_cells:
            cluster.append(nb)
            edge_cells.remove(nb)
            cluster.extend(make_cluster(nb, edge_cells))
        return cluster

      def make_clusters(edge_cells: list[Cell]) -> list[list[Cell]]:
        clusters: list[list[Cell]] = []
        while len(edge_cells):
          cluster = make_cluster(edge_cells[0], edge_cells)
          clusters.append(cluster)

        clusters.sort(key=lambda x: len(x))
        return clusters

      def find_valid_states(grid: list[list[CellPred]], cluster: list[Cell], depth):
        states: list[tuple[int]] = []

        shallow_cluster = cluster[:depth]

        # Create every state
        for state in product([CellPred.PRED_SAFE, CellPred.PRED_MINE], repeat=depth):
          # Set each cell in the cluster to its state
          for pred, cell in enumerate(shallow_cluster):
            grid[cell.row][cell.col] = state[pred]

          if validate_state(shallow_cluster, grid, state):
            states.append(state)

        # Reset grid
        for cell in shallow_cluster:
          grid[cell.row][cell.col] = CellPred.COVERED

        return states


      def validate_state(cluster: list[Cell], grid: list[list[int]], c: tuple[int]):
        # Evaluate all cells in the cluster
        for cell in cluster:
          # Get all adjacent cells
          for adj in get_neighbors(cell):
            if adj.hidden:
              continue

            if adj in cluster:
              continue

            covered = 0
            count = 0

            for nb in get_neighbors(adj, is_covered):
              state = grid[nb.row][nb.col]
              if state == CellPred.COVERED:
                covered += 1
              elif state != CellPred.PRED_SAFE:
                count += 1

            # Don't overload a cell
            if count > adj.adjacent:
              return False

            # Don't underload a cell
            if covered < (adj.adjacent - count):
              return False

        return True


      # Find cells that are always safe or always mines
      def find_shared(grid: list[list[CellPred]], cluster: list[Cell], depth: int, valid_states: list[tuple[int]]):
        candidate: Cell = None
        for i in range(depth):
          safe = True
          mine = True

          for state in valid_states:
            safe = safe and state[i] == CellPred.PRED_SAFE
            mine = mine and state[i] == CellPred.PRED_MINE

          if mine:
            c = cluster[i]
            grid[c.row][c.col] = CellPred.KNOWN_MINE

          if safe and candidate is None:
            candidate = cluster[i]

        return candidate

      candidate: Cell | None = None

      cells = get_cells()

      covered = list(filter(is_covered, cells))
      uncovered = list(filter(is_uncovered, cells))

      uncovered_extra = list(filter(lambda x: has_extra_cells(x), uncovered))
      uncovered_extra = sorted(uncovered_extra, key=lambda x: get_num_extra_cells(x))
      edge_cells = get_edge_cells(uncovered_extra)
      clusters = make_clusters(edge_cells)

      # Create grid for simulations
      grid = [[CellPred.COVERED for _ in range(10)] for _ in range(10)]

      for cluster in clusters:
        for depth in range(1, len(cluster) + 1):
          valid_states = find_valid_states(grid, cluster, depth)
          if len(valid_states) == 0:
            continue
          candidate = find_shared(grid, cluster, depth, valid_states)
          if candidate:
            break
        if candidate:
          break

      # If still uncertain (ie first pick), pick random cell from outwards in, prioritizing the center
      if candidate is None:
        best_random_candidate = sorted(covered, key=partial(random_key), reverse=True)
        candidate = best_random_candidate[0]

      self.game_manager.handle_clicked_cell(candidate.row, candidate.col)
      return candidate.row, candidate.col

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

        return (0,0)
