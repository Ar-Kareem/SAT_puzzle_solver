import numpy as np
import board
from utils import Monster

# define board and parameters
bor = np.array([
  ['**', '**', '//', '\\', '**', '//'],
  ['**', '**', '\\', '//', '**', '**'],
  ['//', '\\', '**', '**', '//', '//'],
  ['**', '**', '**', '**', '**', '**'],
  ['\\', '\\', '**', '**', '**', '**'],
  ['**', '//', '\\', '**', '**', '\\'],
])
t = np.array([0, 4, 2, 0, 5, 0])
b = np.array([0, 0, 0, 2, 0, 6])
r = np.array([3, 4, 0, 3, 5, 0])
l = np.array([0, 5, 2, 3, 1, 5])
counts = {Monster.VAMPIRE: 6, Monster.ZOMBIE: 3, Monster.GHOST: 13}

# create board and solve
binst = board.Board(board=bor, sides={'top': t, 'bottom': b, 'right': r, 'left': l}, monster_count=counts)
binst.solve_and_print()
