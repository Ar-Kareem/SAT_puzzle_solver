import numpy as np

from puzzle_solver import flip_solver as solver
from puzzle_solver.core.utils import Pos, get_pos

def test_toy():
    board = np.array([
        ['W', 'B', 'B'],
        ['B', 'B', 'W'],
        ['B', 'B', 'B'],
    ])
    binst = solver.Board(board=board)
    solutions = binst.solve_and_print()
    assert len(solutions) == 1, f'unique solutions != 1, == {len(solutions)}'
    solution = solutions[0].assignment
    ground = np.array([
        ['T', ' ', ' '],
        ['T', ' ', 'T'],
        ['T', 'T', 'T'],
    ])
    ground_assignment = {get_pos(x=x, y=y): 1 if ground[y][x] == 'T' else 0 for x in range(ground.shape[1]) for y in range(ground.shape[0])}
    assert set(solution.keys()) == set(ground_assignment.keys()), f'solution keys != ground assignment keys, {set(solution.keys()) - set(ground_assignment.keys())} \n\n\n{solution} \n\n\n{ground_assignment}'
    for pos in solution.keys():
        assert solution[pos] == ground_assignment[pos], f'solution[{pos}] != ground_assignment[{pos}], {solution[pos]} != {ground_assignment[pos]}'

def test_toy_random():
    # 3 X 3 RANDOM
    # https://www.chiark.greenend.org.uk/~sgtatham/puzzles/js/flip.html
    board = np.array([
        ['B', 'W', 'B'],
        ['W', 'W', 'W'],
        ['W', 'B', 'W'],
    ])
    random_mapping = {
        Pos(x=0, y=0): ['R', 'D'],
        Pos(x=1, y=0): ['L', 'D', 'DR'],
        Pos(x=2, y=0): ['L', 'D'],

        Pos(x=0, y=1): ['U', 'R', 'D'],
        Pos(x=1, y=1): ['U', 'UL', 'UR'],
        Pos(x=2, y=1): ['U', 'D', 'DL'],

        Pos(x=0, y=2): ['U', 'R', 'UR'],
        Pos(x=1, y=2): ['L', 'R', 'UL'],
        Pos(x=2, y=2): ['L', 'U'],
    }
    binst = solver.Board(board=board, random_mapping=random_mapping)
    solutions = binst.solve_and_print()
    assert len(solutions) == 2

def test_ground():
    # 7 x 7 NORMAL
    # https://www.chiark.greenend.org.uk/~sgtatham/puzzles/js/flip.html#7x7c%23786091446619314
    board = np.array([
        ['B', 'W', 'W', 'W', 'W', 'W', 'W'],
        ['B', 'B', 'W', 'W', 'W', 'B', 'B'],
        ['W', 'B', 'W', 'W', 'B', 'B', 'W'],
        ['B', 'B', 'B', 'W', 'W', 'B', 'W'],
        ['W', 'W', 'B', 'B', 'W', 'B', 'W'],
        ['B', 'W', 'B', 'B', 'W', 'W', 'W'],
        ['B', 'W', 'B', 'W', 'W', 'B', 'B'],
    ])
    binst = solver.Board(board=board)
    solutions = binst.solve_and_print()
    assert len(solutions) == 1, f'unique solutions != 1, == {len(solutions)}'
    solution = solutions[0].assignment
    ground = np.array([
        ['T', ' ', 'T', 'T', 'T', ' ', ' '],
        [' ', ' ', ' ', 'T', ' ', 'T', ' '],
        [' ', 'T', ' ', ' ', 'T', ' ', ' '],
        ['T', ' ', 'T', ' ', ' ', 'T', ' '],
        [' ', ' ', ' ', 'T', ' ', ' ', 'T'],
        ['T', ' ', 'T', ' ', 'T', 'T', 'T'],
        [' ', ' ', ' ', ' ', ' ', 'T', 'T'],
    ])
    ground_assignment = {get_pos(x=x, y=y): 1 if ground[y][x] == 'T' else 0 for x in range(ground.shape[1]) for y in range(ground.shape[0])}
    assert set(solution.keys()) == set(ground_assignment.keys()), f'solution keys != ground assignment keys, {set(solution.keys()) ^ set(ground_assignment.keys())} \n\n\n{solution} \n\n\n{ground_assignment}'
    for pos in solution.keys():
        assert solution[pos] == ground_assignment[pos], f'solution[{pos}] != ground_assignment[{pos}], {solution[pos]} != {ground_assignment[pos]}'


if __name__ == '__main__':
    test_toy()
    test_toy_random()
    test_ground()
