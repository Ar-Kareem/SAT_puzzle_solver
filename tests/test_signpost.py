import numpy as np

from puzzle_solver import signpost_solver as solver
from puzzle_solver.core.utils import get_pos


def test_ground():
  # https://www.chiark.greenend.org.uk/~sgtatham/puzzles/js/signpost.html#7x7c%23512596780210399
  # Q = up-left, W = up, E = up-right, A = left, D = right, Z = down-left, X = down, C = down-right
  board1 = np.array([
    ['C', 'D', 'D', 'X', 'D', 'Z', 'X'],
    ['D', 'C', 'D', 'X', 'X', 'A', 'A'],
    ['X', 'X', 'D', 'Q', 'Z', 'W', 'A'],
    ['W', 'D', 'W', 'W', 'X', 'Z', 'X'],
    ['X', 'A', 'Q', 'Q', 'A', 'Q', 'X'],
    ['D', 'W', 'W', 'A', 'E', 'A', 'Z'],
    ['D', 'E', 'D', 'E', 'D', 'A', ' '],
  ])
  board2 = np.array([
    [ 1,  0, 23,  0,  0,  0,  0],
    [30, 32,  0,  0,  0,  0,  0],
    [ 0,  0,  2,  0,  0,  0,  0],
    [ 0,  0,  0,  0,  0,  0,  0],
    [ 0, 45,  0,  0, 33,  0,  0],
    [ 0,  0, 22,  8, 39, 10,  0],
    [ 0,  0,  0,  0,  0, 20, 49],
  ])
  binst = solver.Board(board=board1, values=board2)
  solutions = binst.solve_and_print()
  ground = np.array([
    [1, 42, 23, 7, 43, 44, 24],
    [30, 32, 36, 5, 37, 4, 31],
    [28, 12, 2, 41, 26, 3, 25],
    [29, 13, 35, 6, 38, 14, 17],
    [46, 45, 27, 34, 33, 40, 18],
    [9, 11, 22, 8, 39, 10, 19],
    [47, 21, 15, 16, 48, 20, 49],
  ])
  assert len(solutions) == 1, f'unique solutions != 1, == {len(solutions)}'
  solution = solutions[0].assignment
  ground_assignment = {get_pos(x=x, y=y): ground[y][x] for x in range(ground.shape[1]) for y in range(ground.shape[0])}
  assert set(solution.keys()) == set(ground_assignment.keys()), f'solution keys != ground assignment keys, {set(solution.keys()) ^ set(ground_assignment.keys())} \n\n\n{solution} \n\n\n{ground_assignment}'
  for pos in solution.keys():
    assert solution[pos] == ground_assignment[pos], f'solution[{pos}] != ground_assignment[{pos}], {solution[pos]} != {ground_assignment[pos]}'


if __name__ == '__main__':
  test_ground()
