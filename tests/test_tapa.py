import numpy as np

from puzzle_solver import tapa_solver as solver
from puzzle_solver.core.utils import get_pos

def test_toy():
    board = np.array([
        ['   ', '   ', '   ', '   ', '   ', '   '],
        ['   ', '6  ', '1/4', '   ', '6  ', '   '],
        ['   ', '   ', '   ', '   ', '1/5', '   '],
        ['   ', '2/4', '   ', '   ', '   ', '   '],
        ['   ', '3/3', '   ', '7  ', '3/3', '   '],
        ['   ', '   ', '   ', '   ', '   ', '   '],
    ])
    binst = solver.Board(board=board)
    solutions = binst.solve_and_print()
    assert len(solutions) == 1, f'unique solutions != 1, == {len(solutions)}'
    solution = solutions[0].assignment
    ground = np.array([
        [ 'B', 'B', 'B', 'B', 'B', 'B' ],
        [ 'B', ' ', ' ', 'B', ' ', 'B' ],
        [ 'B', 'B', ' ', ' ', ' ', 'B' ],
        [ 'B', ' ', 'B', 'B', 'B', 'B' ],
        [ 'B', ' ', 'B', ' ', ' ', ' ' ],
        [ 'B', ' ', 'B', 'B', 'B', 'B' ],
    ])
    ground_assignment = {get_pos(x=x, y=y): 1 if ground[y][x] == 'B' else 0 for x in range(ground.shape[1]) for y in range(ground.shape[0])}
    assert set(solution.keys()) == set(ground_assignment.keys()), f'solution keys != ground assignment keys, {set(solution.keys()) ^ set(ground_assignment.keys())} \n\n\n{solution} \n\n\n{ground_assignment}'
    for pos in solution.keys():
        assert solution[pos] == ground_assignment[pos], f'solution[{pos}] != ground_assignment[{pos}], {solution[pos]} != {ground_assignment[pos]}'


def test_toy_2():
    # easy 6 x 6 that has a cell with 3 numbers
    # https://www.puzzle-tapa.com/?e=MDoxLDEwMSwwOTU=
    board = np.array([
        ['1  ', '   ', '   ', '   ', '   ', '1  '],
        ['1/2', '   ', '   ', '   ', '   ', '2  '],
        ['   ', '   ', '   ', '   ', '   ', '   '],
        ['   ', '   ', '1/2','1/1/3','   ', '   '],
        ['1/2', '   ', '   ', '   ', '   ', '5  '],
        ['   ', '   ', '   ', '   ', '   ', '   '],
    ])
    binst = solver.Board(board=board)
    solutions = binst.solve_and_print()
    assert len(solutions) == 1, f'unique solutions != 1, == {len(solutions)}'
    solution = solutions[0].assignment
    ground = np.array([
        [ ' ', 'B', 'B', ' ', ' ', ' ' ],
        [ ' ', ' ', 'B', 'B', 'B', ' ' ],
        [ 'B', 'B', 'B', ' ', 'B', ' ' ],
        [ 'B', ' ', ' ', ' ', 'B', 'B' ],
        [ ' ', ' ', 'B', ' ', 'B', ' ' ],
        [ 'B', 'B', 'B', 'B', 'B', 'B' ],
    ])
    ground_assignment = {get_pos(x=x, y=y): 1 if ground[y][x] == 'B' else 0 for x in range(ground.shape[1]) for y in range(ground.shape[0])}
    assert set(solution.keys()) == set(ground_assignment.keys()), f'solution keys != ground assignment keys, {set(solution.keys()) ^ set(ground_assignment.keys())} \n\n\n{solution} \n\n\n{ground_assignment}'
    for pos in solution.keys():
        assert solution[pos] == ground_assignment[pos], f'solution[{pos}] != ground_assignment[{pos}], {solution[pos]} != {ground_assignment[pos]}'


