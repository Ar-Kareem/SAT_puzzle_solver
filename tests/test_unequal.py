import numpy as np

from puzzle_solver import unequal_solver as solver
from puzzle_solver.core.utils import get_pos


def test_toy():
    board = np.array([
        [' ', '<', ' '],
        ['∧', '.', ' '],
        ['2', ' ', ' '],
    ])
    binst = solver.Board(board=board)
    solutions = binst.solve_and_print()
    assert len(solutions) == 1, f'unique solutions != 1, == {len(solutions)}'
    solution = solutions[0].assignment
    ground = np.array([
        [1, 2],
        [2, 1],
    ])
    ground_assignment = {get_pos(x=x, y=y): ground[y][x] for x in range(ground.shape[1]) for y in range(ground.shape[0])}
    assert set(solution.keys()) == set(ground_assignment.keys()), f'solution keys != ground assignment keys, {set(solution.keys()) ^ set(ground_assignment.keys())} \n\n\n{solution} \n\n\n{ground_assignment}'
    for pos in solution.keys():
        assert solution[pos] == ground_assignment[pos], f'solution[{pos}] != ground_assignment[{pos}], {solution[pos]} != {ground_assignment[pos]}'


def test_easy():
    # 4x4 easy
    # https://www.chiark.greenend.org.uk/~sgtatham/puzzles/js/unequal.html#4:0,0,0L,0L,0,0D,0,1,0,0,0,0,0,0,0,4,
    # ∧
    board = np.array([
        [' ', ' ', ' ', '<', ' ', '<', ' '],
        [' ', 'X', ' ', 'X', ' ', 'X', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', '1'],
        [' ', 'X', 'V', 'X', ' ', 'X', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', 'X', ' ', 'X', ' ', 'X', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', '4'],
    ])
    binst = solver.Board(board=board)
    solutions = binst.solve_and_print()
    assert len(solutions) == 1, f'unique solutions != 1, == {len(solutions)}'
    solution = solutions[0].assignment
    ground = np.array([
        [ 4, 1, 2, 3 ],
        [ 2, 4, 3, 1 ],
        [ 1, 3, 4, 2 ],
        [ 3, 2, 1, 4 ],
    ])
    ground_assignment = {get_pos(x=x, y=y): ground[y][x] for x in range(ground.shape[1]) for y in range(ground.shape[0])}
    assert set(solution.keys()) == set(ground_assignment.keys()), f'solution keys != ground assignment keys, {set(solution.keys()) ^ set(ground_assignment.keys())} \n\n\n{solution} \n\n\n{ground_assignment}'
    for pos in solution.keys():
        assert solution[pos] == ground_assignment[pos], f'solution[{pos}] != ground_assignment[{pos}], {solution[pos]} != {ground_assignment[pos]}'


def test_ground():
    # 10x10 max difficulity (recursive difficulity)
    # https://www.chiark.greenend.org.uk/~sgtatham/puzzles/js/unequal.html#10dr%23210113504207134
    board = np.array([
        [' ', ' ', ' ', ' ', '9', ' ', '1', ' ', '7', '>', ' ', '>', ' ', ' ', ' ', ' ', ' ', '>', ' '],
        [' ', 'X', 'V', 'X', ' ', 'X', ' ', 'X', ' ', 'X', ' ', 'X', '∧', 'X', ' ', 'X', ' ', 'X', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', '6', ' ', ' ', ' ', '9', ' ', ' ', ' ', '5', ' ', '3', ' ', ' '],
        [' ', 'X', ' ', 'X', '∧', 'X', ' ', 'X', '∧', 'X', ' ', 'X', ' ', 'X', ' ', 'X', ' ', 'X', ' '],
        [' ', ' ', ' ', '>', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '6', ' ', '9', ' ', ' ', ' ', ' '],
        [' ', 'X', ' ', 'X', 'V', 'X', 'V', 'X', 'V', 'X', ' ', 'X', ' ', 'X', ' ', 'X', ' ', 'X', 'V'],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '<', ' ', '<', ' ', '>', ' ', ' ', ' ', ' ', ' '],
        [' ', 'X', ' ', 'X', '∧', 'X', 'V', 'X', ' ', 'X', ' ', 'X', ' ', 'X', ' ', 'X', ' ', 'X', ' '],
        [' ', ' ', '3', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '<', ' ', ' ', ' '],
        [' ', 'X', ' ', 'X', ' ', 'X', ' ', 'X', '∧', 'X', ' ', 'X', ' ', 'X', ' ', 'X', ' ', 'X', ' '],
        [' ', '<', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '5', ' ', ' ', '>', ' ', '<', ' ', ' ', '4'],
        ['V', 'X', '∧', 'X', 'V', 'X', ' ', 'X', ' ', 'X', ' ', 'X', ' ', 'X', 'V', 'X', ' ', 'X', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '>', ' ', ' ', ' ', ' ', ' '],
        [' ', 'X', ' ', 'X', ' ', 'X', ' ', 'X', ' ', 'X', ' ', 'X', '∧', 'X', ' ', 'X', ' ', 'X', 'V'],
        [' ', ' ', ' ', '<', ' ', ' ', ' ', '<', ' ', ' ', ' ', '<', ' ', '<', ' ', ' ', ' ', '<', ' '],
        [' ', 'X', ' ', 'X', ' ', 'X', 'V', 'X', ' ', 'X', 'V', 'X', '∧', 'X', ' ', 'X', ' ', 'X', ' '],
        [' ', ' ', ' ', ' ', ' ', '>', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '>', ' ', ' ', '9', ' ', ' '],
        ['V', 'X', ' ', 'X', ' ', 'X', ' ', 'X', ' ', 'X', ' ', 'X', ' ', 'X', ' ', 'X', ' ', 'X', 'V'],
        [' ', '>', ' ', ' ', ' ', '>', ' ', ' ', ' ', ' ', '4', '<', ' ', '<', ' ', '<', '7', ' ', '2'],
    ])
    binst = solver.Board(board=board)
    solutions = binst.solve_and_print()
    assert len(solutions) == 1, f'unique solutions != 1, == {len(solutions)}'
    solution = solutions[0].assignment


if __name__ == '__main__':
    test_toy()
    test_easy()
    test_ground()