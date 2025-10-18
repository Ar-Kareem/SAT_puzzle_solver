import numpy as np

from puzzle_solver import dominosa_solver as solver
from puzzle_solver.core.utils import get_pos

# https://www.chiark.greenend.org.uk/~sgtatham/puzzles/js/dominosa.html#9db%23801628305305591
board = np.array([
  [6, 8, 2, 7, 1, 3, 3, 4, 6, 6, 0],
  [4, 9, 5, 6, 1, 0, 6, 1, 2, 2, 4],
  [8, 2, 8, 9, 1, 9, 3, 3, 8, 8, 5],
  [1, 1, 7, 3, 4, 7, 0, 8, 7, 7, 7],
  [4, 5, 3, 9, 9, 3, 0, 1, 6, 1, 5],
  [6, 9, 5, 8, 9, 2, 1, 2, 6, 7, 9],
  [2, 7, 4, 3, 5, 5, 9, 6, 4, 0, 9],
  [0, 7, 8, 0, 5, 4, 2, 7, 6, 7, 3],
  [0, 4, 5, 2, 8, 6, 1, 0, 9, 0, 4],
  [0, 8, 8, 3, 2, 1, 3, 2, 5, 5, 4],
])

def test_ground():
  binst = solver.Board(board=board)
  solutions = binst.solve_and_print()
  ground = np.array([
    ['R', 'L', 'R', 'L', 'D', 'R', 'L', 'R', 'L', 'R', 'L'],
    ['D', 'D', 'R', 'L', 'U', 'D', 'D', 'D', 'R', 'L', 'D'],
    ['U', 'U', 'D', 'R', 'L', 'U', 'U', 'U', 'R', 'L', 'U'],
    ['D', 'D', 'U', 'D', 'D', 'R', 'L', 'D', 'R', 'L', 'D'],
    ['U', 'U', 'D', 'U', 'U', 'R', 'L', 'U', 'D', 'D', 'U'],
    ['D', 'D', 'U', 'R', 'L', 'D', 'R', 'L', 'U', 'U', 'D'],
    ['U', 'U', 'R', 'L', 'D', 'U', 'R', 'L', 'R', 'L', 'U'],
    ['D', 'D', 'D', 'D', 'U', 'R', 'L', 'R', 'L', 'R', 'L'],
    ['U', 'U', 'U', 'U', 'D', 'D', 'R', 'L', 'D', 'D', 'D'],
    ['R', 'L', 'R', 'L', 'U', 'U', 'R', 'L', 'U', 'U', 'U'],
  ])
  assert len(solutions) == 1, f'unique solutions != 1, == {len(solutions)}'
  solution = solutions[0].assignment
  d = {'U': 1, 'D': 2, 'L': 3, 'R': 4}
  ground_assignment = {get_pos(x=x, y=y): d[ground[y][x]] for x in range(ground.shape[1]) for y in range(ground.shape[0])}
  assert set(solution.keys()) == set(ground_assignment.keys()), f'solution keys != ground assignment keys, {set(solution.keys())} != {set(ground_assignment.keys())}'
  for pos in solution.keys():
    assert solution[pos] == ground_assignment[pos], f'solution[{pos}] != ground_assignment[{pos}], {solution[pos]} != {ground_assignment[pos]}'

if __name__ == '__main__':
  test_ground()
