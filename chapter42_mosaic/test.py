import numpy as np
import board

# define board and parameters
bor = np.array([
  ['*', '*', '3', '4', '4'],
  ['1', '*', '*', '*', '*'],
  ['*', '1', '1', '3', '*'],
  ['*', '*', '1', '*', '*'],
  ['2', '*', '*', '0', '*'],
])
binst = board.Board(board=bor)
solutions = binst.solve_and_print()
assert len(solutions) == 1, f'unique solutions != 1, == {len(solutions)}'