def test_ground():
    # 20 by 20 hard
    # https://www.puzzle-tapa.com/?e=Nzo5LDg3MCw2NTg=
    board = np.array([
        ['   ', '   ', '   ', '   ', '   ', '3  ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '3  ', '   ', '   ', '   ', '   ', '   '],
        ['   ', '   ', '   ', '   ', '2/3', '   ', '   ','1/2/2','   ', '3/3', '7  ', '   ', '7  ', '   ', '   ', '2/3', '   ', '   ', '   ', '   '],
        ['   ', '2/4', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '2/3', '   '],
        ['   ', '   ', '   ', '1/3','1/1/2','   ', '   ', '7  ', '   ', '   ', '   ', '   ', '7  ', '   ','   ','1/1/1/1','1/3','   ', '   ', '   '],
        ['   ', '   ','1/1/3','   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '1/4', '   ', '   '],

        ['   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ','1/1/3','1/2', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   '],
        ['   ', '   ', '5  ', '   ', '   ','1/1/1','1/1', '   ', '   ', '   ', '   ', '   ', '   ', '1/3', '2/3', '   ', '   ', '3/3', '   ', '   '],
        ['   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   '],

        ['   ', '   ','1/1/2','   ', '   ', '   ', '   ', '   ', '7  ', '3/3', '3/3', '2/4', '   ', '   ', '   ', '   ', '   ', '6  ', '   ', '   '],
        ['   ', '1/4', '   ', '   ', '2/3', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '2/4', '   ', '   ', '1/3', '   '],
        ['   ', '1/3', '   ', '   ', '1/4', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '2/3', '   ', '   ','1/1/2','   '],
        ['   ', '   ', '6  ', '   ', '   ', '   ', '   ', '   ', '1/1', '1/2','1/1/2','1/4', '   ', '   ', '   ', '   ', '   ', '6  ', '   ', '   '],
        ['   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   '],

        ['   ', '   ', '3/3', '   ', '   ', '1/2', '1/1', '   ', '   ', '   ', '   ', '   ', '   ', '1/3','1/1/3','   ', '   ', '2/3', '   ', '   '],
        ['   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '4  ', '1/3', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   '],
        ['   ', '   ', '1/4', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '1/3', '   ', '   '],

        ['   ', '   ', '   ', '1/3','1/1/3','   ', '   ', '6  ', '   ', '   ', '   ', '   ', '7  ', '   ', '   ','1/1/2','1/3', '   ', '   ', '   '],
        ['   ', '2/3', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '2/3', '   '],
        ['   ', '   ', '   ', '   ', '2/3', '   ', '   ', '6  ', '   ', '1/3', '4  ', '   ', '6  ', '   ', '   ', '2/3', '   ', '   ', '   ', '   '],
        ['   ', '   ', '   ', '   ', '   ', '1/1', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '1/1', '   ', '   ', '   ', '   ', '   '],
    ])
    binst = solver.Board(board=board)
    solutions = binst.solve_and_print()
    assert len(solutions) == 1, f'unique solutions != 1, == {len(solutions)}'
    solution = solutions[0].assignment
    ground = np.array([
        [ ' ', 'B', 'B', 'B', ' ', ' ', 'B', ' ', 'B', 'B', 'B', 'B', 'B', 'B', ' ', ' ', 'B', 'B', 'B', 'B' ],
        [ 'B', 'B', ' ', 'B', ' ', 'B', 'B', ' ', ' ', ' ', ' ', 'B', ' ', 'B', 'B', ' ', 'B', ' ', ' ', 'B' ],
        [ 'B', ' ', 'B', 'B', ' ', 'B', ' ', 'B', 'B', 'B', 'B', 'B', 'B', ' ', 'B', ' ', 'B', 'B', ' ', 'B' ],
        [ 'B', ' ', 'B', ' ', ' ', 'B', 'B', ' ', 'B', ' ', ' ', 'B', ' ', 'B', ' ', ' ', ' ', 'B', ' ', 'B' ],
        [ 'B', 'B', ' ', 'B', ' ', ' ', 'B', 'B', 'B', ' ', 'B', 'B', 'B', 'B', 'B', ' ', 'B', ' ', ' ', 'B' ],
        [ 'B', ' ', 'B', 'B', 'B', ' ', 'B', ' ', 'B', ' ', ' ', ' ', ' ', ' ', 'B', 'B', 'B', 'B', 'B', 'B' ],
        [ 'B', ' ', ' ', 'B', ' ', ' ', ' ', ' ', 'B', ' ', 'B', ' ', ' ', ' ', ' ', 'B', ' ', ' ', ' ', 'B' ],
        [ 'B', ' ', 'B', 'B', 'B', ' ', ' ', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', ' ', 'B', 'B', 'B', 'B' ],
        [ 'B', 'B', ' ', ' ', 'B', 'B', ' ', 'B', ' ', ' ', ' ', ' ', 'B', ' ', ' ', 'B', 'B', ' ', ' ', 'B' ],
        [ 'B', ' ', ' ', 'B', ' ', 'B', 'B', 'B', 'B', 'B', 'B', 'B', ' ', ' ', 'B', ' ', 'B', 'B', ' ', 'B' ],
        [ 'B', ' ', 'B', 'B', ' ', ' ', 'B', ' ', ' ', 'B', ' ', 'B', 'B', 'B', 'B', ' ', 'B', ' ', ' ', 'B' ],
        [ 'B', ' ', ' ', 'B', 'B', ' ', 'B', ' ', ' ', ' ', ' ', ' ', 'B', ' ', ' ', ' ', 'B', ' ', 'B', ' ' ],
        [ 'B', 'B', 'B', 'B', ' ', ' ', 'B', ' ', ' ', 'B', 'B', ' ', 'B', 'B', ' ', 'B', 'B', 'B', 'B', 'B' ],
        [ 'B', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'B', 'B', ' ', 'B', 'B', ' ', ' ', 'B', ' ', ' ', ' ', 'B' ],
        [ 'B', 'B', 'B', 'B', 'B', 'B', ' ', ' ', 'B', ' ', ' ', 'B', ' ', 'B', ' ', 'B', 'B', 'B', ' ', 'B' ],
        [ 'B', ' ', ' ', 'B', ' ', 'B', 'B', 'B', 'B', ' ', ' ', 'B', 'B', 'B', ' ', ' ', 'B', ' ', ' ', 'B' ],
        [ 'B', ' ', 'B', ' ', ' ', 'B', ' ', ' ', 'B', 'B', 'B', 'B', ' ', 'B', 'B', ' ', ' ', 'B', ' ', 'B' ],
        [ 'B', ' ', 'B', 'B', ' ', 'B', ' ', 'B', 'B', ' ', ' ', 'B', 'B', ' ', 'B', ' ', 'B', 'B', ' ', 'B' ],
        [ 'B', ' ', ' ', 'B', ' ', 'B', ' ', ' ', 'B', ' ', ' ', 'B', ' ', ' ', 'B', ' ', 'B', ' ', ' ', 'B' ],
        [ 'B', 'B', 'B', 'B', ' ', ' ', 'B', 'B', 'B', ' ', 'B', 'B', 'B', 'B', ' ', ' ', 'B', 'B', 'B', 'B' ],
    ])
    ground_assignment = {get_pos(x=x, y=y): 1 if ground[y][x] == 'B' else 0 for x in range(ground.shape[1]) for y in range(ground.shape[0])}
    assert set(solution.keys()) == set(ground_assignment.keys()), f'solution keys != ground assignment keys, {set(solution.keys()) ^ set(ground_assignment.keys())} \n\n\n{solution} \n\n\n{ground_assignment}'
    for pos in solution.keys():
        assert solution[pos] == ground_assignment[pos], f'solution[{pos}] != ground_assignment[{pos}], {solution[pos]} != {ground_assignment[pos]}'


if __name__ == '__main__':
    test_toy()
    test_toy_2()
    test_ground()
