import numpy as np
import board

# define board and parameters
# bor = np.array([
#   ['H', 'H', 'H', 'H', 'V'],
#   ['V', 'V', 'H', 'H', 'V'],
#   ['V', 'V', 'H', 'H', 'V'],
#   ['H', 'H', 'H', 'H', 'V'],
#   ['V', 'H', 'H', 'V', 'V'],
#   ['V', 'H', 'H', 'V', 'V'],
# ])
# pos_v = np.array([3, 2, 2, 0, 2])
# neg_v = np.array([2, 2, 1, 2, 2])
# pos_h = np.array([2, 1, 1, 2, 2, 1])
# neg_h = np.array([1, 2, 1, 2, 2, 1])

bor = np.array([
  ['V', 'H', 'H', 'V', 'V', 'H', 'H', 'H', 'H'],
  ['V', 'H', 'H', 'V', 'V', 'V', 'V', 'V', 'V'],
  ['V', 'H', 'H', 'H', 'H', 'V', 'V', 'V', 'V'],
  ['V', 'V', 'H', 'H', 'V', 'V', 'V', 'V', 'V'],
  ['V', 'V', 'H', 'H', 'V', 'V', 'V', 'V', 'V'],
  ['V', 'V', 'H', 'H', 'H', 'H', 'H', 'H', 'V'],
  ['V', 'V', 'V', 'H', 'H', 'V', 'H', 'H', 'V'],
  ['V', 'V', 'V', 'H', 'H', 'V', 'V', 'H', 'H'],
  ['V', 'V', 'H', 'H', 'H', 'H', 'V', 'H', 'H'],
  ['V', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H'],
])
pos_v = np.array([-1, -1, -1, 4, 1, 3, 5, 3, 5])
neg_v = np.array([5, 5, 4, -1, -1, 3, -1, 5, -1])
pos_h = np.array([-1, -1, -1, 4, -1, -1, -1, -1, -1, 5])
neg_h = np.array([3, -1, -1, -1, -1, -1, -1, 1, 3, -1])

binst = board.Board(board=bor, sides={'pos_v': pos_v, 'neg_v': neg_v, 'pos_h': pos_h, 'neg_h': neg_h})
solutions = binst.solve_and_print()
assert len(solutions) == 1, f'unique solutions != 1, == {len(solutions)}'