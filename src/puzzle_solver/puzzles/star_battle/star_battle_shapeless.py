import numpy as np

from . import star_battle

class Board(star_battle.Board):
    def __init__(self, board: np.array, star_count: int = 1):
        super().__init__(board=board, star_count=star_count, shapeless=True)
