import numpy as np

from . import binairo

class Board(binairo.Board):
    def __init__(self, board: np.array, arith_rows: np.array, arith_cols: np.array):
        super().__init__(board=board, arith_rows=arith_rows, arith_cols=arith_cols, force_unique=False)
