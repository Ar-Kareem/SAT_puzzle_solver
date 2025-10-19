

import numpy as np

from puzzle_solver import thermometers_solver as solver
from puzzle_solver.core.utils import get_pos


def test_ground():
  # https://www.puzzle-thermometers.com/?e=Nzo5LDU5Miw2MDU=
  board = np.array([
    ['R', 'R', 'D', 'R', 'D', 'R', 'X', 'D', 'L', 'X', 'L', 'L', 'L', 'L', 'L'],
    ['D', 'D', 'D', 'U', 'X', 'U', 'X', 'R', 'R', 'R', 'R', 'D', 'D', 'R', 'U'],
    ['D', 'D', 'D', 'U', 'X', 'U', 'U', 'R', 'R', 'R', 'X', 'D', 'D', 'D', 'D'],
    ['X', 'D', 'D', 'U', 'U', 'U', 'L', 'U', 'R', 'R', 'D', 'X', 'D', 'X', 'X'],
    ['X', 'D', 'D', 'U', 'U', 'R', 'R', 'R', 'R', 'X', 'R', 'X', 'D', 'R', 'X'],
    ['U', 'D', 'D', 'U', 'U', 'R', 'X', 'R', 'R', 'R', 'R', 'D', 'D', 'R', 'D'],
    ['U', 'D', 'D', 'R', 'R', 'X', 'R', 'R', 'R', 'R', 'D', 'D', 'R', 'X', 'D'],
    ['U', 'D', 'D', 'U', 'X', 'L', 'X', 'L', 'R', 'X', 'X', 'R', 'X', 'X', 'L'],
    ['U', 'D', 'D', 'R', 'X', 'U', 'L', 'L', 'L', 'L', 'L', 'L', 'L', 'L', 'L'],
    ['X', 'D', 'X', 'U', 'R', 'R', 'R', 'R', 'R', 'R', 'R', 'R', 'R', 'D', 'U'],
    ['U', 'D', 'X', 'U', 'R', 'R', 'X', 'R', 'R', 'R', 'R', 'X', 'X', 'L', 'U'],
    ['U', 'R', 'U', 'U', 'R', 'X', 'R', 'X', 'R', 'X', 'R', 'R', 'R', 'R', 'U'],
    ['U', 'R', 'X', 'R', 'R', 'R', 'R', 'R', 'R', 'R', 'R', 'R', 'X', 'X', 'L'],
    ['U', 'U', 'R', 'R', 'X', 'D', 'R', 'R', 'D', 'R', 'X', 'X', 'L', 'L', 'U'],
    ['U', 'U', 'U', 'L', 'L', 'R', 'X', 'X', 'L', 'U', 'R', 'R', 'R', 'U', 'U'],
  ])
  top = np.array([7, 4, 12, 8, 4, 6, 5, 7, 5, 4, 8, 9, 13, 8, 12])
  side = np.array([8, 10, 9, 10, 6, 10, 4, 6, 6, 10, 5, 7, 6, 6, 9])
  binst = solver.Board(board=board, top=top, side=side)
  solutions = binst.solve_and_print()
  assert len(solutions) == 1, f'unique solutions != 1, == {len(solutions)}'
  solution = solutions[0].assignment
  ground = np.array([
    ['X', 'X', 'X', ' ', ' ', ' ', ' ', 'X', 'X', ' ', ' ', ' ', 'X', 'X', 'X'],
    ['X', ' ', 'X', ' ', ' ', ' ', ' ', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X'],
    ['X', ' ', 'X', 'X', ' ', 'X', 'X', 'X', ' ', ' ', ' ', 'X', 'X', ' ', 'X'],
    [' ', ' ', 'X', 'X', ' ', 'X', 'X', 'X', 'X', 'X', 'X', ' ', 'X', ' ', 'X'],
    [' ', ' ', 'X', 'X', ' ', ' ', ' ', ' ', ' ', ' ', 'X', ' ', 'X', 'X', 'X'],
    [' ', ' ', 'X', 'X', ' ', ' ', ' ', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X'],
    [' ', ' ', 'X', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'X', 'X', ' ', 'X'],
    [' ', ' ', 'X', ' ', ' ', ' ', 'X', 'X', ' ', ' ', ' ', 'X', 'X', ' ', 'X'],
    [' ', ' ', 'X', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'X', 'X', 'X', 'X', 'X'],
    [' ', ' ', ' ', ' ', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', ' ', 'X'],
    [' ', ' ', ' ', 'X', 'X', 'X', 'X', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'X'],
    ['X', ' ', ' ', 'X', ' ', ' ', ' ', ' ', ' ', ' ', 'X', 'X', 'X', 'X', 'X'],
    ['X', 'X', 'X', 'X', 'X', 'X', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    ['X', 'X', 'X', ' ', ' ', 'X', ' ', ' ', ' ', ' ', ' ', ' ', 'X', 'X', ' '],
    ['X', 'X', 'X', 'X', 'X', ' ', ' ', ' ', ' ', ' ', 'X', 'X', 'X', 'X', ' '],
  ])
  ground_assignment = {get_pos(x=x, y=y): 1 if ground[y][x] == 'X' else 0 for x in range(ground.shape[1]) for y in range(ground.shape[0])}
  assert set(solution.keys()) == set(ground_assignment.keys()), f'solution keys != ground assignment keys, {set(solution.keys()) ^ set(ground_assignment.keys())} \n\n\n{solution} \n\n\n{ground_assignment}'
  for pos in solution.keys():
    assert solution[pos] == ground_assignment[pos], f'solution[{pos}] != ground_assignment[{pos}], {solution[pos]} != {ground_assignment[pos]}'
if __name__ == '__main__':
  test_ground()
