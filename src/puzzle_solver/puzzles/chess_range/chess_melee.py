from .chess_range import Board as RangeBoard

class Board(RangeBoard):
    def __init__(self, pieces: list[str], colors: list[str]):
        super().__init__(pieces=pieces, colors=colors)

