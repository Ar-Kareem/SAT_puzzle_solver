import numpy as np

from puzzle_solver import binairo_plus_solver as solver
from puzzle_solver.core.utils import get_pos

def test_easy():
    # 6x6 easy
    # https://www.puzzle-binairo.com/binairo-plus-6x6-easy/?e=MTM6Nyw3NDcsNjMz
    board = np.array([
        ['B', ' ', ' ', ' ', ' ', 'W'],
        [' ', ' ', ' ', ' ', ' ', ' '],
        ['B', ' ', ' ', ' ', ' ', 'W'],
        ['B', ' ', ' ', ' ', ' ', 'B'],
        [' ', ' ', ' ', ' ', ' ', ' '],
        ['W', ' ', ' ', ' ', ' ', 'B'],
    ])
    arith_rows = np.array([
        [' ', ' ', '=', ' ', ' '],
        [' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' '],
        [' ', '=', ' ', 'x', ' '],
        [' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' '],
    ])
    arith_cols = np.array([
        [' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', 'x', 'x', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' '],
        [' ', 'x', ' ', ' ', 'x', ' '],
    ])
    binst = solver.Board(board=board, arith_rows=arith_rows, arith_cols=arith_cols)
    solutions = binst.solve_and_print()
    assert len(solutions) == 1, f'unique solutions != 1, == {len(solutions)}'
    solution = solutions[0].assignment
    ground = np.array([
        ['B', 'B', ' ', ' ', 'B', ' '],
        [' ', 'B', ' ', 'B', ' ', 'B'],
        ['B', ' ', 'B', ' ', 'B', ' '],
        ['B', ' ', ' ', 'B', ' ', 'B'],
        [' ', 'B', 'B', ' ', 'B', ' '],
        [' ', ' ', 'B', 'B', ' ', 'B'],
    ])
    ground_assignment = {get_pos(x=x, y=y): 1 if ground[y][x] == 'B' else 0 for x in range(ground.shape[1]) for y in range(ground.shape[0])}
    assert set(solution.keys()) == set(ground_assignment.keys()), f'solution keys != ground assignment keys, {set(solution.keys()) ^ set(ground_assignment.keys())} \n\n\n{solution} \n\n\n{ground_assignment}'
    for pos in solution.keys():
        assert solution[pos] == ground_assignment[pos], f'solution[{pos}] != ground_assignment[{pos}], {solution[pos]} != {ground_assignment[pos]}'


def test_easy_2():
    # 8x8 hard
    # https://www.puzzle-binairo.com/binairo-plus-8x8-hard/?e=MTY6Myw4NzMsNzA3
    board = np.array([
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', 'B', 'B', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        ['B', ' ', 'B', ' ', ' ', 'W', ' ', 'B'],
        ['W', ' ', 'W', ' ', ' ', 'B', ' ', 'B'],
        [' ', 'B', ' ', 'W', 'B', ' ', 'B', ' '],
    ])
    arith_rows = np.array([
        [' ', 'x', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', 'x', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', '=', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' '],
    ])
    arith_cols = np.array([
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', '='],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', 'x', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', 'x'],
        [' ', ' ', ' ', 'x', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    ])
    binst = solver.Board(board=board, arith_rows=arith_rows, arith_cols=arith_cols)
    solutions = binst.solve_and_print()
    assert len(solutions) == 1, f'unique solutions != 1, == {len(solutions)}'
    solution = solutions[0].assignment
    ground = np.array([
        ['B', ' ', 'B', ' ', ' ', 'B', 'B', ' '],
        ['B', ' ', ' ', 'B', 'B', ' ', 'B', ' '],
        [' ', 'B', 'B', ' ', ' ', 'B', ' ', 'B'],
        ['B', ' ', ' ', 'B', 'B', ' ', ' ', 'B'],
        [' ', 'B', ' ', 'B', ' ', 'B', 'B', ' '],
        ['B', ' ', 'B', ' ', 'B', ' ', ' ', 'B'],
        [' ', 'B', ' ', 'B', ' ', 'B', ' ', 'B'],
        [' ', 'B', 'B', ' ', 'B', ' ', 'B', ' '],
    ])
    ground_assignment = {get_pos(x=x, y=y): 1 if ground[y][x] == 'B' else 0 for x in range(ground.shape[1]) for y in range(ground.shape[0])}
    assert set(solution.keys()) == set(ground_assignment.keys()), f'solution keys != ground assignment keys, {set(solution.keys()) ^ set(ground_assignment.keys())} \n\n\n{solution} \n\n\n{ground_assignment}'
    for pos in solution.keys():
        assert solution[pos] == ground_assignment[pos], f'solution[{pos}] != ground_assignment[{pos}], {solution[pos]} != {ground_assignment[pos]}'

def test_ground():
    # 14 x 14 hard
    # https://www.puzzle-binairo.com/binairo-plus-14x14-hard/?e=MjA6OSw1MDcsMjA0
    board = np.array([
        [' ', ' ', 'W', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'B', ' ', ' '],
        ['B', ' ', ' ', ' ', 'W', ' ', ' ', ' ', ' ', 'B', ' ', ' ', ' ', 'B'],
        [' ', ' ', ' ', ' ', ' ', 'W', ' ', ' ', 'W', ' ', ' ', ' ', ' ', ' '],
        ['B', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'W'],
        [' ', ' ', ' ', 'B', ' ', ' ', ' ', ' ', ' ', ' ', 'B', ' ', ' ', ' '],
        ['W', ' ', 'B', ' ', 'W', ' ', ' ', ' ', ' ', 'W', ' ', 'B', ' ', 'B'],
        [' ', ' ', 'W', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'B', ' ', ' '],
        [' ', ' ', 'B', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'W', ' ', ' '],
        ['B', ' ', 'W', ' ', 'B', ' ', ' ', ' ', ' ', 'W', ' ', 'W', ' ', 'B'],
        [' ', ' ', ' ', 'B', ' ', ' ', ' ', ' ', ' ', ' ', 'W', ' ', ' ', ' '],
        ['W', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'B'],
        [' ', ' ', ' ', ' ', ' ', 'W', ' ', ' ', 'W', ' ', ' ', ' ', ' ', ' '],
        ['W', ' ', ' ', ' ', 'W', ' ', ' ', ' ', ' ', 'B', ' ', ' ', ' ', 'W'],
        [' ', ' ', 'B', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'W', ' ', ' '],
    ])
    # between cells horizontally
    arith_rows = np.array([
        [' ', ' ', ' ', '=', ' ', 'x', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', '=', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', 'x', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        ['x', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', '=', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', '=', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '=', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', 'x', 'x', ' ', ' ', ' ', 'x', ' ', ' ', ' ', ' '],
    ])
    # between cells vertically
    arith_cols = np.array([
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', '=', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', '=', ' ', '=', ' ', ' ', 'x', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', 'x', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', 'x', '=', ' ', '=', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', '=', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '=', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', '=', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', '=', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', 'x', ' ', ' ', ' ', ' ', ' ', 'x', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', '=', ' ', 'x', ' ', ' ', ' ', 'x', ' '],
    ])
    binst = solver.Board(board=board, arith_rows=arith_rows, arith_cols=arith_cols)
    solutions = binst.solve_and_print()
    assert len(solutions) == 1, f'unique solutions != 1, == {len(solutions)}'
    solution = solutions[0].assignment
    ground = np.array([
        ['B', ' ', ' ', 'B', 'B', ' ', 'B', 'B', ' ', ' ', 'B', 'B', ' ', ' '],
        ['B', ' ', ' ', 'B', ' ', 'B', ' ', ' ', 'B', 'B', ' ', ' ', 'B', 'B'],
        [' ', 'B', 'B', ' ', 'B', ' ', ' ', 'B', ' ', ' ', 'B', ' ', 'B', 'B'],
        ['B', 'B', ' ', ' ', 'B', ' ', 'B', ' ', 'B', 'B', ' ', 'B', ' ', ' '],
        ['B', ' ', ' ', 'B', ' ', 'B', 'B', ' ', ' ', 'B', 'B', ' ', 'B', ' '],
        [' ', 'B', 'B', ' ', ' ', 'B', ' ', 'B', 'B', ' ', ' ', 'B', ' ', 'B'],
        [' ', 'B', ' ', ' ', 'B', ' ', 'B', ' ', 'B', 'B', ' ', 'B', 'B', ' '],
        ['B', ' ', 'B', 'B', ' ', ' ', 'B', 'B', ' ', ' ', 'B', ' ', 'B', ' '],
        ['B', 'B', ' ', ' ', 'B', 'B', ' ', 'B', ' ', ' ', 'B', ' ', ' ', 'B'],
        [' ', ' ', 'B', 'B', ' ', 'B', ' ', ' ', 'B', 'B', ' ', 'B', 'B', ' '],
        [' ', 'B', 'B', ' ', 'B', ' ', 'B', ' ', 'B', ' ', ' ', 'B', ' ', 'B'],
        ['B', 'B', ' ', ' ', 'B', ' ', 'B', 'B', ' ', ' ', 'B', ' ', ' ', 'B'],
        [' ', ' ', 'B', 'B', ' ', 'B', ' ', ' ', 'B', 'B', ' ', 'B', 'B', ' '],
        [' ', ' ', 'B', 'B', ' ', 'B', ' ', 'B', ' ', 'B', 'B', ' ', ' ', 'B'],
    ])
    ground_assignment = {get_pos(x=x, y=y): 1 if ground[y][x] == 'B' else 0 for x in range(ground.shape[1]) for y in range(ground.shape[0])}
    assert set(solution.keys()) == set(ground_assignment.keys()), f'solution keys != ground assignment keys, {set(solution.keys()) ^ set(ground_assignment.keys())} \n\n\n{solution} \n\n\n{ground_assignment}'
    for pos in solution.keys():
        assert solution[pos] == ground_assignment[pos], f'solution[{pos}] != ground_assignment[{pos}], {solution[pos]} != {ground_assignment[pos]}'



if __name__ == '__main__':
    test_easy()
    test_easy_2()
    test_ground()
