import numpy as np
import time
from puzzle_solver import inertia_solver as solver


# https://www.chiark.greenend.org.uk/~sgtatham/puzzles/js/inertia.html#15x12%23919933974949365
board1 = np.array([
  ['M', 'W', ' ', 'M', 'O', 'O', 'W', 'O', 'W', 'O', 'O', ' ', 'W', ' ', 'M'],
  ['M', ' ', 'O', 'M', 'W', 'O', ' ', 'M', 'W', 'G', 'W', ' ', 'M', 'W', 'G'],
  ['M', 'O', ' ', 'M', ' ', 'G', ' ', 'M', 'M', 'O', 'G', ' ', 'O', 'O', 'W'],
  ['B', ' ', ' ', 'M', 'G', 'O', 'O', 'W', 'G', 'M', 'M', 'G', 'W', 'W', 'W'],
  ['G', 'M', 'G', 'O', 'M', 'G', 'M', 'O', 'G', 'G', 'G', 'G', 'G', ' ', 'O'],
  ['O', 'W', 'O', 'G', 'O', 'G', 'O', 'G', 'G', 'G', ' ', 'W', 'G', ' ', 'W'],
  ['M', ' ', ' ', 'M', ' ', ' ', 'W', 'M', 'O', 'W', 'W', 'G', 'O', 'O', 'W'],
  ['W', 'O', ' ', 'W', 'W', 'W', 'O', 'G', 'G', 'O', 'W', 'G', 'O', 'M', 'O'],
  [' ', ' ', ' ', 'M', 'M', 'O', 'M', 'W', 'M', 'G', 'G', 'M', 'M', ' ', ' '],
  ['W', 'O', 'W', 'W', 'G', 'M', 'G', 'W', 'G', ' ', 'M', 'O', 'M', 'W', 'M'],
  ['G', ' ', 'M', 'O', 'O', 'G', 'G', ' ', 'O', ' ', 'W', 'G', ' ', 'M', ' '],
  ['G', ' ', 'G', 'M', 'M', 'W', 'W', ' ', 'O', 'O', 'M', ' ', 'W', 'W', ' ']
])
# https://www.chiark.greenend.org.uk/~sgtatham/puzzles/js/inertia.html#15x12%23518193627142459
board2 = np.array([
  [' ', 'G', ' ', ' ', 'M', 'M', 'O', 'W', 'M', 'O', ' ', ' ', 'O', 'M', 'G'],
  ['G', 'G', ' ', 'G', 'W', 'M', 'W', 'O', 'G', 'O', 'W', 'O', 'G', 'M', 'O'],
  ['O', 'G', 'O', 'G', 'M', ' ', 'W', ' ', 'W', ' ', 'O', 'G', 'W', ' ', 'B'],
  ['G', ' ', 'M', 'M', 'G', 'M', 'O', 'M', 'M', 'G', 'G', 'M', 'G', 'G', 'O'],
  [' ', 'W', 'O', ' ', ' ', ' ', 'O', ' ', 'W', 'O', 'M', 'W', ' ', ' ', 'O'],
  ['O', 'O', 'M', ' ', 'W', 'G', ' ', ' ', 'W', 'G', 'W', 'W', 'O', 'W', 'W'],
  ['O', 'G', ' ', ' ', 'W', 'M', 'O', 'W', 'W', 'W', 'O', 'G', 'G', 'M', 'O'],
  ['W', 'M', 'O', 'W', 'M', 'O', 'O', 'G', ' ', 'M', 'M', 'O', ' ', 'G', 'W'],
  [' ', 'M', 'W', 'O', 'M', 'O', 'O', 'W', 'M', 'O', 'W', 'G', ' ', 'M', 'G'],
  ['M', 'W', 'O', 'W', 'M', 'W', 'W', 'G', ' ', 'O', ' ', 'G', 'W', 'G', 'W'],
  ['G', ' ', 'O', 'W', ' ', 'M', 'O', 'M', 'O', 'G', 'G', 'M', ' ', ' ', 'G'],
  ['M', ' ', 'W', ' ', 'M', 'M', 'M', 'W', 'M', 'G', 'W', 'M', 'G', 'G', 'G']
])
# https://www.chiark.greenend.org.uk/~sgtatham/puzzles/js/inertia.html#20x16%23200992952951435
board3 = np.array([
  ['O', 'O', 'M', ' ', 'G', 'O', 'G', 'O', ' ', ' ', 'M', ' ', ' ', 'O', 'G', 'G', 'W', 'O', 'O', 'O'],
  ['O', ' ', 'W', ' ', 'W', 'O', 'G', 'M', ' ', ' ', ' ', 'G', 'M', 'O', 'W', 'G', ' ', 'M', 'M', 'O'],
  ['O', 'M', 'O', 'O', ' ', 'M', ' ', 'W', 'W', 'M', 'G', 'W', ' ', ' ', 'G', ' ', 'W', 'G', 'O', 'G'],
  ['O', ' ', 'O', 'M', 'G', 'O', 'W', 'G', 'M', 'O', ' ', ' ', 'G', 'G', 'G', ' ', 'M', 'W', 'M', 'O'],
  ['M', 'M', 'O', 'G', ' ', 'W', ' ', ' ', 'O', 'G', ' ', 'M', 'M', ' ', 'W', 'W', ' ', 'W', 'W', 'O'],
  ['G', ' ', 'G', 'W', 'M', 'W', 'W', ' ', 'G', 'G', 'W', 'M', 'G', 'G', ' ', 'G', 'O', 'O', 'M', 'M'],
  ['M', ' ', 'M', ' ', 'W', 'W', 'M', 'M', 'M', 'O', 'M', 'G', 'O', 'M', 'M', 'W', 'B', 'O', 'W', 'M'],
  ['G', 'G', ' ', 'W', 'M', 'M', 'W', 'O', 'W', 'G', 'W', 'O', 'O', 'M', ' ', 'W', 'W', 'G', 'G', 'M'],
  [' ', 'M', 'M', ' ', ' ', ' ', 'G', 'G', 'M', 'O', 'M', 'O', 'M', 'G', 'W', 'M', 'W', ' ', 'O', ' '],
  ['G', ' ', 'M', ' ', ' ', ' ', 'W', 'O', 'W', 'W', 'M', 'M', 'G', 'W', ' ', ' ', 'W', 'M', 'G', 'W'],
  ['G', 'O', 'M', 'M', 'G', 'M', 'W', 'O', 'O', 'G', 'W', 'M', 'M', 'G', 'G', ' ', 'O', ' ', 'W', 'W'],
  ['G', 'G', 'W', 'G', 'M', ' ', 'G', 'W', 'W', ' ', 'G', ' ', 'O', 'W', 'G', 'G', 'O', ' ', 'M', 'M'],
  ['W', 'M', 'O', ' ', 'W', 'O', 'O', 'M', 'M', 'O', 'G', 'W', ' ', 'G', 'O', 'G', 'G', 'O', 'O', 'W'],
  ['W', 'W', 'W', ' ', 'W', 'O', 'W', 'M', 'O', 'M', 'G', 'O', 'O', ' ', ' ', 'W', 'W', 'G', 'W', 'W'],
  ['O', 'W', 'O', 'M', 'O', 'G', ' ', 'O', 'O', 'M', 'O', ' ', 'M', 'M', 'O', 'G', 'W', 'G', 'M', ' '],
  ['M', 'G', 'O', 'G', 'O', 'G', 'O', 'G', ' ', 'W', 'W', 'G', 'O', ' ', 'W', 'M', 'G', ' ', 'W', ' ']
])

