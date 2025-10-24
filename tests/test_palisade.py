import numpy as np

from puzzle_solver import palisade_solver as solver
from puzzle_solver.core.utils import get_pos


def test_toy():
    board = np.array([
        ['3', '2', '3'],
        ['3', '2', '3'],
        [' ', ' ', ' ']
    ])
    binst = solver.Board(board, region_size=3)
    solutions = binst.solve_and_print()
    assert len(solutions) == 1, f'unique solutions != 1, == {len(solutions)}'
    solution = solutions[0].assignment
    ground = np.array([
        [0, 0, 0],
        [1, 1, 1],
        [2, 2, 2],
    ])
    ground_assignment = {get_pos(x=x, y=y): ground[y][x] for x in range(ground.shape[1]) for y in range(ground.shape[0])}
    assert set(solution.keys()) == set(ground_assignment.keys()), f'solution keys != ground assignment keys, {set(solution.keys()) ^ set(ground_assignment.keys())} \n\n\n{solution} \n\n\n{ground_assignment}'
    for pos in solution.keys():
        assert solution[pos] == ground_assignment[pos], f'solution[{pos}] != ground_assignment[{pos}], {solution[pos]} != {ground_assignment[pos]}'


def test_easy():
    board = np.array([
        ['2', ' ', ' '],
        ['3', ' ', ' '],
        ['2', ' ', ' '],
        [' ', '3', ' '],
    ])
    binst = solver.Board(board, region_size=4)
    solutions = binst.solve_and_print()
    assert len(solutions) == 1, f'unique solutions != 1, == {len(solutions)}'
    solution = solutions[0].assignment
    ground = np.array([
        [0, 0, 0],
        [0, 1, 2],
        [1, 1, 2],
        [1, 2, 2],
    ])
    ground_assignment = {get_pos(x=x, y=y): ground[y][x] for x in range(ground.shape[1]) for y in range(ground.shape[0])}
    assert set(solution.keys()) == set(ground_assignment.keys()), f'solution keys != ground assignment keys, {set(solution.keys()) ^ set(ground_assignment.keys())} \n\n\n{solution} \n\n\n{ground_assignment}'
    for pos in solution.keys():
        assert solution[pos] == ground_assignment[pos], f'solution[{pos}] != ground_assignment[{pos}], {solution[pos]} != {ground_assignment[pos]}'


def test_easy_2():
    board = np.array([
        ['3', ' ', ' ', ' ', ' '],
        ['3', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', '1'],
        ['2', ' ', '2', '3', '2'],
        [' ', ' ', ' ', '2', ' '],
    ])
    binst = solver.Board(board, region_size=5)
    solutions = binst.solve_and_print()
    assert len(solutions) == 1, f'unique solutions != 1, == {len(solutions)}'
    solution = solutions[0].assignment
    ground = np.array([
        [0, 0, 0, 0, 0],
        [1, 1, 1, 1, 2],
        [3, 1, 3, 2, 2],
        [3, 3, 3, 4, 2],
        [4, 4, 4, 4, 2],
    ])
    ground_assignment = {get_pos(x=x, y=y): ground[y][x] for x in range(ground.shape[1]) for y in range(ground.shape[0])}
    assert set(solution.keys()) == set(ground_assignment.keys()), f'solution keys != ground assignment keys, {set(solution.keys()) ^ set(ground_assignment.keys())} \n\n\n{solution} \n\n\n{ground_assignment}'
    for pos in solution.keys():
        assert solution[pos] == ground_assignment[pos], f'solution[{pos}] != ground_assignment[{pos}], {solution[pos]} != {ground_assignment[pos]}'


# def test_ground():
#     # 15 x 12
#     # https://www.chiark.greenend.org.uk/~sgtatham/puzzles/js/palisade.html#15x12n10%23238133276724374
#     board = np.array([
#         ['2', ' ', ' ', ' ', ' ', '3', ' ', ' ', '1', '1', '3', ' ', ' ', ' ', ' '],
#         ['3', '2', '1', ' ', '2', '3', ' ', ' ', ' ', ' ', ' ', '2', ' ', '0', ' '],
#         [' ', ' ', ' ', '1', '1', ' ', ' ', '1', ' ', ' ', ' ', '1', ' ', ' ', ' '],
#         [' ', '3', '2', ' ', ' ', ' ', ' ', '2', '3', ' ', ' ', ' ', '1', ' ', ' '],
#         [' ', '0', '1', ' ', '2', ' ', ' ', '0', ' ', ' ', ' ', '1', ' ', '3', '2'],
#         ['1', '0', ' ', ' ', ' ', '2', '2', ' ', '2', ' ', '3', ' ', '0', '2', ' '],
#         [' ', ' ', ' ', ' ', ' ', '3', ' ', ' ', ' ', '2', ' ', ' ', ' ', ' ', ' '],
#         [' ', '1', ' ', ' ', ' ', '3', '1', ' ', '1', ' ', ' ', ' ', ' ', '1', ' '],
#         [' ', ' ', ' ', '0', ' ', ' ', '0', ' ', ' ', '1', '2', ' ', ' ', ' ', '3'],
#         [' ', ' ', ' ', ' ', ' ', ' ', '1', ' ', ' ', '2', ' ', ' ', '1', '2', '1'],
#         [' ', ' ', ' ', ' ', '1', ' ', '2', '3', '1', ' ', ' ', ' ', '2', ' ', '1'],
#         ['2', ' ', '1', ' ', '2', '2', '1', ' ', ' ', '2', ' ', ' ', ' ', ' ', ' '],
#     ])
#     binst = solver.Board(board, region_size=10)
#     solutions = binst.solve_and_print()
#     assert len(solutions) == 1, f'unique solutions != 1, == {len(solutions)}'
#     solution = solutions[0].assignment





if __name__ == '__main__':
    test_toy()
    test_easy()
    test_easy_2()
    # test_ground()
