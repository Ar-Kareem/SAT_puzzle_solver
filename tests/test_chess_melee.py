from puzzle_solver import chess_melee_solver as solver
from puzzle_solver.puzzles.chess_range.chess_range import to_algebraic_notation



def test_ground():
    # https://www.puzzle-chess.com/chess-melee-13/?e=MzE6NywyNzksNDYy
    # algebraic notation
    board = ['Pb7', 'Nc7', 'Bc6', 'Ne6', 'Pb5', 'Rc4', 'Qb3', 'Rf7', 'Rb6', 'Pe5', 'Nc3', 'Pd3', 'Nf3']
    colors = ['B', 'B', 'B', 'B', 'B', 'B', 'B', 'W', 'W', 'W', 'W', 'W', 'W']
    binst = solver.Board(board, colors)
    solutions = binst.solve_and_print()
    assert len(solutions) == 1, f'unique solutions != 1, == {len(solutions)}'
    ground = ' | '.join(['Rf7->Nc7', 'Ne6->Rc7', 'Pd3->Rc4', 'Qb3->Nc3', 'Pc4->Pb5', 'Qc3->Pe5', 'Nf3->Qe5', 'Nc7->Pb5', 'Ne5->Bc6', 'Pb7->Nc6', 'Rb6->Nb5', 'Pc6->Rb5'])
    solution = to_algebraic_notation(solutions[0])
    assert ' | '.join(solution) == ground, f'solution != {ground}, == {solution}'


def test_ground_2():
    board = ['Ba1', 'Bb2', 'Kc3', 'Kd4', 'Kc2']
    colors = ['W', 'W', 'B', 'B', 'B']
    binst = solver.Board(board, colors)
    solutions = binst.solve_and_print()
    assert len(solutions) == 1, f'unique solutions != 1, == {len(solutions)}'


def test_ground_3():
    board = ['Qc5', 'Nd5', 'Nd6', 'Pe6']
    colors = ['W', 'W', 'B', 'B']
    binst = solver.Board(board, colors)
    solutions = binst.solve_and_print()
    assert len(solutions) == 1, f'unique solutions != 1, == {len(solutions)}'



if __name__ == '__main__':
    test_ground()
