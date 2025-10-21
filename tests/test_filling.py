import time

import numpy as np

from puzzle_solver import filling_solver as solver
from puzzle_solver.core.utils import get_pos

# print('\n\nshould have 1 solution')
# binst = solver.Board(board=np.array([
#   ['1', '3', ' '],
#   ['3', '3', ' '],
# ]))
# solutions = binst.solve_and_print()

# print('\n\nshould have 1 solution')
# binst = solver.Board(board=np.array([
#   ['4', '4', ' '],
#   ['4', '4', ' '],
# ]))
# solutions = binst.solve_and_print()

# print('\n\nshould have 2 solutions')
# binst = solver.Board(board=np.array([
#   ['1', ' ', ' '],
#   ['3', '3', ' '],
# ]))
# solutions = binst.solve_and_print()

# https://www.chiark.greenend.org.uk/~sgtatham/puzzles/js/filling.html#17x13%23390801013916720
# board = np.array([
#   [' ', ' ', ' ', ' ', ' ', '4', ' ', ' ', ' ', '5', ' ', ' ', ' ', '3', '2', ' ', ' '],
#   ['6', '2', ' ', ' ', ' ', '8', ' ', '8', '8', ' ', ' ', ' ', '4', ' ', '5', '3', ' '],
#   [' ', ' ', '2', '6', ' ', ' ', '8', ' ', '8', '8', ' ', '4', '4', '5', ' ', ' ', ' '],
#   [' ', '3', ' ', ' ', '7', ' ', '7', ' ', ' ', ' ', '4', ' ', '9', ' ', '4', ' ', ' '],
#   [' ', ' ', ' ', ' ', ' ', ' ', '7', '9', ' ', '5', '3', ' ', '2', '2', '4', '4', '1'],
#   [' ', '8', ' ', '4', '4', ' ', ' ', ' ', '5', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
#   [' ', '8', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '5', '3', '9', '6', '6', '6', ' ', '8'],
#   [' ', '3', ' ', '2', '8', '3', '8', '2', '2', '3', ' ', ' ', '6', ' ', ' ', ' ', '3'],
#   [' ', ' ', ' ', '2', '4', ' ', ' ', '4', ' ', ' ', ' ', ' ', '5', ' ', ' ', ' ', ' '],
#   [' ', '7', ' ', ' ', ' ', '3', ' ', ' ', ' ', '9', ' ', ' ', ' ', ' ', '7', ' ', ' '],
#   [' ', ' ', '7', ' ', '7', ' ', ' ', ' ', ' ', '6', ' ', '5', '6', '8', ' ', ' ', ' '],
#   ['6', ' ', ' ', ' ', '7', ' ', '6', '9', ' ', '3', ' ', ' ', '5', '7', ' ', '4', ' '],
#   ['2', ' ', ' ', ' ', '7', ' ', ' ', ' ', ' ', ' ', '9', ' ', ' ', ' ', '7', '2', ' '],
# ])
# https://www.chiark.greenend.org.uk/~sgtatham/puzzles/js/filling.html#13x9%23954909678226244
# board = np.array([
#   [' ', ' ', ' ', ' ', '8', ' ', '3', ' ', ' ', ' ', '7', ' ', ' '],
#   ['8', '8', ' ', ' ', '8', ' ', '2', '5', ' ', ' ', ' ', ' ', ' '],
#   ['5', ' ', ' ', ' ', ' ', ' ', '3', ' ', '3', ' ', '7', '2', ' '],
#   [' ', ' ', '5', ' ', ' ', ' ', ' ', '5', '5', ' ', ' ', '7', ' '],
#   [' ', ' ', ' ', '8', ' ', '6', ' ', ' ', ' ', '8', ' ', '3', '4'],
#   ['6', ' ', '8', ' ', ' ', '9', '5', '7', ' ', ' ', ' ', ' ', ' '],
#   [' ', '6', '3', ' ', ' ', ' ', '7', ' ', '8', ' ', ' ', '4', ' '],
#   [' ', ' ', ' ', '5', '5', '5', ' ', '3', ' ', ' ', ' ', ' ', ' '],
#   [' ', ' ', ' ', '4', ' ', '4', ' ', ' ', '3', '5', ' ', '2', '2'],
# ])

