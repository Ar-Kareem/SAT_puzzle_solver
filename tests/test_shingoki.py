import numpy as np

from puzzle_solver import shingoki_solver as solver
from puzzle_solver.core.utils import Pos, get_all_pos, get_char, get_next_pos, Direction, in_bounds


def _ground_to_assignment(ground):
    res = {}
    for pos in get_all_pos(ground.shape[1], ground.shape[0]):
        cs = get_char(ground, pos).strip()
        if not cs:
            continue
        if 'L' in cs:
            left_p1 = pos
            left_p2 = get_next_pos(pos, Direction.DOWN)
            res[(left_p1, left_p2)] = 1
            res[(left_p2, left_p1)] = 1
        if 'U' in cs:
            up_p1 = pos
            up_p2 = get_next_pos(pos, Direction.RIGHT)
            res[(up_p1, up_p2)] = 1
            res[(up_p2, up_p1)] = 1
        if 'R' in cs:
            right_p1 = get_next_pos(pos, Direction.RIGHT)
            right_p2 = get_next_pos(right_p1, Direction.DOWN)
            res[(right_p1, right_p2)] = 1
            res[(right_p2, right_p1)] = 1
        if 'D' in cs:
            down_p1 = get_next_pos(pos, Direction.DOWN)
            down_p2 = get_next_pos(down_p1, Direction.RIGHT)
            res[(down_p1, down_p2)] = 1
            res[(down_p2, down_p1)] = 1
    for pos in get_all_pos(ground.shape[1]+1, ground.shape[0]+1):
        for direction in Direction:
            p1 = pos
            p2 = get_next_pos(p1, direction)
            if not in_bounds(p2, ground.shape[1]+1, ground.shape[0]+1):
                continue
            if (p1, p2) not in res:
                res[(p1, p2)] = 0
    return res


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
        [ '', 'LU', 'U', 'U', 'L' ],
        [ '', 'L', 'LU', 'L', 'L' ],
        [ '', 'L', 'L', 'L', 'RU' ],
        [ 'LU', '', 'L', 'L', 'LU' ],
        [ 'U', 'U', '', 'DL', 'DRU' ],
    ])
    ground_assignment = _ground_to_assignment(ground)
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
    ground = np.array([
        [ '', '', '', '', '', 'LU', 'U', 'U', 'L', 'LU', 'U', 'U', 'U', 'U', 'U', 'U', 'L', 'LU', 'L', 'LRU' ],
        [ 'LU', 'U', 'U', 'U', 'L', 'U', 'L', 'LU', '', 'L', 'LU', 'U', 'L', 'LU', 'U', 'U', '', 'L', 'U', 'R' ],
        [ 'U', 'L', 'LU', 'U', '', 'LU', '', 'U', 'L', 'L', 'U', 'L', 'U', '', '', 'LU', 'L', 'L', 'LU', 'LR' ],
        [ 'LU', '', 'U', 'L', '', 'U', 'U', 'L', 'L', 'L', 'LU', '', 'LU', 'L', 'LU', '', 'L', 'L', 'L', 'LR' ],
        [ 'U', 'U', 'L', 'U', 'L', 'LU', 'U', '', 'L', 'L', 'L', 'LU', '', 'U', '', 'LU', '', 'L', 'L', 'LR' ],
        [ 'LU', 'U', '', 'LU', '', 'U', 'U', 'L', 'U', '', 'U', '', 'LU', 'U', 'L', 'L', '', 'U', '', 'LR' ],
        [ 'U', 'L', 'LU', '', '', 'LU', 'L', 'U', 'U', 'U', 'U', 'U', '', '', 'L', 'U', 'U', 'U', 'L', 'LR' ],
        [ 'LU', '', 'L', '', 'LU', '', 'U', 'U', 'L', '', 'LU', 'U', 'U', 'L', 'U', 'L', 'LU', 'U', '', 'LR' ],
        [ 'L', 'LU', '', '', 'L', 'LU', 'U', 'L', 'U', 'U', '', 'LU', 'L', 'L', 'LU', '', 'U', 'L', '', 'LR' ],
        [ 'L', 'L', '', '', 'L', 'L', 'LU', '', 'LU', 'U', 'L', 'L', 'L', 'L', 'L', 'LU', 'L', 'L', '', 'LR' ],
        [ 'L', 'U', 'U', 'U', '', 'L', 'L', 'LU', '', '', 'L', 'L', 'L', 'L', 'L', 'L', 'L', 'U', 'U', 'R' ],
        [ 'U', 'U', 'U', 'L', 'LU', '', 'L', 'L', '', '', 'L', 'L', 'L', 'L', 'L', 'L', 'U', 'U', 'L', 'LU' ],
        [ 'LU', 'L', '', 'U', '', '', 'L', 'L', 'LU', 'L', 'L', 'L', 'L', 'U', '', 'L', 'LU', 'L', 'L', 'L' ],
        [ 'L', 'U', 'U', 'L', '', 'LU', '', 'L', 'L', 'L', 'L', 'L', 'U', 'L', '', 'U', '', 'L', 'L', 'RU' ],
        [ 'L', 'LU', 'L', 'L', '', 'U', 'U', '', 'L', 'U', '', 'L', 'LU', '', 'LU', 'U', 'L', 'L', 'U', 'LR' ],
        [ 'L', 'L', 'L', 'U', 'U', 'L', 'LU', 'L', 'U', 'U', 'U', '', 'U', 'L', 'L', '', 'L', 'L', 'LU', 'R' ],
        [ 'L', 'L', 'U', 'U', 'L', 'U', '', 'L', '', 'LU', 'L', '', '', 'L', 'L', '', 'U', '', 'L', 'LU' ],
        [ 'L', 'L', '', 'LU', '', 'LU', 'U', '', 'LU', '', 'U', 'U', 'U', '', 'U', 'L', 'LU', 'L', 'L', 'L' ],
        [ 'L', 'U', 'L', 'L', 'LU', '', '', 'LU', '', 'LU', 'U', 'U', 'L', 'LU', 'U', '', 'L', 'U', '', 'RU' ],
        [ 'U', 'DL', 'L', 'DL', 'DU', 'DU', 'DU', 'D', 'LU', '', 'DLU', 'DU', 'D', 'DU', 'DU', 'L', 'DL', 'LU', 'U', 'DLR' ],
    ])
    ground_assignment = _ground_to_assignment(ground)
    assert set(solution.keys()) == set(ground_assignment.keys()), f'solution keys != ground assignment keys, {set(solution.keys()) ^ set(ground_assignment.keys())} \n\n\n{solution} \n\n\n{ground_assignment}'
    for pos in solution.keys():
        assert solution[pos] == ground_assignment[pos], f'solution[{pos}] != ground_assignment[{pos}], {solution[pos]} != {ground_assignment[pos]}'


if __name__ == '__main__':
    test_small()
    test_small_normal()
    test_medium()
    test_ground()
