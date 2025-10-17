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
# https://www.chiark.greenend.org.uk/~sgtatham/puzzles/js/inertia.html#15x12%23518193627142459
bor2 = np.array([
  [" ", "G", " ", " ", "M", "M", "O", "W", "M", "O", " ", " ", "O", "M", "G"],
  ["G", "G", " ", "G", "W", "M", "W", "O", "G", "O", "W", "O", "G", "M", "O"],
  ["O", "G", "O", "G", "M", " ", "W", " ", "W", " ", "O", "G", "W", " ", "B"],
  ["G", " ", "M", "M", "G", "M", "O", "M", "M", "G", "G", "M", "G", "G", "O"],
  [" ", "W", "O", " ", " ", " ", "O", " ", "W", "O", "M", "W", " ", " ", "O"],
  ["O", "O", "M", " ", "W", "G", " ", " ", "W", "G", "W", "W", "O", "W", "W"],
  ["O", "G", " ", " ", "W", "M", "O", "W", "W", "W", "O", "G", "G", "M", "O"],
  ["W", "M", "O", "W", "M", "O", "O", "G", " ", "M", "M", "O", " ", "G", "W"],
  [" ", "M", "W", "O", "M", "O", "O", "W", "M", "O", "W", "G", " ", "M", "G"],
  ["M", "W", "O", "W", "M", "W", "W", "G", " ", "O", " ", "G", "W", "G", "W"],
  ["G", " ", "O", "W", " ", "M", "O", "M", "O", "G", "G", "M", " ", " ", "G"],
  ["M", " ", "W", " ", "M", "M", "M", "W", "M", "G", "W", "M", "G", "G", "G"]
])

def test_ground_1():
  print('board 1:')
  assert np.sum(bor1 == 'B') == 1, 'board must have exactly one start position'
  print('" " count', np.sum(bor1 == ' '))
  print('M count', np.sum(bor1 == 'M'))
  print('G count', np.sum(bor1 == 'G'))
  print('O count', np.sum(bor1 == 'O'))
  print('W count', np.sum(bor1 == 'W'))
  start_pos, edges, edges_to_direction, gems_to_edges = solver.parse_nodes_and_edges(bor1)
  optimal_walk = tsp.solve_optimal_walk(start_pos, edges, gems_to_edges)
  moves = solver.get_moves_from_walk(optimal_walk, edges_to_direction)
  assert solver.is_board_completed(bor1, moves)
  assert len(moves) <= 61, 'website solves it in 61 moves'
  print('#moves found is better than website')

def test_ground_2():
  print('board 2:')
  assert np.sum(bor2 == 'B') == 1, 'board must have exactly one start position'
  print(' count', np.sum(bor2 == ' '))
  print('M count', np.sum(bor2 == 'M'))
  print('G count', np.sum(bor2 == 'G'))
  print('O count', np.sum(bor2 == 'O'))
  print('W count', np.sum(bor2 == 'W'))
  start_pos, edges, edges_to_direction, gems_to_edges = solver.parse_nodes_and_edges(bor2)
  optimal_walk = tsp.solve_optimal_walk(start_pos, edges, gems_to_edges)
  moves = solver.get_moves_from_walk(optimal_walk, edges_to_direction)
  assert solver.is_board_completed(bor2, moves)
  assert len(moves) <= 73, f'website solves it in 73 moves. The optimal here is {len(moves)}'
  print('#moves found is better than website')

if __name__ == '__main__':
  test_ground_1()
  test_ground_2()