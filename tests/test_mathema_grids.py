import numpy as np
from puzzle_solver import mathema_grids_solver as solver
from puzzle_solver.core.utils import Pos


def test_toy():
    board = np.array([
        [' ', '*', ' ', '=', '24'],
        ['+', ' ', '/', ' ', ' '],
        [' ', '+', ' ', '=', '5'],
        ['=', ' ', '=', ' ', ' '],
        ['7', ' ', '3', ' ', ' '],
    ])
    binst = solver.Board(board=board, digits=[2, 3, 4, 6])
    solutions = binst.solve_and_print()
    assert len(solutions) == 1, f'unique solutions != 1, == {len(solutions)}'
    solution = solutions[0].assignment
    ground = {Pos(x=0, y=0): 4, Pos(x=2, y=0): 6, Pos(x=0, y=2): 3, Pos(x=2, y=2): 2}
    assert set(solution.keys()) == set(ground.keys()), f'solution keys != ground keys, {set(solution.keys()) ^ set(ground.keys())} \n\n\n{solution} \n\n\n{ground}'
    for pos in solution.keys():
        assert solution[pos] == ground[pos], f'solution[{pos}] != ground[{pos}], {solution[pos]} != {ground[pos]}'


def test_toy2():
    board = np.array([
        [' ', '*', ' ', '=', '-8'],
        ['+', ' ', '/', ' ', ' '],
        [' ', '+', ' ', '=', '4'],
        ['=', ' ', '=', ' ', ' '],
        ['7', ' ', '-2', ' ', ' '],
    ])
    binst = solver.Board(board=board, digits=[-2, 3, 4, 1])
    solutions = binst.solve_and_print()
    assert len(solutions) == 1, f'unique solutions != 1, == {len(solutions)}'
    solution = solutions[0].assignment
    ground = {Pos(x=0, y=0): 4, Pos(x=2, y=0): -2, Pos(x=0, y=2): 3, Pos(x=2, y=2): 1}
    assert set(solution.keys()) == set(ground.keys()), f'solution keys != ground keys, {set(solution.keys()) ^ set(ground.keys())} \n\n\n{solution} \n\n\n{ground}'
    for pos in solution.keys():
        assert solution[pos] == ground[pos], f'solution[{pos}] != ground[{pos}], {solution[pos]} != {ground[pos]}'


def test_toy3():
    board = np.array([
        ['4', '*', '0', '=', '0'],
        ['+', ' ', '/', ' ', ' '],
        ['3', '+', '1', '=', '4'],
        ['=', ' ', '=', ' ', ' '],
        ['7', ' ', '0', ' ', ' '],
    ])
    binst = solver.Board(board=board, digits=[3, 4, 1, 0])
    solutions = binst.solve_and_print()
    assert len(solutions) == 1, f'unique solutions != 1, == {len(solutions)}'
    solution = solutions[0].assignment
    ground = {Pos(x=0, y=0): 4, Pos(x=2, y=0): 0, Pos(x=0, y=2): 3, Pos(x=2, y=2): 1}
    assert set(solution.keys()) == set(ground.keys()), f'solution keys != ground keys, {set(solution.keys()) ^ set(ground.keys())} \n\n\n{solution} \n\n\n{ground}'
    for pos in solution.keys():
        assert solution[pos] == ground[pos], f'solution[{pos}] != ground[{pos}], {solution[pos]} != {ground[pos]}'


def test_ground():
    board = np.array([
        ['8', '*', ' ', '-', ' ', '=', '39'],
        ['-', ' ', '-', ' ', '*', ' ', ' '],
        [' ', '+', '1', '*', ' ', '=', '35'],
        ['*', ' ', '*', ' ', '+', ' ', ' '],
        [' ', '*', ' ', '+', '2', '=', '17'],
        ['=', ' ', '=', ' ', '=', ' ', ' '],
        ['20', ' ', '15', ' ', '65', ' ', ' '],
    ])
    binst = solver.Board(board=board, digits=[1, 2, 3, 4, 5, 6, 7, 8, 9])
    solutions = binst.solve_and_print()
    assert len(solutions) == 1, f'unique solutions != 1, == {len(solutions)}'
    solution = solutions[0].assignment
    ground = {Pos(x=0, y=0): 8, Pos(x=2, y=0): 6, Pos(x=4, y=0): 9, Pos(x=0, y=2): 4, Pos(x=2, y=2): 1, Pos(x=4, y=2): 7, Pos(x=0, y=4): 5, Pos(x=2, y=4): 3, Pos(x=4, y=4): 2}
    assert set(solution.keys()) == set(ground.keys()), f'solution keys != ground keys, {set(solution.keys()) ^ set(ground.keys())} \n\n\n{solution} \n\n\n{ground}'
    for pos in solution.keys():
        assert solution[pos] == ground[pos], f'solution[{pos}] != ground[{pos}], {solution[pos]} != {ground[pos]}'


def test_ground2():
    board = np.array([
        [' ', '+', ' ', '-', ' ', '=', '4'],
        ['+', ' ', '+', ' ', '*', ' ', ' '],
        [' ', '*', ' ', '/', ' ', '=', '3'],
        ['*', ' ', '*', ' ', '+', ' ', ' '],
        [' ', '*', '2', '-', ' ', '=', '2'],
        ['=', ' ', '=', ' ', '=', ' ', ' '],
        ['24', ' ', '32', ' ', '30', ' ', ' '],
    ])
    binst = solver.Board(board=board, digits=[1, 2, 3, 4, 5, 6, 7, 8, 9])
    solutions = binst.solve_and_print()
    assert len(solutions) == 1, f'unique solutions != 1, == {len(solutions)}'
    solution = solutions[0].assignment
    # print(solution)
    ground = {Pos(x=0, y=0): 5, Pos(x=2, y=0): 7, Pos(x=4, y=0): 8, Pos(x=0, y=2): 1, Pos(x=2, y=2): 9, Pos(x=4, y=2): 3, Pos(x=0, y=4): 4, Pos(x=2, y=4): 2, Pos(x=4, y=4): 6}
    assert set(solution.keys()) == set(ground.keys()), f'solution keys != ground keys, {set(solution.keys()) ^ set(ground.keys())} \n\n\n{solution} \n\n\n{ground}'
    for pos in solution.keys():
        assert solution[pos] == ground[pos], f'solution[{pos}] != ground[{pos}], {solution[pos]} != {ground[pos]}'


if __name__ == '__main__':
    test_toy()
    test_toy2()
    test_toy3()
    test_ground()
    test_ground2()
