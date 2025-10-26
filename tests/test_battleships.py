import numpy as np

from puzzle_solver import battleships_solver as solver
from puzzle_solver.core.utils import get_pos

def test_ground_1():
  board = np.array([
    [' ', ' ', ' ', ' ', ' ', ' '],
    [' ', 'R', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' '],
  ])
  top = np.array([1, 1, 1, 3, 1, 3])
  side = np.array([2, 2, 3, 0, 3, 0])
  ship_counts = {1: 3, 2: 2, 3: 1}
  binst = solver.Board(board=board, top=top, side=side, ship_counts=ship_counts)
  solutions = binst.solve_and_print()
  ground = np.array([
    ['0', '0', '0', '1', '0', '1'],
    ['1', '1', '0', '0', '0', '0'],
    ['0', '0', '0', '1', '1', '1'],
    ['0', '0', '0', '0', '0', '0'],
    ['0', '0', '1', '1', '0', '1'],
    ['0', '0', '0', '0', '0', '0'],
  ])
  assert len(solutions) == 1, f'unique solutions != 1, == {len(solutions)}'
  solution = solutions[0].assignment
  ground_assignment = {get_pos(x=x, y=y): 1 if ground[y][x] == '1' else 0 for x in range(ground.shape[1]) for y in range(ground.shape[0])}
  assert set(solution.keys()) == set(ground_assignment.keys()), f'solution keys != ground assignment keys, {set(solution.keys()) ^ set(ground_assignment.keys())} \n\n\n{solution} \n\n\n{ground_assignment}'
  for pos, val in solution.items():
    assert val == ground_assignment[pos], f'solution value != ground assignment value, {pos} = {val} != {ground_assignment[pos]}'

def test_ground_2():
  # https://www.puzzle-battleships.com/?e=Nzo4OTMsNTYz
  board = np.array([
    [' ', ' ', ' ', ' ', ' ', 'S', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'S', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'O', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    ['W', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', 'O', ' ', ' ', ' ', ' ', 'W', ' ', ' ', 'R'],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'U', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', 'L', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'S'],
  ])
  top = np.array([2, 2, 4, 2, 1, 2, 1, 2, 4, 1, 3, 2, 5, 2, 2])
  side = np.array([1, 2, 1, 1, 0, 7, 0, 9, 2, 2, 5, 1, 3, 0, 1])
  ship_counts = {1: 5, 2: 4, 3: 3, 4: 2, 5: 1}
  binst = solver.Board(board=board, top=top, side=side, ship_counts=ship_counts)
  solutions = binst.solve_and_print()
  assert len(solutions) == 1, f'unique solutions != 1, == {len(solutions)}'

if __name__ == '__main__':
  # test_ground_1()
  test_ground_2()
