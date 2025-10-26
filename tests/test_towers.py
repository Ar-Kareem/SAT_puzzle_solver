import numpy as np

from puzzle_solver import towers_solver as solver
from puzzle_solver.core.utils import get_pos


def test_ground():
  # https://www.chiark.greenend.org.uk/~sgtatham/puzzles/js/towers.html#6:2//2/2/2/3/2/4//4//////2//4/3//2///,n3u
  board = np.array([
    [' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', '3', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' '],
  ])
  side_t = np.array([2, -1, 2, 2, 2, 3])
  side_b = np.array([2, 4, -1, 4, -1, -1])
  side_r = np.array([3, -1, 2, -1, -1, -1])
  side_l = np.array([-1, -1, -1, 2, -1, 4])
  binst = solver.Board(board=board, sides={'top': side_t, 'bottom': side_b, 'right': side_r, 'left': side_l})
  solutions = binst.solve_and_print()
  ground = np.array([
    [5, 6, 4, 1, 2, 3],
    [3, 4, 2, 6, 1, 5],
    [4, 5, 3, 2, 6, 1],
    [2, 1, 6, 5, 3, 4],
    [6, 3, 1, 4, 5, 2],
    [1, 2, 5, 3, 4, 6],
  ])
  assert len(solutions) == 1, f'unique solutions != 1, == {len(solutions)}'
  solution = solutions[0].assignment
  ground_assignment = {get_pos(x=x, y=y): ground[y][x] for x in range(ground.shape[1]) for y in range(ground.shape[0])}
  assert set(solution.keys()) == set(ground_assignment.keys()), f'solution keys != ground assignment keys, {set(solution.keys()) ^ set(ground_assignment.keys())} \n\n\n{solution} \n\n\n{ground_assignment}'
  for pos in solution.keys():
    assert solution[pos] == ground_assignment[pos], f'solution[{pos}] != ground_assignment[{pos}], {solution[pos]} != {ground_assignment[pos]}'


if __name__ == '__main__':
  test_ground()
