from puzzle_solver import chess_solo_solver as solver
from puzzle_solver.puzzles.chess_range.chess_range import to_algebraic_notation



def test_ground():
    # https://www.puzzle-chess.com/solo-chess-11/?e=MTg6NSw1NjQsMjMx
    # algebraic notation
    board = ['Kc6', 'Rc5', 'Rc4', 'Pb3', 'Bd3', 'Pd2', 'Pe3', 'Nf2', 'Ng2', 'Qg3', 'Pg6']
    binst = solver.Board(board)
    solutions = binst.solve_and_print(max_solutions=1)
    assert len(solutions) >= 1, f'no solutions found'
    ground = ' | '.join(['Pd2->Pe3', 'Pb3->Rc4', 'Ng2->Pe3', 'Qg3->Pg6', 'Qg6->Bd3', 'Nf2->Qd3', 'Nd3->Rc5', 'Ne3->Pc4', 'Kc6->Nc5', 'Kc5->Nc4'])
    solution = to_algebraic_notation(solutions[0].assignment)
    assert ' | '.join(solution) == ground, f'solution != {ground}, == {solution}'


if __name__ == '__main__':
    test_ground()
