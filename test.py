import numpy as np
import importlib
import board
from ortools.sat.python import cp_model
import multiprocessing
from utils import get_char

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

def callback(single_res: board.SingleSolution):
    print("Solution found")
    res = np.zeros_like(bor)
    for pos in binst.get_all_pos():
      c = get_char(binst.board, pos)
      if c == '*':
          c = single_res.assignment[pos].value[0]
      res[pos[1]][pos[0]] = c
    print(res)

binst.solve_all(callback=callback)
