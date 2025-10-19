from puzzle_solver import chess_solo_solver as solver
from puzzle_solver.puzzles.chess_range.chess_range import parse_algebraic_notation



def test_ground():
    ground = ['Pd2->Pe3', 'Pb3->Rc4', 'Ng2->Pe3', 'Qg3->Pg6', 'Qg6->Bd3', 'Nf2->Qd3', 'Nd3->Rc5', 'Ne3->Pc4', 'Kc6->Nc5', 'Kc5->Nc4']
    ground = [move.split('->') for move in ground]
    unsorted_ground = [(parse_algebraic_notation(move[0])[1], parse_algebraic_notation(move[1])[1]) for move in ground]
    unsorted_ground = sorted([(p1.x, p1.y, p2.x, p2.y) for p1, p2 in unsorted_ground])

    # https://www.puzzle-chess.com/solo-chess-11/?e=MTg6NSw1NjQsMjMx
    # algebraic notation
    board = ['Kc6', 'Rc5', 'Rc4', 'Pb3', 'Bd3', 'Pd2', 'Pe3', 'Nf2', 'Ng2', 'Qg3', 'Pg6']
    binst = solver.Board(board)
    solutions = binst.solve_and_print(max_solutions=1)
    assert len(solutions) == 1, f'unique solutions != 1, == {len(solutions)}'
    unsorted_solution = sorted([(p1.x, p1.y, p2.x, p2.y) for _, p1, p2, _ in solutions[0].assignment.values()])
    assert unsorted_ground == unsorted_solution, f'unsorted_ground != unsorted_solution, {unsorted_ground} != {unsorted_solution}'


if __name__ == '__main__':
    test_ground()
