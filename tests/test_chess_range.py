from puzzle_solver import chess_range_solver as solver


# https://www.puzzle-chess.com/chess-ranger-11/?e=Nzo5NDAsOTEy
# algebraic notation
board = ['Qe7', 'Nc6', 'Kb6', 'Pb5', 'Nf5', 'Pg4', 'Rb3', 'Bc3', 'Pd3', 'Pc2', 'Rg2']

def test_ground():
    binst = solver.Board(board)
    solutions = binst.solve_and_print(max_solutions=1)
    assert len(solutions) >= 1, f'no solutions found'

if __name__ == '__main__':
    test_ground()