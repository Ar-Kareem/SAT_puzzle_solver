from .chess_range import Board as RangeBoard
from .chess_range import PieceType

class Board(RangeBoard):
    def __init__(self, pieces: list[str]):
        king_pieces = [p for p in range(len(pieces)) if pieces[p][0] == 'K']
        assert len(king_pieces) == 1, 'exactly one king piece is required'
        super().__init__(pieces, max_moves_per_piece=2, last_piece_alive=PieceType.KING)

