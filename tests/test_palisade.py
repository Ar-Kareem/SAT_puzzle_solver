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
        [1, 1, 1],
        [2, 2, 2],
        [3, 3, 3],
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
        [7, 7, 7],
        [7, 14, 11],
        [14, 14, 11],
        [14, 11, 11],
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
        [194, 194, 194, 194, 194],
        [243, 243, 243, 243, 185],
        [169, 243, 169, 185, 185],
        [169, 169, 169, 86, 185],
        [86, 86, 86, 86, 185],
    ])
    
    
    ground_assignment = {get_pos(x=x, y=y): ground[y][x] for x in range(ground.shape[1]) for y in range(ground.shape[0])}
    assert set(solution.keys()) == set(ground_assignment.keys()), f'solution keys != ground assignment keys, {set(solution.keys()) ^ set(ground_assignment.keys())} \n\n\n{solution} \n\n\n{ground_assignment}'
    for pos in solution.keys():
        assert solution[pos] == ground_assignment[pos], f'solution[{pos}] != ground_assignment[{pos}], {solution[pos]} != {ground_assignment[pos]}'


def test_ground():
    # 15 x 12
    # https://www.chiark.greenend.org.uk/~sgtatham/puzzles/js/palisade.html#15x12n10%23238133276724374
    board = np.array([
        ['2', ' ', ' ', ' ', ' ', '3', ' ', ' ', '1', '1', '3', ' ', ' ', ' ', ' '],
        ['3', '2', '1', ' ', '2', '3', ' ', ' ', ' ', ' ', ' ', '2', ' ', '0', ' '],
        [' ', ' ', ' ', '1', '1', ' ', ' ', '1', ' ', ' ', ' ', '1', ' ', ' ', ' '],
        [' ', '3', '2', ' ', ' ', ' ', ' ', '2', '3', ' ', ' ', ' ', '1', ' ', ' '],
        [' ', '0', '1', ' ', '2', ' ', ' ', '0', ' ', ' ', ' ', '1', ' ', '3', '2'],
        ['1', '0', ' ', ' ', ' ', '2', '2', ' ', '2', ' ', '3', ' ', '0', '2', ' '],
        [' ', ' ', ' ', ' ', ' ', '3', ' ', ' ', ' ', '2', ' ', ' ', ' ', ' ', ' '],
        [' ', '1', ' ', ' ', ' ', '3', '1', ' ', '1', ' ', ' ', ' ', ' ', '1', ' '],
        [' ', ' ', ' ', '0', ' ', ' ', '0', ' ', ' ', '1', '2', ' ', ' ', ' ', '3'],
        [' ', ' ', ' ', ' ', ' ', ' ', '1', ' ', ' ', '2', ' ', ' ', '1', '2', '1'],
        [' ', ' ', ' ', ' ', '1', ' ', '2', '3', '1', ' ', ' ', ' ', '2', ' ', '1'],
        ['2', ' ', '1', ' ', '2', '2', '1', ' ', ' ', '2', ' ', ' ', ' ', ' ', ' '],
    ])
    binst = solver.Board(board, region_size=10)
    solutions = binst.solve_and_print()
    assert len(solutions) == 1, f'unique solutions != 1, == {len(solutions)}'
    solution = solutions[0].assignment
    ground = np.array([
        [63217, 63217, 63217, 63217, 63217, 46629, 46629, 46629, 46629, 46629, 46629, 23802, 23802, 23802, 23802],
        [63217, 71104, 71104, 71104, 63217, 124980, 124980, 1479, 46629, 46629, 91358, 91358, 23802, 23802, 23802],
        [71104, 71104, 71104, 71104, 63217, 63217, 124980, 1479, 1479, 46629, 46629, 91358, 91358, 23802, 23802],
        [71104, 10323, 71104, 71104, 63217, 124980, 124980, 1479, 91358, 91358, 91358, 91358, 91358, 91358, 23802],
        [10323, 10323, 10323, 10323, 124980, 124980, 1479, 1479, 1479, 15340, 15340, 15340, 15340, 30123, 30123],
        [10323, 10323, 10323, 124980, 124980, 124980, 1479, 1479, 1479, 15340, 11463, 15340, 15340, 15340, 30123],
        [10323, 10323, 45540, 45540, 45540, 45540, 128365, 120174, 120174, 120174, 11463, 30123, 15340, 15340, 30123],
        [45540, 45540, 45540, 5910, 5910, 5910, 128365, 128365, 120174, 120174, 11463, 30123, 30123, 30123, 30123],
        [45540, 45540, 5910, 5910, 5910, 128365, 128365, 128365, 120174, 120174, 11463, 11463, 11463, 30123, 57371],
        [45540, 5910, 5910, 5910, 40045, 128365, 128365, 128365, 85455, 120174, 120174, 11463, 11463, 57371, 57371],
        [40045, 5910, 40045, 40045, 40045, 85455, 85455, 128365, 85455, 85455, 120174, 11463, 11463, 57371, 57371],
        [40045, 40045, 40045, 40045, 40045, 85455, 85455, 85455, 85455, 85455, 57371, 57371, 57371, 57371, 57371],
    ])
    ground_assignment = {get_pos(x=x, y=y): ground[y][x] for x in range(ground.shape[1]) for y in range(ground.shape[0])}
    assert set(solution.keys()) == set(ground_assignment.keys()), f'solution keys != ground assignment keys, {set(solution.keys()) ^ set(ground_assignment.keys())} \n\n\n{solution} \n\n\n{ground_assignment}'
    for pos in solution.keys():
        assert solution[pos] == ground_assignment[pos], f'solution[{pos}] != ground_assignment[{pos}], {solution[pos]} != {ground_assignment[pos]}'


