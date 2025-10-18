import numpy as np

from puzzle_solver import light_solver as solver
from puzzle_solver.core.utils import get_pos

# https://www.chiark.greenend.org.uk/~sgtatham/puzzles/js/lightup.html#10x10b20s2d2%23436435953565512
bor = np.array([
  ['*', '0', '*', '*', '*', '*', 'W', '*', '*', '*'],
  ['*', '*', '*', '0', '*', '*', '*', '*', '*', '1'],
  ['W', '*', 'W', '*', '*', 'W', '*', '*', '0', '*'],
  ['0', '*', '*', '*', '3', '*', 'W', '*', '0', '*'],
  ['*', '*', '*', '*', 'W', '*', '2', '*', 'W', '*'],
  ['*', '1', '*', 'W', '*', '2', '*', '*', '*', '*'],
  ['*', '0', '*', 'W', '*', 'W', '*', '*', '*', 'W'],
  ['*', '0', '*', '*', '1', '*', '*', '2', '*', 'W'],
  ['0', '*', '*', '*', '*', '*', '1', '*', '*', '*'],
  ['*', '*', '*', '2', '*', '*', '*', '*', 'W', '*'],
])


def test_ground():
  binst = solver.Board(board=bor)
  solutions = binst.solve_and_print()
  ground = np.array([
    ['S', '0', 'S', 'S', 'S', 'L', 'W', 'S', 'S', 'L'],
    ['L', 'S', 'S', '0', 'S', 'S', 'L', 'S', 'S', '1'],
    ['W', 'L', 'W', 'S', 'L', 'W', 'S', 'S', '0', 'S'],
    ['0', 'S', 'S', 'L', '3', 'L', 'W', 'S', '0', 'S'],
    ['S', 'S', 'L', 'S', 'W', 'S', '2', 'L', 'W', 'L'],
    ['L', '1', 'S', 'W', 'L', '2', 'L', 'S', 'S', 'S'],
    ['S', '0', 'S', 'W', 'S', 'W', 'S', 'S', 'S', 'W'],
    ['S', '0', 'S', 'S', '1', 'L', 'S', '2', 'L', 'W'],
    ['0', 'S', 'S', 'L', 'S', 'S', '1', 'L', 'S', 'S'],
    ['S', 'L', 'S', '2', 'L', 'S', 'S', 'S', 'W', 'L'],
  ])
  print(ground, ground.shape)
  assert len(solutions) == 1, f'unique solutions != 1, == {len(solutions)}'
  solution = solutions[0].assignment
  ground_assignment = {get_pos(x=x, y=y): ground[y][x] for x in range(ground.shape[1]) for y in range(ground.shape[0]) if ground[y][x] in ['S', 'L']}
  assert set(solution.keys()) == set(ground_assignment.keys()), f'solution keys != ground assignment keys, {set(solution.keys()) ^ set(ground_assignment.keys())} \n\n\n{solution} \n\n\n{ground_assignment}'
  for pos in solution.keys():
    assert solution[pos] == ground_assignment[pos], f'solution[{pos}] != ground_assignment[{pos}], {solution[pos]} != {ground_assignment[pos]}'

if __name__ == '__main__':
  test_ground()