# # https://www.chiark.greenend.org.uk/~sgtatham/puzzles/js/filling.html#9x7%23656829517556831
# board = np.array([
#   [' ', '9', '4', '8', ' ', ' ', '8', ' ', ' '],
#   [' ', ' ', ' ', ' ', ' ', '8', '8', ' ', '4'],
#   [' ', ' ', '2', ' ', ' ', ' ', ' ', ' ', '3'],
#   [' ', ' ', ' ', ' ', ' ', '4', ' ', '7', ' '],
#   [' ', '9', '4', ' ', ' ', '4', '8', ' ', '7'],
#   ['9', ' ', ' ', '3', ' ', '8', ' ', ' ', '4'],
#   [' ', '3', '3', ' ', ' ', ' ', '8', ' ', ' '],
# ])
# https://www.chiark.greenend.org.uk/~sgtatham/puzzles/js/filling.html#7x6%23266555745914427
board = np.array([
  [' ', '4', '2', ' ', ' ', '2', ' '],
  [' ', ' ', '7', ' ', ' ', '3', ' '],
  [' ', ' ', ' ', ' ', '4', ' ', '3'],
  [' ', '6', '6', ' ', '3', ' ', ' '],
  [' ', '7', ' ', '6', '4', '5', ' '],
  [' ', '6', ' ', ' ', ' ', ' ', '4'],
])
# board = np.array([
#   ['5', '4', ' ', ' ', '4'],
#   [' ', '5', ' ', ' ', ' '],
#   ['5', ' ', ' ', '2', '2'],
#   ['3', ' ', '3', ' ', ' '],
#   ['2', ' ', ' ', ' ', '5'],
# ])

def test_ground_simple():

  board = np.array([
    ['1', '3', ' '],
    ['3', '3', ' '],
  ])
  binst = solver.Board(board=board)
  solutions = binst.solve_and_print()
  assert len(solutions) == 1, f'unique solutions != 1, == {len(solutions)}'
  solution = solutions[0].assignment
  ground = np.array([
    ['1', '3', '2'],
    ['3', '3', '2'],
  ])
  ground_assignment = {get_pos(x=x, y=y): int(ground[y][x]) for x in range(ground.shape[1]) for y in range(ground.shape[0])}
  assert set(solution.keys()) == set(ground_assignment.keys()), f'solution keys != ground assignment keys, {set(solution.keys()) ^ set(ground_assignment.keys())} \n\n\n{solution} \n\n\n{ground_assignment}'
  for pos in solution.keys():
    assert solution[pos] == ground_assignment[pos], f'solution[{pos}] != ground_assignment[{pos}], {solution[pos]} != {ground_assignment[pos]}'

def test_ground():
  print(f'setting up board')
  tic = time.time()
  binst = solver.Board(board=board)
  toc = time.time()
  print('solving board')
  solutions = binst.solve_and_print()
  print(f'building model took {toc - tic:.2f} seconds')
  ground = np.array([
    ['4', '4', '2', '2', '4', '2', '2'],
    ['4', '4', '7', '4', '4', '3', '3'],
    ['7', '7', '7', '3', '4', '5', '3'],
    ['7', '6', '6', '3', '3', '5', '5'],
    ['7', '7', '6', '6', '4', '5', '5'],
    ['1', '6', '6', '1', '4', '4', '4'],
  ])
  assert len(solutions) == 1, f'unique solutions != 1, == {len(solutions)}'
  solution = solutions[0].assignment
  ground_assignment = {get_pos(x=x, y=y): int(ground[y][x]) for x in range(ground.shape[1]) for y in range(ground.shape[0])}
  assert set(solution.keys()) == set(ground_assignment.keys()), f'solution keys != ground assignment keys, {set(solution.keys()) ^ set(ground_assignment.keys())} \n\n\n{solution} \n\n\n{ground_assignment}'
  for pos in solution.keys():
    assert solution[pos] == ground_assignment[pos], f'solution[{pos}] != ground_assignment[{pos}], {solution[pos]} != {ground_assignment[pos]}'

if __name__ == '__main__':
  test_ground_simple()
  test_ground()
