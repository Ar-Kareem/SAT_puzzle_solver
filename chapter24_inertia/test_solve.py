import numpy as np

from . import solver
from . import tsp
from core.utils import Direction8


# https://www.chiark.greenend.org.uk/~sgtatham/puzzles/js/inertia.html#15x12%23919933974949365
bor1 = np.array([
  ["M", "W", " ", "M", "O", "O", "W", "O", "W", "O", "O", " ", "W", " ", "M"],
  ["M", " ", "O", "M", "W", "O", " ", "M", "W", "G", "W", " ", "M", "W", "G"],
  ["M", "O", " ", "M", " ", "G", " ", "M", "M", "O", "G", " ", "O", "O", "W"],
  ["B", " ", " ", "M", "G", "O", "O", "W", "G", "M", "M", "G", "W", "W", "W"],
  ["G", "M", "G", "O", "M", "G", "M", "O", "G", "G", "G", "G", "G", " ", "O"],
  ["O", "W", "O", "G", "O", "G", "O", "G", "G", "G", " ", "W", "G", " ", "W"],
  ["M", " ", " ", "M", " ", " ", "W", "M", "O", "W", "W", "G", "O", "O", "W"],
  ["W", "O", " ", "W", "W", "W", "O", "G", "G", "O", "W", "G", "O", "M", "O"],
  [" ", " ", " ", "M", "M", "O", "M", "W", "M", "G", "G", "M", "M", " ", " "],
  ["W", "O", "W", "W", "G", "M", "G", "W", "G", " ", "M", "O", "M", "W", "M"],
  ["G", " ", "M", "O", "O", "G", "G", " ", "O", " ", "W", "G", " ", "M", " "],
  ["G", " ", "G", "M", "M", "W", "W", " ", "O", "O", "M", " ", "W", "W", " "]
])

def test_ground_1():
  start_pos, edges, edges_to_direction, gems_to_edges = solver.parse_nodes_and_edges(bor1)
  optimal_walk = tsp.solve_optimal_walk(start_pos, edges, gems_to_edges)
  moves = solver.get_moves_from_walk(optimal_walk, edges_to_direction)
  assert solver.is_board_completed(bor1, moves)
  assert len(moves) <= 61, 'website solves it in 61 moves'


if __name__ == '__main__':
  test_ground_1()
