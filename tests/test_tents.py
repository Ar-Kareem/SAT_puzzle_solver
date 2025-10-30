import numpy as np

from puzzle_solver import tents_solver as solver
from puzzle_solver.core.utils import get_pos


def test_ground():
  # https://www.chiark.greenend.org.uk/~sgtatham/puzzles/js/tents.html#15x15dt%23727673714482646
  board = np.array([
    [' ', 'T', ' ', ' ', ' ', ' ', ' ', ' ', 'T', ' ', 'T', ' ', 'T', ' ', ' '],
    [' ', ' ', ' ', ' ', 'T', ' ', ' ', 'T', ' ', 'T', ' ', ' ', 'T', ' ', ' '],
    [' ', 'T', ' ', 'T', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'T', ' ', ' ', ' ', 'T', ' ', 'T'],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', 'T', ' ', ' ', 'T', ' ', 'T', ' ', ' ', 'T', ' ', ' ', 'T', 'T', ' '],
    [' ', 'T', ' ', ' ', 'T', ' ', ' ', ' ', 'T', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', 'T', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', 'T', ' ', ' ', ' ', ' ', 'T', ' ', ' ', 'T', ' '],
    [' ', ' ', ' ', 'T', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'T', ' ', 'T'],
    ['T', ' ', ' ', ' ', ' ', ' ', ' ', 'T', ' ', ' ', ' ', 'T', ' ', ' ', ' '],
    ['T', ' ', ' ', ' ', 'T', ' ', 'T', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'T', ' ', 'T', ' ', ' ', ' ', 'T'],
    [' ', 'T', ' ', ' ', ' ', 'T', ' ', ' ', ' ', ' ', ' ', ' ', 'T', ' ', ' '],
    [' ', 'T', ' ', ' ', 'T', ' ', ' ', ' ', ' ', 'T', ' ', 'T', ' ', ' ', ' '],
  ])
  side = np.array([4, 1, 6, 0, 5, 2, 3, 1, 5, 2, 3, 2, 4, 3, 4])
  top = np.array([4, 2, 4, 1, 3, 3, 3, 3, 3, 3, 2, 2, 6, 2, 4])

  binst = solver.Board(board=board, top=top, side=side)
  solutions = binst.solve_and_print()
  ground = np.array([
    [' ', 'T', 'E', ' ', ' ', ' ', ' ', 'E', 'T', ' ', 'T', 'E', 'T', 'E', ' '],
    [' ', ' ', ' ', ' ', 'T', 'E', ' ', 'T', ' ', 'T', ' ', ' ', 'T', ' ', ' '],
    ['E', 'T', 'E', 'T', ' ', ' ', ' ', 'E', ' ', 'E', ' ', ' ', 'E', ' ', 'E'],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'T', ' ', ' ', ' ', 'T', ' ', 'T'],
    [' ', 'E', ' ', ' ', 'E', ' ', 'E', ' ', 'E', ' ', ' ', ' ', 'E', ' ', ' '],
    [' ', 'T', ' ', ' ', 'T', ' ', 'T', ' ', ' ', 'T', 'E', ' ', 'T', 'T', 'E'],
    [' ', 'T', ' ', ' ', 'T', 'E', ' ', 'E', 'T', ' ', ' ', ' ', 'E', ' ', ' '],
    [' ', 'E', ' ', ' ', ' ', ' ', 'T', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', 'E', 'T', 'E', ' ', ' ', 'E', 'T', ' ', 'E', 'T', 'E'],
    ['E', ' ', 'E', 'T', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'T', ' ', 'T'],
    ['T', ' ', ' ', ' ', ' ', ' ', ' ', 'T', 'E', ' ', ' ', 'T', 'E', ' ', 'E'],
    ['T', ' ', ' ', 'E', 'T', 'E', 'T', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    ['E', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'T', 'E', 'T', 'E', ' ', 'E', 'T'],
    [' ', 'T', 'E', ' ', 'E', 'T', 'E', ' ', ' ', ' ', ' ', ' ', 'T', ' ', ' '],
    ['E', 'T', ' ', ' ', 'T', ' ', ' ', ' ', 'E', 'T', 'E', 'T', 'E', ' ', ' '],
  ])
  assert len(solutions) == 1, f'unique solutions != 1, == {len(solutions)}'
  solution = solutions[0].assignment
  ground_assignment = {get_pos(x=x, y=y): 1 if ground[y][x] == 'E' else 0 for x in range(ground.shape[1]) for y in range(ground.shape[0]) if ground[y][x] in [' ', 'E']}
  assert set(solution.keys()) == set(ground_assignment.keys()), f'solution keys != ground assignment keys, {set(solution.keys()) ^ set(ground_assignment.keys())} \n\n\n{solution} \n\n\n{ground_assignment}'
  for pos in solution.keys():
    assert solution[pos] == ground_assignment[pos], f'solution[{pos}] != ground_assignment[{pos}], {solution[pos]} != {ground_assignment[pos]}'


def test_dummy():
  board = np.array([
    [' ', ' ', ' '],
    [' ', ' ', 'T'],
    [' ', ' ', ' '],
    [' ', ' ', ' '],
    [' ', ' ', 'T'],
  ])
  top = np.array([0, 0, 2])
  side = np.array([-1, -1, -1, -1, -1])
  binst = solver.Board(board=board, top=top, side=side)
  solutions = binst.solve_and_print()
  ground = np.array([
    [' ', ' ', 'E'],
    [' ', ' ', 'T'],
    [' ', ' ', ' '],
    [' ', ' ', 'E'],
    [' ', ' ', 'T'],
  ])
  assert len(solutions) == 1, f'unique solutions != 1, == {len(solutions)}'
  solution = solutions[0].assignment
  ground_assignment = {get_pos(x=x, y=y): 1 if ground[y][x] == 'E' else 0 for x in range(ground.shape[1]) for y in range(ground.shape[0]) if ground[y][x] in [' ', 'E']}
  assert set(solution.keys()) == set(ground_assignment.keys()), f'solution keys != ground assignment keys, {set(solution.keys()) ^ set(ground_assignment.keys())} \n\n\n{solution} \n\n\n{ground_assignment}'
  for pos in solution.keys():
    assert solution[pos] == ground_assignment[pos], f'solution[{pos}] != ground_assignment[{pos}], {solution[pos]} != {ground_assignment[pos]}'

if __name__ == '__main__':
  test_dummy()
  test_ground()
