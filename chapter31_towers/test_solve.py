import numpy as np

from . import board

# https://www.chiark.greenend.org.uk/~sgtatham/puzzles/js/towers.html#6:2//2/2/2/3/2/4//4//////2//4/3//2///,n3u
bor = np.array([
  ['*', '*', '*', '*', '*', '*'],
  ['*', '*', '*', '*', '*', '*'],
  ['*', '*', '3', '*', '*', '*'],
  ['*', '*', '*', '*', '*', '*'],
  ['*', '*', '*', '*', '*', '*'],
  ['*', '*', '*', '*', '*', '*'],
])
t = np.array([2, -1, 2, 2, 2, 3])
b = np.array([2, 4, -1, 4, -1, -1])
r = np.array([3, -1, 2, -1, -1, -1])
l = np.array([-1, -1, -1, 2, -1, 4])
# bor = np.array([
#   ['*', '*', '*'],
#   ['*', '*', '*'],
#   ['*', '*', '*'],
# ])
# t = np.array([-1, -1, -1])
# b = np.array([-1, -1, -1])
# r = np.array([-1, -1, 1])
# l = np.array([-1, -1, -1])

binst = board.Board(board=bor, sides={'top': t, 'bottom': b, 'right': r, 'left': l})
solutions = binst.solve_and_print()

def test_ground():
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
  ground_assignment = {board.get_pos(x=x, y=y): ground[y][x] for x in range(ground.shape[1]) for y in range(ground.shape[0])}
  assert set(solution.keys()) == set(ground_assignment.keys()), f'solution keys != ground assignment keys, {set(solution.keys()) ^ set(ground_assignment.keys())} \n\n\n{solution} \n\n\n{ground_assignment}'
  for pos in solution.keys():
    assert solution[pos] == ground_assignment[pos], f'solution[{pos}] != ground_assignment[{pos}], {solution[pos]} != {ground_assignment[pos]}'