def test_ground_2():
    # 10 x 8
    # https://www.chiark.greenend.org.uk/~sgtatham/puzzles/js/palisade.html#10x8n8%23517510531477622
    board = np.array([
        [' ', ' ', ' ', '1', ' ', '1', ' ', ' ', ' ', ' '],
        [' ', '0', '2', ' ', '1', ' ', ' ', '2', ' ', '1'],
        ['2', ' ', ' ', '3', '3', '3', '1', '1', ' ', ' '],
        [' ', ' ', ' ', ' ', '1', ' ', '1', ' ', ' ', ' '],
        [' ', ' ', '1', ' ', '3', ' ', ' ', '3', ' ', ' '],
        [' ', ' ', ' ', '0', ' ', ' ', ' ', '1', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', '1', '2', '2', '1', ' '],
        ['3', '1', '2', ' ', ' ', '3', ' ', ' ', ' ', ' '],
    ])
    binst = solver.Board(board, region_size=8)
    solutions = binst.solve_and_print()
    assert len(solutions) == 1, f'unique solutions != 1, == {len(solutions)}'
    solution = solutions[0].assignment
    ground = np.array([
        [1993, 1993, 874, 874, 874, 874, 874, 331, 331, 331],
        [1993, 1993, 1993, 874, 874, 874, 778, 778, 331, 331],
        [1993, 1993, 1993, 2951, 1642, 778, 778, 778, 778, 331],
        [2951, 2951, 2951, 2951, 1642, 1642, 1642, 1642, 778, 331],
        [2951, 2512, 2512, 2512, 1642, 3632, 1642, 3910, 778, 331],
        [2951, 2582, 2512, 2512, 2512, 3632, 1642, 3910, 3910, 3910],
        [2951, 2582, 2512, 2512, 3632, 3632, 3632, 3910, 3910, 3910],
        [2582, 2582, 2582, 2582, 2582, 2582, 3632, 3632, 3632, 3910],
    ])
    ground_assignment = {get_pos(x=x, y=y): ground[y][x] for x in range(ground.shape[1]) for y in range(ground.shape[0])}
    assert set(solution.keys()) == set(ground_assignment.keys()), f'solution keys != ground assignment keys, {set(solution.keys()) ^ set(ground_assignment.keys())} \n\n\n{solution} \n\n\n{ground_assignment}'
    for pos in solution.keys():
        assert solution[pos] == ground_assignment[pos], f'solution[{pos}] != ground_assignment[{pos}], {solution[pos]} != {ground_assignment[pos]}'


if __name__ == '__main__':
    test_toy()
    test_easy()
    test_easy_2()
    test_ground_2()
    test_ground()
