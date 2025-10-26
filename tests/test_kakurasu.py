import numpy as np

from puzzle_solver import kakurasu_solver as solver
from puzzle_solver.core.utils import get_pos


def test_ground_1():
  # https://www.puzzle-kakurasu.com/?e=MDo2NzQsNjYx
  side = np.array([6, 1, 2, 5])
  bottom = np.array([2, 8, 4, 1])
  binst = solver.Board(side=side, bottom=bottom)
  solutions = binst.solve_and_print()
  assert len(solutions) == 1, f'unique solutions != 1, == {len(solutions)}'
  solution = solutions[0].assignment
  ground = np.array([
    [0, 1, 0, 1],
    [1, 0, 0, 0],
    [0, 1, 0, 0],
    [0, 1, 1, 0],
  ])
  ground_assignment = {get_pos(x=x, y=y): ground[y][x] for x in range(ground.shape[1]) for y in range(ground.shape[0])}
  assert set(solution.keys()) == set(ground_assignment.keys()), f'solution keys != ground assignment keys, {set(solution.keys()) ^ set(ground_assignment.keys())} \n\n\n{solution} \n\n\n{ground_assignment}'
  for pos in solution.keys():
    assert solution[pos] == ground_assignment[pos], f'solution[{pos}] != ground_assignment[{pos}], {solution[pos]} != {ground_assignment[pos]}'

def test_ground_2():
  # monthly, oct 2025, https://www.puzzle-kakurasu.com/?pl=f686e1e6767cad5da493e4bfde80250d68f5ced31da3d
  side = np.array([27, 6, 1, 12, 37, 37, 11, 4, 29, 23, 66, 55])
  bottom = np.array([22, 1, 25, 36, 10, 22, 25, 35, 32, 28, 45, 45])
  binst = solver.Board(side=side, bottom=bottom)
  solutions = binst.solve_and_print()
  assert len(solutions) == 1, f'unique solutions != 1, == {len(solutions)}'
  solution = solutions[0].assignment
  ground = np.array([
    ['X', 'X', ' ', 'X', ' ', ' ', ' ', 'X', ' ', ' ', ' ', 'X'],
    [' ', ' ', ' ', ' ', ' ', 'X', ' ', ' ', ' ', ' ', ' ', ' '],
    ['X', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', 'X', ' ', 'X', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', 'X', 'X', ' ', ' ', ' ', 'X', ' ', 'X', ' ', 'X'],
    ['X', ' ', ' ', ' ', 'X', ' ', ' ', 'X', ' ', ' ', 'X', 'X'],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'X', ' '],
    [' ', ' ', ' ', 'X', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', 'X', ' ', ' ', 'X', ' ', ' ', 'X', ' ', 'X', ' '],
    [' ', ' ', ' ', 'X', ' ', ' ', 'X', ' ', ' ', ' ', ' ', 'X'],
    [' ', ' ', 'X', ' ', ' ', 'X', 'X', 'X', 'X', 'X', 'X', 'X'],
    ['X', ' ', ' ', 'X', ' ', ' ', ' ', 'X', 'X', 'X', 'X', 'X'],
  ])
  ground_assignment = {get_pos(x=x, y=y): 1 if ground[y][x] == 'X' else 0 for x in range(ground.shape[1]) for y in range(ground.shape[0])}
  assert set(solution.keys()) == set(ground_assignment.keys()), f'solution keys != ground assignment keys, {set(solution.keys()) ^ set(ground_assignment.keys())} \n\n\n{solution} \n\n\n{ground_assignment}'
  for pos in solution.keys():
    assert solution[pos] == ground_assignment[pos], f'solution[{pos}] != ground_assignment[{pos}], {solution[pos]} != {ground_assignment[pos]}'


if __name__ == '__main__':
  test_ground_1()
  test_ground_2()
