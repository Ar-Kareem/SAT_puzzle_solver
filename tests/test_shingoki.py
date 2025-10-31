import numpy as np
import pytest

from puzzle_solver import shingoki_solver as solver
from puzzle_solver.core.utils import get_pos


def _debug_print_assignment(assignment, V, H):
    res = np.array([[assignment[get_pos(x=c, y=r)] for c in range(H)] for r in range(V)])
    print('[')
    for row in res:
        row = [f"'{c}'" + ' ' * (2 - len(c)) for c in row]
        print("        [ " + ", ".join(row) + " ],")
    print('    ]')


def test_small():
    # 6 x 6 medium
    # https://www.puzzle-shingoki.com/?e=MToyLDk3Miw1MTQ=
    board = np.array([
        ['  ', '6B', '  ', '  ', '  ', '  '],
        ['  ', '  ', '  ', '  ', '2W', '  '],
        ['  ', '  ', '  ', '  ', '  ', '2B'],
        ['  ', '  ', '  ', '  ', '  ', '  '],
        ['3B', '  ', '  ', '  ', '  ', '  '],
        ['  ', '  ', '  ', '6B', '2W', '  '],
    ])
    binst = solver.Board(board=board)
    solutions = binst.solve_and_print()
    assert len(solutions) == 1, f'unique solutions != 1, == {len(solutions)}'
    solution = solutions[0].assignment
    ground = np.array([
        [ ''  , 'DR', 'LR', 'LR', 'DL', ''   ],
        [ ''  , 'UD', 'DR', 'DL', 'UD', ''   ],
        [ ''  , 'UD', 'UD', 'UD', 'UR', 'DL' ],
        [ 'DR', 'UL', 'UD', 'UD', 'DR', 'UL' ],
        [ 'UR', 'LR', 'UL', 'UD', 'UR', 'DL' ],
        [ ''  , ''  , ''  , 'UR', 'LR', 'UL' ],
    ])
    # _debug_print_assignment(solution, board.shape[0], board.shape[1])
    ground_assignment = {get_pos(x=x, y=y): ground[y][x] for x in range(ground.shape[1]) for y in range(ground.shape[0])}
    assert set(solution.keys()) == set(ground_assignment.keys()), f'solution keys != ground assignment keys, {set(solution.keys()) ^ set(ground_assignment.keys())} \n\n\n{solution} \n\n\n{ground_assignment}'
    for pos in solution.keys():
        assert solution[pos] == ground_assignment[pos], f'solution[{pos}] != ground_assignment[{pos}], {solution[pos]} != {ground_assignment[pos]}'


def test_small_normal():
    # 6 x 6 normal
    # https://www.puzzle-shingoki.com/?e=MToyLDM0OSw0NjY=
    board = np.array([
        ['  ', '  ', '  ', '  ', '  ', '  '],
        ['  ', '  ', '  ', '  ', '3W', '  '],
        ['  ', '  ', '  ', '3W', '  ', '  '],
        ['  ', '  ', '  ', '  ', '  ', '  '],
        ['  ', '  ', '4B', '  ', '  ', '  '],
        ['  ', '5B', '  ', '2B', '  ', '  '],
    ])
    binst = solver.Board(board=board)
    solutions = binst.solve_and_print()
    assert len(solutions) == 1, f'unique solutions != 1, == {len(solutions)}'
    solution = solutions[0].assignment
    # _debug_print_assignment(solution, board.shape[0], board.shape[1])
    ground = np.array([
        [ 'DR', 'LR', 'LR', 'DL', 'DR', 'DL' ],
        [ 'UD', 'DR', 'DL', 'UD', 'UD', 'UD' ],
        [ 'UD', 'UD', 'UD', 'UD', 'UD', 'UD' ],
        [ 'UD', 'UD', 'UD', 'UR', 'UL', 'UD' ],
        [ 'UD', 'UD', 'UR', 'DL', 'DR', 'UL' ],
        [ 'UR', 'UL', ''  , 'UR', 'UL', ''   ],
    ])
    ground_assignment = {get_pos(x=x, y=y): ground[y][x] for x in range(ground.shape[1]) for y in range(ground.shape[0])}
    assert set(solution.keys()) == set(ground_assignment.keys()), f'solution keys != ground assignment keys, {set(solution.keys()) ^ set(ground_assignment.keys())} \n\n\n{solution} \n\n\n{ground_assignment}'
    for pos in solution.keys():
        assert solution[pos] == ground_assignment[pos], f'solution[{pos}] != ground_assignment[{pos}], {solution[pos]} != {ground_assignment[pos]}'


