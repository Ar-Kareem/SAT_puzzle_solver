import numpy as np

from puzzle_solver import pearl_solver as solver
from puzzle_solver.core.utils import get_pos

# https://www.chiark.greenend.org.uk/~sgtatham/puzzles/js/pearl.html#12x8dt%23105305052653698
bor = np.array([
  ['B', ' ', ' ', 'W', ' ', ' ', 'W', ' ', 'B', ' ', ' ', 'B'],
  [' ', ' ', ' ', 'B', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
  [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'B', ' ', ' ', ' '],
  [' ', 'B', ' ', 'B', ' ', 'W', ' ', 'B', ' ', 'B', 'W', ' '],
  [' ', ' ', 'B', ' ', 'B', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
  [' ', ' ', ' ', ' ', ' ', ' ', ' ', 'W', 'W', ' ', ' ', 'B'],
  [' ', ' ', 'B', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
  ['B', ' ', ' ', ' ', ' ', 'B', 'B', ' ', ' ', ' ', ' ', 'B'],
])

def test_ground():
  binst = solver.Board(bor)
  solutions = binst.solve_and_print()
  ground = np.array([
    ['DR', 'LR', 'LR', 'LR', 'DL', 'DR', 'LR', 'DL', 'DR', 'LR', 'LR', 'DL'],
    ['DU', 'DR', 'LR', 'DL', 'RU', 'LU', 'DR', 'LU', 'DU', 'DR', 'DL', 'DU'],
    ['RU', 'LU', '  ', 'DU', 'DR', 'DL', 'RU', 'LR', 'LU', 'DU', 'DU', 'DU'],
    ['  ', 'DR', 'LR', 'LU', 'DU', 'DU', '  ', 'DR', 'LR', 'LU', 'DU', 'DU'],
    ['  ', 'DU', 'DR', 'LR', 'LU', 'RU', 'DL', 'DU', 'DR', 'DL', 'RU', 'LU'],
    ['DR', 'LU', 'DU', '  ', 'DR', 'DL', 'DU', 'DU', 'DU', 'RU', 'LR', 'DL'],
    ['DU', '  ', 'RU', 'LR', 'LU', 'DU', 'DU', 'RU', 'LU', '  ', '  ', 'DU'],
    ['RU', 'LR', 'LR', 'LR', 'LR', 'LU', 'RU', 'LR', 'LR', 'LR', 'LR', 'LU'],
  ])
  assert len(solutions) == 1, f'unique solutions != 1, == {len(solutions)}'
  solution = solutions[0].assignment
  ground_assignment = {get_pos(x=x, y=y): ground[y][x] for x in range(ground.shape[1]) for y in range(ground.shape[0])}
  assert set(solution.keys()) == set(ground_assignment.keys()), f'solution keys != ground assignment keys, {set(solution.keys()) ^ set(ground_assignment.keys())} \n\n\n{solution} \n\n\n{ground_assignment}'
  for pos in solution.keys():
    assert solution[pos] == ground_assignment[pos], f'solution[{pos}] != ground_assignment[{pos}], {solution[pos]} != {ground_assignment[pos]}'

if __name__ == '__main__':
  test_ground()
