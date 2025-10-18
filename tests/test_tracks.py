import numpy as np

from puzzle_solver import tracks_solver as solver
from puzzle_solver.core.utils import get_pos

# https://www.chiark.greenend.org.uk/~sgtatham/puzzles/js/tracks.html#15x15dh%23872777330479824
# U L D R
board = np.array([
  # 6     5     7     3      3     2    7     8     13    8     9     8     10    13    14
  ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', 'LD', '  ', '  ', ], 
  ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', 'LD', '  ', '  ', '  ', '  ', ], 
  ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', ], 
  ['  ', '  ', '  ', '  ', '  ', 'LD', 'UD', 'DR', '  ', '  ', '  ', '  ', '  ', '  ', '  ', ], 
  ['DR', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', ], 
  ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', 'DR', '  ', '  ', ], 
  ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', 'DR', '  ', '  ', '  ', '  ', '  ', '  ', ], 
  ['  ', '  ', 'UL', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', ], 
  ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', 'LR', '  ', '  ', '  ', '  ', ], 
  ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', 'LD', '  ', '  ', '  ', 'UD', ], 
  ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', 'UR', '  ', '  ', '  ', '  ', 'UD', 'UD', ], 
  ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', 'LR', '  ', '  ', '  ', '  ', '  ', ], 
  ['UL', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', 'LR', 'LR', '  ', '  ', '  ', ], 
  ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', ], 
  ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', 'DR', '  ', ], 
])
side = np.array([9, 7, 7, 7, 11, 10, 9, 8, 9, 10, 7, 9, 9, 2, 2])
top = np.array([6, 5, 7, 3, 3, 2, 7, 8, 13, 8, 9, 8, 10, 13, 14])

# board = np.array([
#   ['LR', '  ', '  ', '  ', '  ', '  ', '  ', '  '], 
#   ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  '], 
#   ['UD', '  ', '  ', '  ', '  ', '  ', '  ', '  '], 
#   ['  ', '  ', '  ', '  ', 'LD', '  ', '  ', '  '], 
#   ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  '], 
#   ['  ', '  ', 'UD', '  ', '  ', '  ', '  ', 'UD'], 
#   ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  '], 
#   ['  ', '  ', 'DR', '  ', '  ', '  ', 'UR', '  '], 
# ])
# side = np.array([5, 6, 5, 8, 6, 7, 5, 6])
# top = np.array([4, 6, 5, 6, 6, 7, 6, 8])


def test_ground():
  binst = solver.Board(board=board, top=top, side=side)
  solutions = binst.solve_and_print()
  ground = np.array([
    ['  ', '  ', '  ', '  ', '  ', '  ', 'DR', 'LR', 'LR', 'LR', 'LR', 'LR', 'DL', 'DR', 'DL'],
    ['  ', '  ', '  ', '  ', '  ', '  ', 'DU', '  ', 'DR', 'LR', 'DL', '  ', 'RU', 'LU', 'DU'],
    ['  ', '  ', '  ', '  ', '  ', '  ', 'DU', '  ', 'DU', '  ', 'RU', 'LR', 'LR', 'LR', 'LU'],
    ['  ', '  ', 'DR', 'DL', 'DR', 'DL', 'DU', 'DR', 'LU', '  ', '  ', '  ', '  ', '  ', '  '],
    ['DR', 'LR', 'LU', 'DU', 'DU', 'RU', 'LU', 'RU', 'DL', '  ', '  ', '  ', '  ', 'DR', 'DL'],
    ['RU', 'LR', 'DL', 'RU', 'LU', '  ', '  ', 'DR', 'LU', '  ', '  ', '  ', 'DR', 'LU', 'DU'],
    ['  ', '  ', 'DU', '  ', '  ', '  ', 'DR', 'LU', 'DR', 'LR', 'LR', 'LR', 'LU', '  ', 'DU'],
    ['  ', 'DR', 'LU', '  ', '  ', '  ', 'RU', 'LR', 'LU', '  ', '  ', '  ', 'DR', 'LR', 'LU'],
    ['  ', 'RU', 'DL', '  ', '  ', '  ', '  ', '  ', 'DR', 'LR', 'LR', 'DL', 'DU', 'DR', 'DL'],
    ['DR', 'LR', 'LU', '  ', '  ', '  ', '  ', '  ', 'DU', 'DR', 'DL', 'RU', 'LU', 'DU', 'DU'],
    ['DU', '  ', '  ', '  ', '  ', '  ', '  ', '  ', 'RU', 'LU', 'RU', 'DL', '  ', 'DU', 'DU'],
    ['DU', '  ', '  ', '  ', '  ', '  ', '  ', 'DR', 'LR', 'LR', 'LR', 'LU', 'DR', 'LU', 'DU'],
    ['LU', '  ', '  ', '  ', '  ', '  ', '  ', 'RU', 'LR', 'LR', 'LR', 'LR', 'LU', 'DR', 'LU'],
    ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', 'RU', 'DL'],
    ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', 'DR', 'LU'],
  ])
  assert len(solutions) == 1, f'unique solutions != 1, == {len(solutions)}'
  solution = solutions[0].assignment
  ground_assignment = {get_pos(x=x, y=y): ground[y][x] for x in range(ground.shape[1]) for y in range(ground.shape[0])}
  assert set(solution.keys()) == set(ground_assignment.keys()), f'solution keys != ground assignment keys, {set(solution.keys()) ^ set(ground_assignment.keys())} \n\n\n{solution} \n\n\n{ground_assignment}'
  for pos in solution.keys():
    assert solution[pos] == ground_assignment[pos], f'solution[{pos}] != ground_assignment[{pos}], {solution[pos]} != {ground_assignment[pos]}'

if __name__ == '__main__':
  test_ground()
