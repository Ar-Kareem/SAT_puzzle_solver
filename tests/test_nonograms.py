import numpy as np

from puzzle_solver import nonograms_solver as solver
from puzzle_solver.core.utils import get_pos

# https://www.chiark.greenend.org.uk/~sgtatham/puzzles/js/pattern.html#15x15%23697217620427463
top_numbers = [
  [8, 2],
  [5, 4],
  [2, 1, 4],
  [2, 4],
  [2, 1, 4],
  [2, 5],
  [2, 8],
  [3, 2],
  [1, 6],
  [1, 9],
  [1, 6, 1],
  [1, 5, 3],
  [3, 2, 1],
  [4, 2],
  [1, 5],
]
side_numbers = [
  [7, 3],
  [7, 1, 1],
  [2, 3],
  [2, 3],
  [3, 2],
  [1, 1, 1, 1, 2],
  [1, 6, 1],
  [1, 9],
  [9],
  [2, 4],
  [8],
  [11],
  [7, 1, 1],
  [4, 3],
  [3, 2],
]
# top_numbers = [
#   -1,
#   -1,
#   -1,
#   -1,
#   -1,
# ]
# side_numbers = [
#   [2, 2],
# ]

def test_ground():
  binst = solver.Board(top=top_numbers, side=side_numbers)
  solutions = binst.solve_and_print()
  ground = np.array([
    ['B', 'B', 'B', 'B', 'B', 'B', 'B', ' ', 'B', 'B', 'B', ' ', ' ', ' ', ' '],
    ['B', 'B', 'B', 'B', 'B', 'B', 'B', ' ', ' ', ' ', ' ', ' ', 'B', ' ', 'B'],
    ['B', 'B', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'B', 'B', 'B', ' '],
    ['B', 'B', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'B', 'B', 'B'],
    ['B', 'B', 'B', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'B', 'B'],
    ['B', ' ', ' ', ' ', 'B', ' ', 'B', ' ', ' ', 'B', ' ', ' ', ' ', 'B', 'B'],
    ['B', ' ', ' ', ' ', ' ', ' ', 'B', 'B', 'B', 'B', 'B', 'B', ' ', ' ', 'B'],
    ['B', ' ', ' ', ' ', ' ', ' ', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B'],
    [' ', ' ', ' ', ' ', ' ', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', ' '],
    [' ', ' ', ' ', ' ', ' ', 'B', 'B', ' ', 'B', 'B', 'B', 'B', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', ' ', ' ', ' '],
    ['B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', ' ', ' ', ' ', ' '],
    ['B', 'B', 'B', 'B', 'B', 'B', 'B', ' ', ' ', 'B', ' ', 'B', ' ', ' ', ' '],
    [' ', 'B', 'B', 'B', 'B', ' ', ' ', ' ', ' ', 'B', 'B', 'B', ' ', ' ', ' '],
    [' ', 'B', 'B', 'B', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'B', 'B', ' ', ' '],
  ], dtype=object)

  assert len(solutions) == 1, f'unique solutions != 1, == {len(solutions)}'
  solution = solutions[0].assignment
  ground_assignment = {get_pos(x=x, y=y): 1 if ground[y][x] == 'B' else 0 for x in range(ground.shape[1]) for y in range(ground.shape[0])}
  assert set(solution.keys()) == set(ground_assignment.keys()), f'solution keys != ground assignment keys, {set(solution.keys())} != {set(ground_assignment.keys())}'
  for pos in solution.keys():
    assert solution[pos] == ground_assignment[pos], f'solution[{pos}] != ground_assignment[{pos}], {solution[pos]} != {ground_assignment[pos]}'

if __name__ == '__main__':
  test_ground()
