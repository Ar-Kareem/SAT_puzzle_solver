import numpy as np
import board

clues = np.array([
    [-1, 10, -1, 9, 14, -1, -1, -1, -1],
    [-1, -1, 8, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, 6, -1, 6, -1],
    [-1, 4, -1, 6, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1, 11, -1, -1],
    [-1, -1, -1, -1, 7, 3, -1, 2, -1],
])
board = board.Board(clues)
sols = board.solve_and_print()