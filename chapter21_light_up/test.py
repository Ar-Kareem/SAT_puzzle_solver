import numpy as np
import board
bor = np.array([
  ['W', '*', '*', '1', '*', '*', '2'],
  ['*', '*', '*', 'W', '*', '*', '*'],
  ['*', '*', '2', '*', 'W', '*', '*'],
  ['*', '*', '*', '*', '*', '*', '*'],
  ['*', '*', '1', '*', 'W', '*', '*'],
  ['*', '*', '*', '1', '*', '*', '*'],
  ['1', '*', '*', 'W', '*', '*', 'W'],
])

binst = board.Board(board=bor)
solutions = binst.solve_and_print()
assert len(solutions) == 1, f'unique solutions != 1, == {len(solutions)}'
