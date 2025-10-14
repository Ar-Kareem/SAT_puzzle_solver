import numpy as np
import board

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
assert len(solutions) == 1, f'unique solutions != 1, == {len(solutions)}'