def test_medium():
    # 8 x 8 hard
    # https://www.puzzle-shingoki.com/?e=NDoxLDU0NCwwNzc=
    board = np.array([
        ['  ', '  ', '  ', '  ', '5W', '  ', '  ', '  '],
        ['  ', '  ', '  ', '  ', '4B', '  ', '2B', '  '],
        ['  ', '2B', '2B', '  ', '  ', '  ', '3W', '  '],
        ['  ', '  ', '  ', '  ', '2B', '  ', '  ', '5B'],
        ['  ', '  ', '  ', '3B', '  ', '  ', '  ', '  '],
        ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  '],
        ['  ', '2W', '  ', '  ', '  ', '3W', '  ', '  '],
        ['  ', '  ', '  ', '  ', '  ', '7W', '  ', '  '],
    ])
    binst = solver.Board(board=board)
    solutions = binst.solve_and_print()
    assert len(solutions) == 1, f'unique solutions != 1, == {len(solutions)}'
    solution = solutions[0].assignment
    # _debug_print_assignment(solution, board.shape[0], board.shape[1])
    ground = np.array([
        [ 'DR', 'LR', 'LR', 'LR', 'LR', 'DL', 'DR', 'DL' ],
        [ 'UD', 'DR', 'LR', 'LR', 'DL', 'UR', 'UL', 'UD' ],
        [ 'UD', 'UR', 'DL', ''  , 'UR', 'LR', 'LR', 'UL' ],
        [ 'UD', 'DR', 'UL', 'DR', 'DL', ''  , 'DR', 'DL' ],
        [ 'UD', 'UR', 'LR', 'UL', 'UR', 'DL', 'UD', 'UD' ],
        [ 'UR', 'LR', 'DL', 'DR', 'LR', 'UL', 'UD', 'UD' ],
        [ 'DR', 'LR', 'UL', 'UR', 'LR', 'LR', 'UL', 'UD' ],
        [ 'UR', 'LR', 'LR', 'LR', 'LR', 'LR', 'LR', 'UL' ],
    ])
    ground_assignment = {get_pos(x=x, y=y): ground[y][x] for x in range(ground.shape[1]) for y in range(ground.shape[0])}
    assert set(solution.keys()) == set(ground_assignment.keys()), f'solution keys != ground assignment keys, {set(solution.keys()) ^ set(ground_assignment.keys())} \n\n\n{solution} \n\n\n{ground_assignment}'
    for pos in solution.keys():
        assert solution[pos] == ground_assignment[pos], f'solution[{pos}] != ground_assignment[{pos}], {solution[pos]} != {ground_assignment[pos]}'


