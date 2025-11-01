import numpy as np

from puzzle_solver import n_queens_solver as solver
from puzzle_solver.core.utils import Pos


def test_ground_1():
  board = np.array([
    ['00', '00', '00', '00', '00', '00', '00', '00'],
    ['01', '01', '00', '00', '00', '00', '00', '00'],
    ['01', '01', '02', '02', '02', '02', '00', '00'],
    ['01', '01', '02', '03', '02', '02', '04', '04'],
    ['01', '01', '03', '03', '05', '02', '04', '04'],
    ['01', '01', '03', '03', '05', '05', '04', '04'],
    ['01', '01', '03', '06', '06', '06', '06', '04'],
    ['01', '01', '06', '06', '04', '04', '04', '04']
  ])
  binst = solver.Board(board=board)
  solutions = binst.solve_and_print()
  assert len(solutions) == 1, f'unique solutions != 1, == {len(solutions)}'
  solution = solutions[0].assignment
  solution = {k: v for k, v in solution.items() if v == 1}
  ground = {Pos(x=3, y=1): 1, Pos(x=5, y=2): 1, Pos(x=7, y=3): 1, Pos(x=2, y=4): 1, Pos(x=4, y=5): 1, Pos(x=6, y=6): 1, Pos(x=1, y=7): 1}
  assert set(solution.keys()) == set(ground.keys()), f'solution keys != ground keys, {set(solution.keys()) ^ set(ground.keys())} \n\n\n{solution} \n\n\n{ground}'
  for pos in solution.keys():
    assert solution[pos] == ground[pos], f'solution[{pos}] != ground[{pos}], {solution[pos]} != {ground[pos]}'


def test_ground_2():
  board = np.array([
    ['00', '00', '00', '01', '01', '01', '01', '02'],
    ['00', '00', '01', '01', '03', '03', '02', '02'],
    ['00', '00', '01', '01', '03', '04', '04', '04'],
    ['00', '00', '01', '05', '05', '04', '04', '04'],
    ['00', '05', '05', '05', '05', '05', '06', '04'],
    ['00', '00', '05', '06', '06', '06', '06', '04'],
    ['00', '00', '06', '06', '06', '06', '06', '04'],
    ['00', '00', '06', '06', '06', '06', '06', '06']
  ])
  binst = solver.Board(board=board)
  solutions = binst.solve_and_print()
  assert len(solutions) == 1, f'unique solutions != 1, == {len(solutions)}'
  solution = solutions[0].assignment
  solution = {k: v for k, v in solution.items() if v == 1}
  ground = {Pos(x=3, y=0): 1, Pos(x=6, y=1): 1, Pos(x=4, y=2): 1, Pos(x=7, y=3): 1, Pos(x=5, y=4): 1, Pos(x=0, y=5): 1, Pos(x=2, y=6): 1}
  assert set(solution.keys()) == set(ground.keys()), f'solution keys != ground keys, {set(solution.keys()) ^ set(ground.keys())} \n\n\n{solution} \n\n\n{ground}'
  for pos in solution.keys():
    assert solution[pos] == ground[pos], f'solution[{pos}] != ground[{pos}], {solution[pos]} != {ground[pos]}'


if __name__ == '__main__':
  test_ground_1()
  test_ground_2()
