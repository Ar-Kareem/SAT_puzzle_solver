import numpy as np

from puzzle_solver import yin_yang_solver as solver
from puzzle_solver.core.utils import get_pos


def test_ground():
  board = np.array([
    [' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', 'W', ' ', ' '],
    [' ', ' ', 'W', ' ', 'B', ' '],
    [' ', ' ', ' ', 'B', ' ', ' '],
    [' ', 'W', ' ', ' ', 'W', ' '],
    ['B', 'W', ' ', 'W', ' ', 'B'],
  ])
  binst = solver.Board(board=board)
  solutions = binst.solve_and_print()
  assert len(solutions) == 1, f'unique solutions != 1, == {len(solutions)}'
  solution = solutions[0].assignment
  ground = np.array([
    ['B', 'B', 'B', 'B', 'B', 'B'],
    ['B', 'W', 'W', 'W', 'W', 'B'],
    ['B', 'B', 'W', 'B', 'B', 'B'],
    ['B', 'W', 'W', 'B', 'W', 'B'],
    ['B', 'W', 'B', 'B', 'W', 'B'],
    ['B', 'W', 'W', 'W', 'W', 'B'],
  ])
  ground_assignment = {get_pos(x=x, y=y): ground[y][x] for x in range(ground.shape[1]) for y in range(ground.shape[0])}
  assert set(solution.keys()) == set(ground_assignment.keys()), f'solution keys != ground assignment keys, {set(solution.keys()) ^ set(ground_assignment.keys())} \n\n\n{solution} \n\n\n{ground_assignment}'
  for pos in solution.keys():
    assert solution[pos] == ground_assignment[pos], f'solution[{pos}] != ground_assignment[{pos}], {solution[pos]} != {ground_assignment[pos]}'