@pytest.mark.slow
def test_ground():
    # 21 x 21 hard
    # https://www.puzzle-shingoki.com/?e=MTM6Niw3NDgsODc0
    board = np.array([
        ['  ', '  ', '  ', '  ', '  ', '4B', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  '],
        ['  ', '  ', '  ', '  ', '5B', '  ', '  ', '2B', '  ', '  ', '3B', '  ', '  ', '  ', '3W', '  ', '  ', '  ', '  ', '2B', '  '],
        ['2B', '2B', '  ', '2W', '  ', '  ', '  ', '  ', '  ', '  ', '2B', '  ', '2B', '  ', '  ', '  ', '3B', '5W', '  ', '  ', '11W'],
        ['  ', '  ', '  ', '  ', '  ', '3B', '  ', '3B', '  ', '  ', '  ', '  ', '2B', '  ', '  ', '  ', '  ', '  ', '3W', '  ', '  '],
        ['  ', '2W', '  ', '  ', '2B', '  ', '2W', '  ', '3W', '  ', '2W', '2B', '2B', '  ', '  ', '  ', '  ', '  ', '  ', '8W', '  '],
        ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '6B', '  ', '  ', '  ', '  ', '4B', '2W', '  ', '  ', '  ', '  ', '  '],
        ['  ', '  ', '  ', '2B', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '2W', '  ', '  ', '  ', '4B', '  ', '  '],
        ['  ', '2B', '2W', '  ', '  ', '  ', '3B', '  ', '  ', '  ', '  ', '3W', '  ', '  ', '  ', '  ', '  ', '  ', '3B', '  ', '  '],
        ['4W', '3B', '  ', '  ', '3W', '  ', '  ', '  ', '  ', '  ', '3B', '  ', '6B', '  ', '  ', '  ', '2B', '  ', '  ', '  ', '  '],
        ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '2W', '7B', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  '],
        ['  ', '  ', '  ', '3W', '  ', '3W', '4W', '5B', '  ', '  ', '  ', '  ', '5W', '  ', '4W', '  ', '  ', '  ', '2W', '  ', '  '],
        ['7B', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '3B', '  '],
        ['  ', '  ', '  ', '  ', '2B', '  ', '4W', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '5B', '  ', '  ', '  '],
        ['  ', '  ', '2W', '  ', '  ', '2B', '  ', '4W', '3W', '  ', '  ', '  ', '  ', '  ', '  ', '5B', '2B', '  ', '3W', '  ', '  '],
        ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '3B', '  ', '7W', '  ', '2B', '5B', '  ', '  ', '  ', '  ', '  ', '  '],
        ['  ', '  ', '  ', '  ', '  ', '3B', '2B', '  ', '  ', '  ', '3W', '  ', '2B', '  ', '  ', '  ', '2W', '  ', '  ', '  ', '  '],
        ['  ', '  ', '  ', '2W', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '3B', '  '],
        ['  ', '4W', '  ', '  ', '2B', '3B', '  ', '  ', '  ', '2B', '4B', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '3W', '  ', '  '],
        ['7W', '  ', '3B', '  ', '  ', '2B', '  ', '  ', '  ', '4B', '  ', '  ', '  ', '  ', '2W', '3B', '  ', '2B', '  ', '  ', '  '],
        ['  ', '  ', '  ', '3W', '  ', '3W', '  ', '  ', '2B', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '3W', '  ', '2W', '  ', '  '],
        ['  ', '2B', '  ', '  ', '  ', '  ', '5W', '  ', '  ', '  ', '  ', '5W', '  ', '  ', '  ', '6B', '  ', '  ', '  ', '  ', '  '],
    ])
    binst = solver.Board(board=board)
    solutions = binst.solve_and_print()
    assert len(solutions) == 1, f'unique solutions != 1, == {len(solutions)}'
    solution = solutions[0].assignment
    # _debug_print_assignment(solution, board.shape[0], board.shape[1])
    ground = np.array([
        [ ''  , ''  , ''  , ''  , ''  , 'DR', 'LR', 'LR', 'DL', 'DR', 'LR', 'LR', 'LR', 'LR', 'LR', 'LR', 'DL', 'DR', 'DL', 'DR', 'DL' ],
        [ 'DR', 'LR', 'LR', 'LR', 'DL', 'UR', 'DL', 'DR', 'UL', 'UD', 'DR', 'LR', 'DL', 'DR', 'LR', 'LR', 'UL', 'UD', 'UR', 'UL', 'UD' ],
        [ 'UR', 'DL', 'DR', 'LR', 'UL', 'DR', 'UL', 'UR', 'DL', 'UD', 'UR', 'DL', 'UR', 'UL', ''  , 'DR', 'DL', 'UD', 'DR', 'DL', 'UD' ],
        [ 'DR', 'UL', 'UR', 'DL', ''  , 'UR', 'LR', 'DL', 'UD', 'UD', 'DR', 'UL', 'DR', 'DL', 'DR', 'UL', 'UD', 'UD', 'UD', 'UD', 'UD' ],
        [ 'UR', 'LR', 'DL', 'UR', 'DL', 'DR', 'LR', 'UL', 'UD', 'UD', 'UD', 'DR', 'UL', 'UR', 'UL', 'DR', 'UL', 'UD', 'UD', 'UD', 'UD' ],
        [ 'DR', 'LR', 'UL', 'DR', 'UL', 'UR', 'LR', 'DL', 'UR', 'UL', 'UR', 'UL', 'DR', 'LR', 'DL', 'UD', ''  , 'UR', 'UL', 'UD', 'UD' ],
        [ 'UR', 'DL', 'DR', 'UL', ''  , 'DR', 'DL', 'UR', 'LR', 'LR', 'LR', 'LR', 'UL', ''  , 'UD', 'UR', 'LR', 'LR', 'DL', 'UD', 'UD' ],
        [ 'DR', 'UL', 'UD', ''  , 'DR', 'UL', 'UR', 'LR', 'DL', ''  , 'DR', 'LR', 'LR', 'DL', 'UR', 'DL', 'DR', 'LR', 'UL', 'UD', 'UD' ],
        [ 'UD', 'DR', 'UL', ''  , 'UD', 'DR', 'LR', 'DL', 'UR', 'LR', 'UL', 'DR', 'DL', 'UD', 'DR', 'UL', 'UR', 'DL', ''  , 'UD', 'UD' ],
        [ 'UD', 'UD', ''  , ''  , 'UD', 'UD', 'DR', 'UL', 'DR', 'LR', 'DL', 'UD', 'UD', 'UD', 'UD', 'DR', 'DL', 'UD', ''  , 'UD', 'UD' ],
        [ 'UD', 'UR', 'LR', 'LR', 'UL', 'UD', 'UD', 'DR', 'UL', ''  , 'UD', 'UD', 'UD', 'UD', 'UD', 'UD', 'UD', 'UR', 'LR', 'UL', 'UD' ],
        [ 'UR', 'LR', 'LR', 'DL', 'DR', 'UL', 'UD', 'UD', ''  , ''  , 'UD', 'UD', 'UD', 'UD', 'UD', 'UD', 'UR', 'LR', 'DL', 'DR', 'UL' ],
        [ 'DR', 'DL', ''  , 'UR', 'UL', ''  , 'UD', 'UD', 'DR', 'DL', 'UD', 'UD', 'UD', 'UR', 'UL', 'UD', 'DR', 'DL', 'UD', 'UD', ''   ],
        [ 'UD', 'UR', 'LR', 'DL', ''  , 'DR', 'UL', 'UD', 'UD', 'UD', 'UD', 'UD', 'UR', 'DL', ''  , 'UR', 'UL', 'UD', 'UD', 'UR', 'DL' ],
        [ 'UD', 'DR', 'DL', 'UD', ''  , 'UR', 'LR', 'UL', 'UD', 'UR', 'UL', 'UD', 'DR', 'UL', 'DR', 'LR', 'DL', 'UD', 'UR', 'DL', 'UD' ],
        [ 'UD', 'UD', 'UD', 'UR', 'LR', 'DL', 'DR', 'DL', 'UR', 'LR', 'LR', 'UL', 'UR', 'DL', 'UD', ''  , 'UD', 'UD', 'DR', 'UL', 'UD' ],
        [ 'UD', 'UD', 'UR', 'LR', 'DL', 'UR', 'UL', 'UD', ''  , 'DR', 'DL', ''  , ''  , 'UD', 'UD', ''  , 'UR', 'UL', 'UD', 'DR', 'UL' ],
        [ 'UD', 'UD', ''  , 'DR', 'UL', 'DR', 'LR', 'UL', 'DR', 'UL', 'UR', 'LR', 'LR', 'UL', 'UR', 'DL', 'DR', 'DL', 'UD', 'UD', ''   ],
        [ 'UD', 'UR', 'DL', 'UD', 'DR', 'UL', ''  , 'DR', 'UL', 'DR', 'LR', 'LR', 'DL', 'DR', 'LR', 'UL', 'UD', 'UR', 'UL', 'UR', 'DL' ],
        [ 'UR', 'DL', 'UD', 'UD', 'UR', 'LR', 'LR', 'UL', 'DR', 'UL', 'DR', 'LR', 'UL', 'UR', 'LR', 'DL', 'UD', 'DR', 'LR', 'DL', 'UD' ],
        [ ''  , 'UR', 'UL', 'UR', 'LR', 'LR', 'LR', 'LR', 'UL', ''  , 'UR', 'LR', 'LR', 'LR', 'LR', 'UL', 'UR', 'UL', ''  , 'UR', 'UL' ],
    ])
    ground_assignment = {get_pos(x=x, y=y): ground[y][x] for x in range(ground.shape[1]) for y in range(ground.shape[0])}
    assert set(solution.keys()) == set(ground_assignment.keys()), f'solution keys != ground assignment keys, {set(solution.keys()) ^ set(ground_assignment.keys())} \n\n\n{solution} \n\n\n{ground_assignment}'
    for pos in solution.keys():
        assert solution[pos] == ground_assignment[pos], f'solution[{pos}] != ground_assignment[{pos}], {solution[pos]} != {ground_assignment[pos]}'


if __name__ == '__main__':
    test_small()
    test_small_normal()
    test_medium()
    test_ground()