def _test_ground(board: np.array, website_moves: int, expected = None):
  tic = time.time()
  assert np.sum(board == 'B') == 1, 'board must have exactly one start position'
  print('" " count', np.sum(board == ' '))
  print('M count', np.sum(board == 'M'))
  print('G count', np.sum(board == 'G'))
  print('O count', np.sum(board == 'O'))
  print('W count', np.sum(board == 'W'))
  start_pos, edges, edges_to_direction, gems_to_edges = solver.parse_nodes_and_edges(board)
  tic = time.time()
  optimal_walk = solver.solve_optimal_walk(start_pos, edges, gems_to_edges)
  toc = time.time()
  print(f'Time taken: {toc - tic:.2f} seconds')
  moves = solver.get_moves_from_walk(optimal_walk, edges_to_direction)
  assert solver.is_board_completed(board, moves)
  assert len(moves) <= website_moves, f'website solves it in {website_moves} moves. The optimal here is {len(moves)}'
  toc = time.time()
  print(f'Time taken: {toc - tic:.2f} seconds')
  if expected is not None:
    assert len(moves) == expected, f'expected {expected} moves, got {len(moves)}'
def test_ground_1():
  print('board 1:')
  board = board1
  _test_ground(board, 61)  # expected: 47

def test_ground_2():
  print('board 2:')
  _test_ground(board2, 73)  # expected: 60

def test_ground_3():
  print('board 3:')
  _test_ground(board3, 121)  # expected: 106

# _test_ground(np.array([
#   ['M', 'O', 'G'],
#   ['B', ' ', 'G'],
#   ['W', 'M', 'M'],
# ]), 6, expected=4)


if __name__ == '__main__':
  test_ground_1()
  test_ground_2()
  test_ground_3()