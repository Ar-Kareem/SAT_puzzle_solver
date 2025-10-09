import numpy as np
import importlib
import board

importlib.reload(board)

bor = np.array([
  ['*', '*', '*'], 
  ['*', '\\', '*'], 
  ['*', '//', '*']]
)
t = np.array([1, 1, 1])
b = np.array([1, 1, 1])
r = np.array([1, 1, 1])
l = np.array([1, 1, 1])
binst = board.Board(board=bor, sides={'top': t, 'bottom': b, 'right': r, 'left': l})
binst.solve()
print(binst.solver.StatusName())

res = np.zeros_like(bor)
for pos in binst.get_all_pos():
    c = binst.get_char(pos)
    if c == '*':
        c = binst.get_solved_pos(pos)
    res[pos[1]][pos[0]] = c
print(res)