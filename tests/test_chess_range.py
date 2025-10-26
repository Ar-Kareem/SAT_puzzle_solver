from puzzle_solver import chess_range_solver as solver



def test_ground():
    # https://www.puzzle-chess.com/chess-ranger-11/?e=Nzo5NDAsOTEy
    # algebraic notation
    board = ['Qe7', 'Nc6', 'Kb6', 'Pb5', 'Nf5', 'Pg4', 'Rb3', 'Bc3', 'Pd3', 'Pc2', 'Rg2']
    binst = solver.Board(board)
    solutions = binst.solve_and_print(max_solutions=1)
    assert len(solutions) >= 1, 'no solutions found'

def test_ground_2():
    board = ['Qc3', 'Pd3', 'Ne3', 'Pf4']
    binst = solver.Board(board)
    solutions = binst.solve_and_print()
    assert len(solutions) == 1, f'unique solutions != 1, == {len(solutions)}'
    solution = solver.to_algebraic_notation(solutions[0])
    ground = ' | '.join(['Qc3->Pd3', 'Qd3->Ne3', 'Qe3->Pf4'])
    assert ' | '.join(solution) == ground, f'solution != {ground}, == {solution}'


def test_chess_jumping():
    board = ['Ba1', 'Kc3', 'Ke5']
    binst = solver.Board(board)
    solutions = binst.solve_and_print()
    assert len(solutions) == 1, f'unique solutions != 1, == {len(solutions)}'


if __name__ == '__main__':
    test_ground()
    test_ground_2()