def test_ground_2():
  # 20 x 20 example
  # https://www.puzzle-yin-yang.com/?e=MTE6Niw0NjEsMTIx
  board = np.array([
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', 'W', ' ', ' ', ' ', 'B', ' ', ' ', 'W', ' ', 'W', ' ', ' ', 'W', ' ', ' '],
    [' ', ' ', 'B', ' ', 'B', ' ', 'W', ' ', ' ', 'W', 'B', ' ', ' ', ' ', ' ', 'W', ' ', 'W', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', 'W', ' ', 'W', ' ', 'B', ' ', ' ', ' ', ' ', 'W', ' ', ' ', 'W', ' ', ' '],
    [' ', 'W', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'W', 'W', ' ', ' ', ' ', ' ', ' ', ' ', 'W', ' ', ' '],
    [' ', ' ', ' ', ' ', 'W', ' ', ' ', ' ', 'W', 'B', ' ', ' ', ' ', ' ', ' ', 'W', ' ', 'W', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', 'W', ' ', ' ', ' ', ' ', 'B', ' ', 'B', ' ', 'B', 'W', ' ', 'W', ' ', ' '],
    [' ', ' ', 'B', 'W', 'W', ' ', 'W', ' ', ' ', ' ', 'B', ' ', 'B', ' ', 'B', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'B', ' ', 'B', ' ', 'B', ' ', 'B', ' ', 'B', ' ', 'B', ' '],
    [' ', 'W', ' ', 'W', ' ', ' ', 'W', ' ', ' ', ' ', 'B', ' ', 'B', ' ', 'B', ' ', 'B', ' ', 'B', ' '],
    [' ', ' ', ' ', ' ', 'W', 'B', ' ', ' ', ' ', 'B', ' ', ' ', 'B', ' ', 'B', ' ', 'B', ' ', 'B', ' '],
    [' ', ' ', 'B', ' ', ' ', ' ', 'B', 'B', ' ', 'W', 'B', ' ', 'B', ' ', 'B', ' ', ' ', 'B', ' ', ' '],
    [' ', 'W', 'W', 'W', ' ', 'B', ' ', 'W', ' ', ' ', 'B', ' ', 'B', ' ', 'B', ' ', ' ', ' ', 'B', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', 'W', ' ', ' ', 'B', ' ', 'B', ' ', ' ', 'B', ' ', 'B', ' ', 'B', ' '],
    [' ', 'W', ' ', 'B', 'W', 'B', ' ', 'W', ' ', ' ', ' ', ' ', 'B', 'B', ' ', ' ', 'B', ' ', 'B', ' '],
    [' ', ' ', ' ', ' ', 'W', ' ', ' ', 'B', 'B', 'B', 'B', 'B', ' ', ' ', ' ', 'B', ' ', ' ', 'B', ' '],
    [' ', 'W', ' ', ' ', ' ', 'W', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'B', ' ', 'B', ' '],
    ['W', ' ', ' ', 'W', ' ', ' ', 'B', ' ', ' ', 'B', 'B', 'B', 'B', 'B', ' ', ' ', 'B', ' ', 'B', ' '],
    [' ', 'W', 'W', ' ', 'W', ' ', ' ', 'B', ' ', ' ', ' ', ' ', ' ', ' ', 'B', ' ', 'B', ' ', 'B', ' '],
    ['B', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'B', 'W']
  ])
  binst = solver.Board(board=board)
  solutions = binst.solve_and_print()
  assert len(solutions) == 1, f'unique solutions != 1, == {len(solutions)}'
  solution = solutions[0].assignment
  ground = np.array([
    [ 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W' ],
    [ 'W', 'B', 'B', 'W', 'B', 'W', 'B', 'B', 'B', 'B', 'B', 'B', 'W', 'B', 'W', 'B', 'B', 'W', 'B', 'W' ],
    [ 'W', 'W', 'B', 'W', 'B', 'W', 'W', 'W', 'W', 'W', 'B', 'W', 'W', 'B', 'W', 'W', 'B', 'W', 'B', 'W' ],
    [ 'W', 'B', 'B', 'B', 'B', 'W', 'B', 'W', 'B', 'B', 'B', 'B', 'B', 'B', 'W', 'B', 'B', 'W', 'B', 'W' ],
    [ 'W', 'W', 'W', 'B', 'W', 'W', 'B', 'W', 'W', 'W', 'W', 'W', 'B', 'W', 'W', 'W', 'B', 'W', 'B', 'W' ],
    [ 'W', 'B', 'W', 'B', 'W', 'B', 'B', 'B', 'W', 'B', 'B', 'W', 'B', 'W', 'B', 'W', 'B', 'W', 'B', 'W' ],
    [ 'W', 'B', 'B', 'B', 'W', 'W', 'W', 'B', 'W', 'W', 'B', 'W', 'B', 'W', 'B', 'W', 'B', 'W', 'B', 'W' ],
    [ 'W', 'W', 'B', 'W', 'W', 'B', 'W', 'B', 'B', 'W', 'B', 'W', 'B', 'W', 'B', 'W', 'B', 'W', 'B', 'W' ],
    [ 'W', 'B', 'B', 'B', 'B', 'B', 'W', 'W', 'B', 'W', 'B', 'W', 'B', 'W', 'B', 'W', 'B', 'W', 'B', 'W' ],
    [ 'W', 'W', 'W', 'W', 'W', 'B', 'W', 'B', 'B', 'W', 'B', 'W', 'B', 'W', 'B', 'W', 'B', 'W', 'B', 'W' ],
    [ 'W', 'B', 'W', 'B', 'W', 'B', 'W', 'W', 'B', 'B', 'B', 'W', 'B', 'W', 'B', 'W', 'B', 'W', 'B', 'W' ],
    [ 'W', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'W', 'B', 'W', 'B', 'W', 'B', 'W', 'B', 'B', 'B', 'W' ],
    [ 'W', 'W', 'W', 'W', 'W', 'B', 'W', 'W', 'W', 'W', 'B', 'W', 'B', 'W', 'B', 'W', 'W', 'W', 'B', 'W' ],
    [ 'W', 'B', 'B', 'B', 'B', 'B', 'W', 'B', 'B', 'B', 'B', 'B', 'B', 'W', 'B', 'W', 'B', 'W', 'B', 'W' ],
    [ 'W', 'W', 'W', 'B', 'W', 'B', 'W', 'W', 'W', 'W', 'W', 'W', 'B', 'B', 'B', 'W', 'B', 'W', 'B', 'W' ],
    [ 'W', 'B', 'B', 'B', 'W', 'B', 'W', 'B', 'B', 'B', 'B', 'B', 'B', 'W', 'B', 'B', 'B', 'W', 'B', 'W' ],
    [ 'W', 'W', 'B', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'B', 'W', 'B', 'W' ],
    [ 'W', 'B', 'B', 'W', 'B', 'B', 'B', 'B', 'W', 'B', 'B', 'B', 'B', 'B', 'B', 'W', 'B', 'W', 'B', 'W' ],
    [ 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'B', 'W', 'W', 'W', 'W', 'W', 'W', 'B', 'W', 'B', 'W', 'B', 'W' ],
    [ 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'W' ],
  ])
  ground_assignment = {get_pos(x=x, y=y): ground[y][x] for x in range(ground.shape[1]) for y in range(ground.shape[0])}
  assert set(solution.keys()) == set(ground_assignment.keys()), f'solution keys != ground assignment keys, {set(solution.keys()) ^ set(ground_assignment.keys())} \n\n\n{solution} \n\n\n{ground_assignment}'
  for pos in solution.keys():
    assert solution[pos] == ground_assignment[pos], f'solution[{pos}] != ground_assignment[{pos}], {solution[pos]} != {ground_assignment[pos]}'

def test_ground_3():
  # 15 x 15 example
  # https://www.puzzle-yin-yang.com/?e=Njo5MDcsNDk4
  board = np.array([
      [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
      [' ', ' ', ' ', ' ', ' ', ' ', 'B', ' ', ' ', ' ', ' ', 'B', ' ', ' ', ' '],
      [' ', ' ', 'W', ' ', 'W', ' ', 'B', ' ', ' ', ' ', ' ', ' ', 'W', ' ', ' '],
      [' ', 'B', 'B', ' ', 'W', ' ', ' ', ' ', 'W', ' ', ' ', ' ', ' ', ' ', ' '],
      [' ', ' ', 'W', 'W', ' ', ' ', 'B', 'W', 'W', ' ', ' ', ' ', 'W', ' ', ' '],
      [' ', 'B', ' ', ' ', 'W', ' ', ' ', 'W', ' ', 'B', ' ', ' ', ' ', ' ', ' '],
      [' ', ' ', 'B', ' ', ' ', ' ', 'B', 'W', ' ', ' ', ' ', 'W', ' ', 'B', ' '],
      [' ', 'W', ' ', ' ', 'W', ' ', ' ', ' ', 'W', ' ', 'W', ' ', 'W', ' ', ' '],
      [' ', 'W', 'B', ' ', ' ', ' ', ' ', 'W', ' ', 'B', 'B', 'B', 'B', 'B', ' '],
      [' ', 'W', 'B', 'W', ' ', ' ', 'W', ' ', 'W', 'W', 'W', 'W', 'W', ' ', ' '],
      [' ', 'W', ' ', 'W', 'B', 'W', ' ', 'B', ' ', 'B', ' ', 'B', ' ', 'B', ' '],
      [' ', ' ', 'W', ' ', 'B', ' ', 'W', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
      ['W', ' ', 'B', 'B', ' ', 'B', ' ', 'W', 'W', ' ', 'W', ' ', 'W', ' ', ' '],
      [' ', ' ', 'B', ' ', 'W', ' ', 'B', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
      [' ', ' ', ' ', 'W', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']
  ])
  binst = solver.Board(board=board)
  solutions = binst.solve_and_print()
  assert len(solutions) == 1, f'unique solutions != 1, == {len(solutions)}'
  solution = solutions[0].assignment
  ground = np.array([
    [ 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B' ],
    [ 'B', 'W', 'B', 'W', 'B', 'W', 'B', 'W', 'B', 'W', 'W', 'B', 'W', 'W', 'B' ],
    [ 'B', 'W', 'W', 'W', 'W', 'W', 'B', 'W', 'W', 'W', 'B', 'B', 'W', 'B', 'B' ],
    [ 'B', 'B', 'B', 'B', 'W', 'B', 'B', 'B', 'W', 'B', 'B', 'W', 'W', 'W', 'B' ],
    [ 'B', 'W', 'W', 'W', 'W', 'W', 'B', 'W', 'W', 'W', 'B', 'B', 'W', 'B', 'B' ],
    [ 'B', 'B', 'B', 'B', 'W', 'B', 'B', 'W', 'B', 'B', 'B', 'W', 'W', 'W', 'B' ],
    [ 'B', 'W', 'B', 'W', 'W', 'W', 'B', 'W', 'B', 'W', 'B', 'W', 'B', 'B', 'B' ],
    [ 'B', 'W', 'B', 'B', 'W', 'B', 'B', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'B' ],
    [ 'B', 'W', 'B', 'W', 'W', 'W', 'B', 'W', 'B', 'B', 'B', 'B', 'B', 'B', 'B' ],
    [ 'B', 'W', 'B', 'W', 'B', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'B' ],
    [ 'B', 'W', 'B', 'W', 'B', 'W', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B' ],
    [ 'B', 'W', 'W', 'W', 'B', 'W', 'W', 'W', 'B', 'W', 'B', 'W', 'B', 'W', 'B' ],
    [ 'W', 'W', 'B', 'B', 'B', 'B', 'B', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'B' ],
    [ 'W', 'B', 'B', 'W', 'W', 'W', 'B', 'W', 'B', 'W', 'B', 'W', 'B', 'W', 'B' ],
    [ 'W', 'W', 'W', 'W', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B' ],
  ])
  ground_assignment = {get_pos(x=x, y=y): ground[y][x] for x in range(ground.shape[1]) for y in range(ground.shape[0])}
  assert set(solution.keys()) == set(ground_assignment.keys()), f'solution keys != ground assignment keys, {set(solution.keys()) ^ set(ground_assignment.keys())} \n\n\n{solution} \n\n\n{ground_assignment}'
  for pos in solution.keys():
    assert solution[pos] == ground_assignment[pos], f'solution[{pos}] != ground_assignment[{pos}], {solution[pos]} != {ground_assignment[pos]}'

def test_ground_4():
  # 10 x 10 example
  # https://www.puzzle-yin-yang.com/?e=MzoyLDcwMSw2NTY=
  board = np.array([
    [' ', ' ', 'B', 'B', 'B', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', 'B', ' ', 'W', ' ', ' ', ' ', ' '],
    [' ', ' ', 'W', ' ', ' ', 'B', 'W', 'W', ' ', ' '],
    [' ', ' ', ' ', ' ', 'B', ' ', ' ', ' ', 'W', ' '],
    [' ', 'B', ' ', 'W', ' ', 'B', 'B', ' ', 'W', ' '],
    [' ', ' ', 'W', ' ', 'B', ' ', 'B', ' ', ' ', ' '],
    [' ', 'B', ' ', 'W', ' ', 'W', ' ', 'W', ' ', 'B'],
    [' ', ' ', 'W', ' ', 'W', ' ', 'W', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', 'W', 'W', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'B'],
  ])
  binst = solver.Board(board=board)
  solutions = binst.solve_and_print()
  assert len(solutions) == 1, f'unique solutions != 1, == {len(solutions)}'
  ground = np.array([
    ['B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B'],
    ['B', 'W', 'W', 'B', 'W', 'W', 'W', 'B', 'W', 'B'],
    ['B', 'B', 'W', 'B', 'B', 'B', 'W', 'W', 'W', 'B'],
    ['B', 'W', 'W', 'W', 'B', 'W', 'W', 'B', 'W', 'B'],
    ['B', 'B', 'B', 'W', 'B', 'B', 'B', 'B', 'W', 'B'],
    ['B', 'W', 'W', 'W', 'B', 'W', 'B', 'W', 'W', 'B'],
    ['B', 'B', 'B', 'W', 'B', 'W', 'B', 'W', 'B', 'B'],
    ['B', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'B', 'W'],
    ['B', 'W', 'B', 'W', 'B', 'W', 'B', 'W', 'W', 'W'],
    ['B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B'],
  ])
  solution = solutions[0].assignment
  ground_assignment = {get_pos(x=x, y=y): ground[y][x] for x in range(ground.shape[1]) for y in range(ground.shape[0])}
  assert set(solution.keys()) == set(ground_assignment.keys()), f'solution keys != ground assignment keys, {set(solution.keys()) ^ set(ground_assignment.keys())} \n\n\n{solution} \n\n\n{ground_assignment}'
  for pos in solution.keys():
    assert solution[pos] == ground_assignment[pos], f'solution[{pos}] != ground_assignment[{pos}], {solution[pos]} != {ground_assignment[pos]}'

if __name__ == '__main__':
  test_ground()
  test_ground_4()
  test_ground_3()
  test_ground_2()