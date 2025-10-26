import numpy as np

from puzzle_solver import nurikabe_solver as solver
from puzzle_solver.core.utils import get_pos


def test_toy():
    # 5 x 5 easy
    # https://www.puzzle-nurikabe.com/?e=MDoxLDcyOSw1NzY=
    board = np.array([
        ['1', ' ', ' ', ' ', ' '],
        [' ', '2', ' ', '2', ' '],
        [' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' '],
        [' ', ' ', '3', ' ', ' '],
    ])
    binst = solver.Board(board=board)
    solutions = binst.solve_and_print()
    assert len(solutions) == 1, f'unique solutions != 1, == {len(solutions)}'
    solution = solutions[0].assignment
    ground = np.array([
        [' ', 'B', 'B', 'B', 'B',],
        ['B', ' ', 'B', ' ', 'B',],
        ['B', ' ', 'B', ' ', 'B',],
        ['B', 'B', 'B', 'B', 'B',],
        ['B', ' ', ' ', ' ', 'B',],
        ])
    ground_assignment = {get_pos(x=x, y=y): 1 if ground[y][x] == 'B' else 0 for x in range(ground.shape[1]) for y in range(ground.shape[0])}
    assert set(solution.keys()) == set(ground_assignment.keys()), f'solution keys != ground assignment keys, {set(solution.keys()) ^ set(ground_assignment.keys())} \n\n\n{solution} \n\n\n{ground_assignment}'
    for pos in solution.keys():
        assert solution[pos] == ground_assignment[pos], f'solution[{pos}] != ground_assignment[{pos}], {solution[pos]} != {ground_assignment[pos]}'


def test_ground():
    # 20 x 20
    # https://www.puzzle-nurikabe.com/?e=NDo5NzUsMjQw
    board = np.array([
        ['2', ' ', '3', ' ', '3', ' ', ' ', ' ', '3', ' ', ' ', '3', ' ', ' ', ' ', '2', ' ', '2', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', '2', ' ', ' ', '1', ' ', ' ', '1', ' ', '3', ' ', ' ', ' ', '3', ' ', ' ', ' '],
        ['2', ' ', ' ', '1', ' ', ' ', '3', ' ', ' ', '2', ' ', '2', ' ', ' ', ' ', '1', ' ', ' ', ' ', ' '],
        [' ', ' ', '2', ' ', '2', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '3', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '2', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        ['1', ' ', ' ', ' ', ' ', '1', ' ', '2', ' ', ' ', '3', ' ', ' ', ' ', ' ', ' ', ' ', '1', ' ', '2'],
        [' ', '2', ' ', '2', ' ', ' ', '1', ' ', ' ', ' ', ' ', ' ', ' ', '6', ' ', ' ', '2', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', '2', ' ', '7', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '3', ' '],
        [' ', ' ', '3', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '2', ' ', '2', ' ', '2', ' ', ' ', ' ', ' ', ' '],
        ['4', ' ', ' ', ' ', ' ', ' ', '7', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', '7', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '3', ' ', ' ', ' ', ' '],
        [' ', ' ', '2', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '1', ' ', '1', ' ', ' ', ' ', ' ', ' ', '3'],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '2', ' ', '4', ' ', ' ', '7', ' ', ' ', ' ', ' '],
        [' ', '1', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', '2', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '1', ' ', ' '],
        ['2', ' ', ' ', ' ', ' ', ' ', ' ', '1', ' ', '3', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '2', ' '],
        [' ', ' ', ' ', '4', ' ', ' ', ' ', ' ', '1', ' ', ' ', ' ', '2', ' ', '1', ' ', '3', ' ', ' ', ' '],
        [' ', '1', ' ', ' ', ' ', ' ', ' ', '3', ' ', ' ', '1', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '2'],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '1', ' ', ' ', ' ', ' ', ' '],
    ])
    binst = solver.Board(board=board)
    solutions = binst.solve_and_print()
    assert len(solutions) == 1, f'unique solutions != 1, == {len(solutions)}'
    solution = solutions[0].assignment
    ground = np.array([
        [ ' ', 'B', ' ', 'B', ' ', ' ', ' ', 'B', ' ', ' ', 'B', ' ', ' ', ' ', 'B', ' ', 'B', ' ', ' ', 'B' ],
        [ ' ', 'B', ' ', 'B', 'B', 'B', 'B', 'B', 'B', ' ', 'B', 'B', 'B', 'B', 'B', ' ', 'B', 'B', 'B', 'B' ],
        [ 'B', 'B', ' ', 'B', ' ', ' ', 'B', ' ', 'B', 'B', ' ', 'B', ' ', ' ', 'B', 'B', ' ', ' ', ' ', 'B' ],
        [ ' ', 'B', 'B', ' ', 'B', 'B', ' ', 'B', 'B', ' ', 'B', ' ', 'B', ' ', 'B', ' ', 'B', 'B', 'B', 'B' ],
        [ ' ', 'B', ' ', 'B', ' ', 'B', ' ', ' ', 'B', ' ', 'B', ' ', 'B', 'B', 'B', 'B', ' ', ' ', ' ', 'B' ],
        [ 'B', 'B', ' ', 'B', ' ', 'B', 'B', 'B', 'B', 'B', 'B', 'B', ' ', 'B', ' ', 'B', 'B', 'B', 'B', 'B' ],
        [ ' ', 'B', 'B', 'B', 'B', ' ', 'B', ' ', ' ', 'B', ' ', 'B', ' ', 'B', ' ', ' ', 'B', ' ', 'B', ' ' ],
        [ 'B', ' ', 'B', ' ', 'B', 'B', ' ', 'B', 'B', 'B', ' ', ' ', 'B', ' ', ' ', 'B', ' ', 'B', 'B', ' ' ],
        [ 'B', ' ', 'B', ' ', 'B', ' ', 'B', ' ', ' ', 'B', 'B', 'B', 'B', ' ', 'B', 'B', ' ', 'B', ' ', 'B' ],
        [ 'B', 'B', ' ', 'B', 'B', ' ', 'B', 'B', ' ', 'B', ' ', 'B', ' ', 'B', ' ', 'B', 'B', 'B', ' ', 'B' ],
        [ ' ', 'B', ' ', ' ', 'B', 'B', ' ', 'B', ' ', 'B', ' ', 'B', ' ', 'B', ' ', 'B', ' ', 'B', ' ', 'B' ],
        [ ' ', 'B', 'B', 'B', ' ', 'B', ' ', 'B', ' ', ' ', 'B', 'B', 'B', 'B', 'B', ' ', ' ', 'B', 'B', 'B' ],
        [ ' ', 'B', ' ', 'B', ' ', 'B', ' ', 'B', 'B', ' ', 'B', ' ', 'B', ' ', 'B', 'B', 'B', ' ', 'B', ' ' ],
        [ ' ', 'B', ' ', 'B', ' ', 'B', ' ', ' ', 'B', 'B', ' ', 'B', ' ', 'B', 'B', ' ', ' ', ' ', 'B', ' ' ],
        [ 'B', ' ', 'B', 'B', ' ', 'B', 'B', ' ', ' ', 'B', ' ', 'B', ' ', ' ', 'B', ' ', 'B', 'B', 'B', ' ' ],
        [ 'B', 'B', ' ', 'B', ' ', ' ', 'B', 'B', 'B', 'B', 'B', 'B', 'B', ' ', 'B', ' ', 'B', ' ', 'B', 'B' ],
        [ ' ', 'B', ' ', 'B', 'B', ' ', 'B', ' ', 'B', ' ', ' ', ' ', 'B', 'B', 'B', ' ', 'B', 'B', ' ', ' ' ],
        [ ' ', 'B', 'B', ' ', 'B', 'B', 'B', 'B', ' ', 'B', 'B', 'B', ' ', 'B', ' ', 'B', ' ', 'B', 'B', 'B' ],
        [ 'B', ' ', 'B', ' ', ' ', ' ', 'B', ' ', 'B', 'B', ' ', 'B', ' ', 'B', 'B', 'B', ' ', ' ', 'B', ' ' ],
        [ 'B', 'B', 'B', 'B', 'B', 'B', 'B', ' ', ' ', 'B', 'B', 'B', 'B', 'B', ' ', 'B', 'B', 'B', 'B', ' ' ],
    ])
    ground_assignment = {get_pos(x=x, y=y): 1 if ground[y][x] == 'B' else 0 for x in range(ground.shape[1]) for y in range(ground.shape[0])}
    assert set(solution.keys()) == set(ground_assignment.keys()), f'solution keys != ground assignment keys, {set(solution.keys()) ^ set(ground_assignment.keys())} \n\n\n{solution} \n\n\n{ground_assignment}'
    for pos in solution.keys():
        assert solution[pos] == ground_assignment[pos], f'solution[{pos}] != ground_assignment[{pos}], {solution[pos]} != {ground_assignment[pos]}'


if __name__ == '__main__':
    test_toy()
    test_ground()
