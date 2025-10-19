from .chess_range import Board as RangeBoard
from .chess_range import PieceType

class Board(RangeBoard):
    def __init__(self, pieces: list[str], colors: list[str]):
        super().__init__(pieces=pieces, colors=colors)

