import numpy as np

from puzzle_solver import range_solver as solver
from puzzle_solver.core.utils import get_pos

def test_ground():
  # https://www.chiark.greenend.org.uk/~sgtatham/puzzles/js/range.html#16x11%23122854521237192
  clues = np.array([
    ['  ', '4 ', '2 ', '  ', '  ', '3 ', '  ', '  ', '  ', '8 ', '  ', '  ', '  ', '  ', '6 ', '  '],
    ['  ', '  ', '  ', '  ', '  ', '13', '  ', '18', '  ', '  ', '14', '  ', '  ', '22', '  ', '  '],
    ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '12', '  ', '  ', '  ', '  '],
    ['  ', '  ', '  ', '  ', '12', '  ', '11', '  ', '  ', '  ', '9 ', '  ', '  ', '  ', '  ', '  '],
    ['7 ', '  ', '  ', '  ', '  ', '  ', '6 ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  '],
    ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  '],
    ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '12', '  ', '  ', '  ', '  ', '  ', '5 '],
    ['  ', '  ', '  ', '  ', '  ', '9 ', '  ', '  ', '  ', '9 ', '  ', '4 ', '  ', '  ', '  ', '  '],
    ['  ', '  ', '  ', '  ', '6 ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  '],
    ['  ', '  ', '10', '  ', '  ', '7 ', '  ', '  ', '13', '  ', '10', '  ', '  ', '  ', '  ', '  '],
    ['  ', '7 ', '  ', '  ', '  ', '  ', '6 ', '  ', '  ', '  ', '6 ', '  ', '  ', '13', '5 ', '  '],
  ])
  binst = solver.Board(clues)
  solutions = binst.solve_and_print()
  ground = np.array([
    ['B', ' ', ' ', 'B', ' ', ' ', 'B', ' ', 'B', ' ', 'B', ' ', 'B', ' ', ' ', ' '],
    [' ', ' ', 'B', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'B'],
    ['B', ' ', ' ', ' ', ' ', 'B', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', 'B', ' ', 'B', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'B', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', 'B', ' ', ' ', 'B', ' ', 'B', ' ', ' ', ' ', 'B', ' '],
    [' ', ' ', 'B', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'B', ' ', ' ', ' ', 'B'],
    ['B', ' ', ' ', ' ', 'B', ' ', 'B', ' ', ' ', ' ', ' ', ' ', 'B', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', 'B', ' ', ' ', 'B', ' ', ' ', ' ', 'B', ' '],
    [' ', 'B', ' ', ' ', ' ', 'B', ' ', ' ', ' ', 'B', ' ', 'B', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', 'B', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'B'],
    ['B', ' ', ' ', ' ', ' ', ' ', ' ', 'B', ' ', ' ', ' ', ' ', 'B', ' ', ' ', ' '],
  ])
  assert len(solutions) == 1, f'unique solutions != 1, == {len(solutions)}'
  solution = solutions[0].assignment
  ground_assignment = {get_pos(x=x, y=y): 1 if ground[y][x] == 'B' else 0 for x in range(ground.shape[1]) for y in range(ground.shape[0])}
  assert set(solution.keys()) == set(ground_assignment.keys()), f'solution keys != ground assignment keys, {set(solution.keys()) ^ set(ground_assignment.keys())} \n\n\n{solution} \n\n\n{ground_assignment}'
  for pos in solution.keys():
    assert solution[pos] == ground_assignment[pos], f'solution[{pos}] != ground_assignment[{pos}], {solution[pos]} != {ground_assignment[pos]}'

def test_easy():
  # 5 x 5
  # https://www.puzzle-kurodoko.com/?e=MDoxLDYxMSwwNjE=
  clues = np.array([
    ['6', '2', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', '4'],
    [' ', ' ', ' ', ' ', ' '],
    ['5', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', '6', '3'],
  ])
  binst = solver.Board(clues)
  solutions = binst.solve_and_print()
  assert len(solutions) == 1, f'unique solutions != 1, == {len(solutions)}'
  solution = solutions[0].assignment
  ground = np.array([
    [' ', ' ', 'B', ' ', ' '],
    [' ', 'B', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', 'B'],
    [' ', 'B', ' ', ' ', ' '],
    [' ', ' ', 'B', ' ', ' '],
  ])
  ground_assignment = {get_pos(x=x, y=y): 1 if ground[y][x] == 'B' else 0 for x in range(ground.shape[1]) for y in range(ground.shape[0])}
  assert set(solution.keys()) == set(ground_assignment.keys()), f'solution keys != ground assignment keys, {set(solution.keys()) ^ set(ground_assignment.keys())} \n\n\n{solution} \n\n\n{ground_assignment}'
  for pos in solution.keys():
    assert solution[pos] == ground_assignment[pos], f'solution[{pos}] != ground_assignment[{pos}], {solution[pos]} != {ground_assignment[pos]}'


if __name__ == '__main__':
  test_ground()
  test_easy()
