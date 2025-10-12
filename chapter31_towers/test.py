import numpy as np
import board

# define board and parameters
bor = np.array([
  ['*', '*', '*', '*', '*', '*'],
  ['*', '*', '*', '2', '*', '*'],
  ['*', '*', '2', '*', '*', '*'],
  ['*', '*', '*', '*', '*', '*'],
  ['*', '*', '*', '*', '*', '*'],
  ['*', '*', '*', '*', '*', '*'],
])
t = np.array([3, -1, 3, 2, -1, 2])
b = np.array([-1, -1, 2, -1, 5, -1])
r = np.array([-1, 3, -1, 3, 2, -1])
l = np.array([3, -1, -1, 2, 3, 1])
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