import numpy as np
import board

# define board and parameters
top_numbers = [
  [2, 5],
  [2, 2],
  [4, 3, 2],
  [3, 2, 3, 2],
  [3, 6],
  [2, 3, 1],
  [3],
  [1, 4],
  [4],
  [2, 9],
  [3, 7],
  [3, 6, 2],
  [2, 3],
  [5, 1, 1, 1],
  [4, 6],
]
side_numbers = [
  [4, 3],
  [4, 3],
  [5, 2, 1],
  [3, 3],
  [3],
  [1, 2],
  [1, 1, 1, 2],
  [3],
  [1, 3],
  [3, 3, 1],
  [1, 4, 6],
  [1, 4, 6, 1],
  [1, 7, 3],
  [5, 6, 1],
  [10, 1, 2],
]
# top_numbers = [
#   -1,
#   -1,
#   -1,
#   -1,
#   -1,
# ]
# side_numbers = [
#   [2, 2],
# ]
binst = board.Board(top=top_numbers, side=side_numbers)
solutions = binst.solve_and_print()
assert len(solutions) == 1, f'unique solutions != 1, == {len(solutions)}'