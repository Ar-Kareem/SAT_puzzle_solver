import numpy as np

from puzzle_solver import unruly_solver as solver
from puzzle_solver.core.utils import get_pos

# https://www.chiark.greenend.org.uk/~sgtatham/puzzles/js/unruly.html#14x14dn%23472699508059540
board = np.array([
  ['W', 'W', ' ', 'B', ' ', ' ', ' ', ' ', 'B', ' ', ' ', ' ', ' ', ' '],
  [' ', ' ', ' ', ' ', ' ', ' ', ' ', 'W', ' ', ' ', ' ', ' ', ' ', 'W'],
  [' ', ' ', ' ', ' ', ' ', 'B', ' ', 'W', ' ', ' ', 'B', ' ', ' ', ' '],
  [' ', ' ', 'W', ' ', ' ', ' ', ' ', ' ', ' ', 'W', ' ', 'W', ' ', ' '],
  ['B', ' ', ' ', 'W', ' ', ' ', ' ', ' ', 'B', ' ', ' ', ' ', ' ', ' '],
  [' ', ' ', ' ', ' ', ' ', 'B', ' ', ' ', ' ', 'B', ' ', 'B', ' ', ' '],
  [' ', 'B', 'B', ' ', ' ', 'B', ' ', ' ', ' ', ' ', ' ', 'B', ' ', ' '],
  [' ', ' ', 'B', ' ', ' ', ' ', ' ', 'W', ' ', 'B', 'B', ' ', ' ', 'W'],
  [' ', ' ', ' ', ' ', ' ', ' ', ' ', 'W', ' ', ' ', ' ', ' ', ' ', 'W'],
  [' ', ' ', ' ', 'B', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
  [' ', ' ', 'W', ' ', ' ', ' ', 'W', ' ', ' ', 'W', ' ', 'W', ' ', ' '],
  [' ', 'W', ' ', 'W', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'B'],
  [' ', ' ', ' ', ' ', 'B', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
  ['W', ' ', ' ', ' ', 'W', ' ', ' ', ' ', 'B', ' ', 'W', ' ', 'B', ' '],
])

def test_ground():
  binst = solver.Board(board=board)
  # assert False
  solutions = binst.solve_and_print()
  ground = np.array([
    ['W', 'W', 'B', 'B', 'W', 'B', 'W', 'B', 'B', 'W', 'B', 'W', 'W', 'B'],
    ['B', 'B', 'W', 'W', 'B', 'W', 'B', 'W', 'W', 'B', 'W', 'B', 'B', 'W'],
    ['W', 'W', 'B', 'W', 'W', 'B', 'B', 'W', 'B', 'W', 'B', 'B', 'W', 'B'],
    ['W', 'B', 'W', 'B', 'B', 'W', 'W', 'B', 'W', 'W', 'B', 'W', 'B', 'B'],
    ['B', 'W', 'B', 'W', 'B', 'W', 'B', 'W', 'B', 'B', 'W', 'W', 'B', 'W'],
    ['B', 'W', 'W', 'B', 'W', 'B', 'B', 'W', 'B', 'B', 'W', 'B', 'W', 'W'],
    ['W', 'B', 'B', 'W', 'W', 'B', 'W', 'B', 'W', 'W', 'B', 'B', 'W', 'B'],
    ['B', 'W', 'B', 'W', 'B', 'W', 'B', 'W', 'W', 'B', 'B', 'W', 'B', 'W'],
    ['B', 'B', 'W', 'B', 'B', 'W', 'B', 'W', 'B', 'W', 'W', 'B', 'W', 'W'],
    ['W', 'W', 'B', 'B', 'W', 'B', 'W', 'B', 'W', 'B', 'W', 'W', 'B', 'B'],
    ['B', 'B', 'W', 'W', 'B', 'W', 'W', 'B', 'B', 'W', 'B', 'W', 'B', 'W'],
    ['B', 'W', 'B', 'W', 'W', 'B', 'B', 'W', 'W', 'B', 'W', 'B', 'W', 'B'],
    ['W', 'B', 'W', 'B', 'B', 'W', 'W', 'B', 'W', 'B', 'B', 'W', 'W', 'B'],
    ['W', 'B', 'W', 'B', 'W', 'B', 'W', 'B', 'B', 'W', 'W', 'B', 'B', 'W'],
  ])
  assert len(solutions) == 1, f'unique solutions != 1, == {len(solutions)}'
  solution = solutions[0].assignment
  ground_assignment = {get_pos(x=x, y=y): 1 if ground[y][x] == 'B' else 0 for x in range(ground.shape[1]) for y in range(ground.shape[0])}
  assert set(solution.keys()) == set(ground_assignment.keys()), f'solution keys != ground assignment keys, {set(solution.keys()) ^ set(ground_assignment.keys())} \n\n\n{solution} \n\n\n{ground_assignment}'
  for pos in solution.keys():
    assert solution[pos] == ground_assignment[pos], f'solution[{pos}] != ground_assignment[{pos}], {solution[pos]} != {ground_assignment[pos]}'

if __name__ == '__main__':
  test_ground()
