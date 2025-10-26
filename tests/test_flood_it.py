import numpy as np

from puzzle_solver import flood_it_solver as solver


def test_toy():
    solution = solver.solve_minimum_steps(board=np.array([
        ['R'],
    ]))
    assert solution is not None, f'No solution found'
    ground = tuple()
    assert tuple(solution) == ground


def test_toy2():
    solutions = solver.solve_minimum_steps(board=np.array([
        ['R', 'G'],
    ]))
    assert len(solutions) == 1, f'unique solutions != 1, == {len(solutions)}'
    ground = ('G',)
    assert tuple(solutions[0]) == ground


def test_toy3():
    board = np.array([
        ['R', 'R', 'G'],
        ['B', 'B', 'B'],
        ['B', 'G', 'B'],
    ])
    solution = solver.solve_minimum_steps(board=board)
    assert solution is not None, 'No solution found'
    ground = ('B', 'G')
    assert tuple(solution) == ground, f"Found solution != expected solution, {tuple(solution)} != {ground}"


def test_toy4():
    board = np.array([
        ['R', 'R', 'G'],
        ['B', 'B', 'B'],
        ['B', 'G', 'B'],
    ])
    solution = solver.solve_minimum_steps(board=board)
    assert solution is not None, 'No solution found'
    ground = ('B', 'G')
    assert tuple(solution) == ground, f"Found solution != expected solution, {tuple(solution)} != {ground}"


def test_ground():
    # 12 x 12 with 10 colors
    # https://www.chiark.Gend.org.uk/~sgtatham/puzzles/js/flood.html#12x12c10m5%23637467359431429
    board = np.array([
        ['G', 'Pink', 'Orange', 'C', 'G', 'Blue', 'C', 'C', 'C', 'Blue', 'C', 'Mint Green'],
        ['Pink', 'Blue', 'C', 'Pink', 'Blue', 'Pink', 'Pink', 'Mint Green', 'Brown', 'Y', 'G', 'G'],
        ['Brown', 'Y', 'Brown', 'C', 'Purple', 'Pink', 'Blue', 'C', 'Pink', 'R', 'Purple', 'C'],
        ['R', 'Pink', 'Pink', 'C', 'Y', 'Pink', 'Purple', 'Mint Green', 'Y', 'Pink', 'G', 'Orange'],
        ['Blue', 'Mint Green', 'Y', 'Purple', 'Purple', 'R', 'Purple', 'C', 'C', 'Mint Green', 'C', 'Mint Green'],
        ['Y', 'Brown', 'C', 'Blue', 'Y', 'Y', 'Mint Green', 'Purple', 'C', 'Orange', 'G', 'R'],
        ['Orange', 'Brown', 'Blue', 'Blue', 'R', 'Blue', 'Pink', 'Mint Green', 'Y', 'Orange', 'Purple', 'Mint Green'],
        ['Mint Green', 'C', 'R', 'Brown', 'Blue', 'Brown', 'Pink', 'Pink', 'G', 'Purple', 'Mint Green', 'Blue'],
        ['Pink', 'C', 'C', 'R', 'Purple', 'G', 'C', 'Y', 'Pink', 'Pink', 'G', 'C'],
        ['Pink', 'Brown', 'G', 'Orange', 'Pink', 'Mint Green', 'R', 'Purple', 'G', 'Orange', 'Y', 'R'],
        ['Mint Green', 'C', 'Pink', 'G', 'Mint Green', 'Orange', 'Blue', 'Y', 'G', 'C', 'Y', 'Purple'],
        ['Orange', 'C', 'Mint Green', 'Blue', 'Purple', 'Pink', 'C', 'R', 'Blue', 'Purple', 'Y', 'Mint Green']
    ])
    solution = solver.solve_minimum_steps(board=board)
    assert solution is not None, 'No solution found'
    assert len(solution) == 25, f'Expected 25 steps, found {len(solution)}'


def test_ground2():
    # 12 x 12 with 6 colors hard (no extra moves allowed)
    # https://www.chiark.Gend.org.uk/~sgtatham/puzzles/js/flood.html#12x12c6m0%23668276603006993
    board = np.array([
        ['B', 'Y', 'G', 'Y', 'R', 'B', 'Y', 'Y', 'G', 'B', 'R', 'P'],
        ['P', 'G', 'G', 'Y', 'B', 'O', 'Y', 'O', 'B', 'Y', 'R', 'O'],
        ['B', 'R', 'P', 'Y', 'O', 'R', 'G', 'G', 'G', 'R', 'R', 'Y'],
        ['O', 'G', 'P', 'G', 'Y', 'Y', 'P', 'P', 'O', 'Y', 'B', 'B'],
        ['G', 'Y', 'G', 'O', 'R', 'G', 'R', 'P', 'G', 'O', 'B', 'R'],
        ['R', 'G', 'B', 'G', 'O', 'B', 'O', 'G', 'B', 'O', 'O', 'B'],
        ['G', 'B', 'P', 'R', 'Y', 'P', 'R', 'B', 'Y', 'B', 'Y', 'P'],
        ['G', 'B', 'G', 'P', 'O', 'Y', 'R', 'Y', 'P', 'P', 'O', 'G'],
        ['R', 'P', 'B', 'O', 'B', 'G', 'Y', 'O', 'Y', 'R', 'P', 'O'],
        ['G', 'P', 'P', 'P', 'P', 'Y', 'G', 'P', 'O', 'G', 'O', 'R'],
        ['Y', 'Y', 'B', 'B', 'R', 'B', 'O', 'R', 'O', 'O', 'R', 'O'],
        ['B', 'G', 'B', 'G', 'R', 'B', 'P', 'Y', 'P', 'B', 'R', 'G']
    ])
    solution = solver.solve_minimum_steps(board=board)
    assert solution is not None, 'No solution found'
    assert len(solution) == 19, f'Expected 19 steps, found {len(solution)}'


def test_ground3():
    # 20 x 20 with 8 colors hard (no extra moves allowed)
    # https://www.chiark.Gend.org.uk/~sgtatham/puzzles/js/flood.html#20x20c8m0%23991967486182787
    board = np.array([
        ['O', 'Y', 'Purple', 'G', 'R', 'Brown', 'G', 'O', 'Brown', 'Y', 'C', 'R', 'G', 'O', 'Purple', 'G', 'Blue', 'R', 'Blue', 'C'],
        ['Purple', 'R', 'Y', 'Purple', 'G', 'Y', 'Purple', 'Brown', 'C', 'R', 'Brown', 'Y', 'R', 'R', 'O', 'G', 'R', 'Y', 'Blue', 'Blue'],
        ['O', 'R', 'Blue', 'G', 'G', 'C', 'Y', 'Blue', 'Purple', 'Blue', 'C', 'Y', 'G', 'G', 'C', 'Blue', 'G', 'Brown', 'Brown', 'G'],
        ['O', 'G', 'G', 'C', 'G', 'Purple', 'C', 'Brown', 'Purple', 'C', 'R', 'Blue', 'R', 'G', 'Brown', 'C', 'Purple', 'Brown', 'Blue', 'C'],
        ['R', 'Brown', 'O', 'C', 'Y', 'Y', 'O', 'Brown', 'Blue', 'Brown', 'C', 'Purple', 'Blue', 'R', 'Blue', 'R', 'Purple', 'Blue', 'Brown', 'Blue'],
        ['O', 'Blue', 'Blue', 'Blue', 'Y', 'Brown', 'Y', 'Blue', 'Y', 'Brown', 'G', 'O', 'O', 'Purple', 'Y', 'C', 'Purple', 'Y', 'O', 'Y'],
        ['O', 'Brown', 'Brown', 'R', 'Y', 'C', 'Purple', 'R', 'G', 'Blue', 'Purple', 'G', 'G', 'Purple', 'Purple', 'R', 'O', 'R', 'C', 'Blue'],
        ['Brown', 'C', 'Purple', 'Blue', 'R', 'C', 'G', 'O', 'C', 'G', 'C', 'G', 'Blue', 'R', 'Brown', 'O', 'Y', 'Brown', 'C', 'G'],
        ['O', 'Purple', 'C', 'R', 'C', 'Brown', 'O', 'G', 'Brown', 'R', 'Brown', 'O', 'Brown', 'Purple', 'R', 'G', 'Y', 'O', 'R', 'O'],
        ['C', 'O', 'Y', 'Blue', 'Brown', 'O', 'Blue', 'Y', 'C', 'R', 'Brown', 'G', 'C', 'Brown', 'Blue', 'Y', 'G', 'Y', 'R', 'O'],
        ['Blue', 'C', 'Purple', 'Y', 'C', 'Blue', 'Purple', 'O', 'Y', 'C', 'Blue', 'G', 'Y', 'O', 'Y', 'Y', 'C', 'Blue', 'R', 'R'],
        ['G', 'C', 'R', 'O', 'Brown', 'G', 'Brown', 'Blue', 'Purple', 'O', 'Purple', 'C', 'Blue', 'R', 'O', 'Blue', 'R', 'Brown', 'G', 'O'],
        ['Blue', 'Y', 'G', 'O', 'C', 'C', 'Blue', 'R', 'Purple', 'C', 'O', 'G', 'Blue', 'R', 'O', 'Blue', 'O', 'Brown', 'R', 'Y'],
        ['Y', 'O', 'O', 'Y', 'Purple', 'G', 'Brown', 'Brown', 'Brown', 'C', 'R', 'Brown', 'R', 'Y', 'O', 'Y', 'R', 'Blue', 'Purple', 'C'],
        ['R', 'Y', 'G', 'C', 'Purple', 'Brown', 'Brown', 'Blue', 'O', 'Purple', 'R', 'C', 'O', 'C', 'C', 'C', 'Purple', 'G', 'Purple', 'Brown'],
        ['Brown', 'Purple', 'Blue', 'O', 'Brown', 'O', 'R', 'Y', 'Y', 'Purple', 'G', 'Brown', 'C', 'Blue', 'G', 'Blue', 'C', 'Blue', 'Purple', 'R'],
        ['Brown', 'Y', 'Brown', 'R', 'Brown', 'Purple', 'G', 'R', 'Brown', 'G', 'R', 'Purple', 'Purple', 'Brown', 'G', 'Brown', 'G', 'O', 'G', 'O'],
        ['Y', 'O', 'Y', 'O', 'Blue', 'Brown', 'C', 'C', 'G', 'Y', 'C', 'Y', 'R', 'Blue', 'Blue', 'Purple', 'O', 'G', 'Blue', 'G'],
        ['O', 'Y', 'O', 'G', 'O', 'R', 'Brown', 'Y', 'Blue', 'C', 'G', 'O', 'R', 'O', 'Brown', 'C', 'Y', 'Purple', 'O', 'O'],
        ['Purple', 'Blue', 'Y', 'Brown', 'C', 'C', 'Y', 'Y', 'Purple', 'O', 'G', 'R', 'G', 'Y', 'C', 'G', 'Purple', 'Y', 'C', 'Blue']
    ])
    solution = solver.solve_minimum_steps(board=board)
    assert solution is not None, 'No solution found'
    assert len(solution) == 36, f'Expected 36 steps, found {len(solution)}'  # WEBSITE SAYS 38


def test_ground4():
    # 20 x 20 with 4 colors
    board = np.array([
        ["R", "Y", "R", "G", "R", "R", "B", "G", "Y", "G", "G", "B", "B", "B", "Y", "R", "B", "Y", "Y", "R"],
        ["Y", "Y", "B", "Y", "G", "B", "Y", "G", "G", "B", "R", "G", "B", "B", "B", "Y", "G", "Y", "G", "R"],
        ["G", "B", "Y", "R", "Y", "R", "B", "R", "Y", "B", "B", "B", "G", "R", "B", "Y", "B", "G", "G", "G"],
        ["G", "Y", "B", "R", "Y", "Y", "Y", "R", "G", "Y", "Y", "G", "B", "B", "G", "R", "G", "R", "G", "Y"],
        ["G", "G", "B", "B", "B", "G", "R", "G", "G", "G", "Y", "R", "Y", "B", "G", "Y", "Y", "B", "Y", "R"],
        ["B", "G", "R", "B", "G", "B", "R", "Y", "B", "G", "B", "B", "Y", "Y", "Y", "G", "G", "B", "Y", "R"],
        ["B", "B", "R", "B", "R", "Y", "B", "Y", "R", "B", "R", "R", "R", "B", "Y", "Y", "G", "G", "B", "B"],
        ["Y", "R", "Y", "B", "Y", "Y", "G", "R", "R", "Y", "G", "Y", "R", "G", "G", "B", "R", "G", "R", "G"],
        ["G", "G", "R", "Y", "G", "Y", "Y", "Y", "B", "R", "Y", "B", "Y", "G", "G", "B", "B", "Y", "R", "R"],
        ["G", "R", "B", "R", "R", "Y", "Y", "R", "Y", "R", "B", "Y", "G", "B", "B", "G", "R", "R", "G", "Y"],
        ["B", "B", "R", "Y", "R", "Y", "B", "B", "R", "R", "B", "Y", "B", "G", "R", "B", "Y", "R", "B", "G"],
        ["B", "B", "Y", "Y", "G", "B", "R", "G", "R", "Y", "R", "Y", "B", "Y", "R", "R", "Y", "Y", "R", "R"],
        ["B", "B", "G", "Y", "Y", "B", "G", "B", "R", "Y", "B", "R", "B", "R", "Y", "G", "B", "R", "B", "B"],
        ["B", "G", "Y", "G", "Y", "R", "Y", "B", "R", "Y", "Y", "B", "Y", "Y", "B", "R", "G", "B", "G", "Y"],
        ["R", "G", "G", "Y", "R", "Y", "R", "Y", "B", "Y", "B", "G", "G", "Y", "G", "B", "G", "G", "Y", "B"],
        ["Y", "G", "B", "G", "B", "B", "G", "G", "B", "B", "B", "B", "G", "B", "Y", "G", "R", "Y", "B", "Y"],
        ["B", "G", "R", "G", "R", "Y", "Y", "R", "G", "R", "Y", "Y", "G", "B", "Y", "Y", "G", "B", "G", "R"],
        ["R", "Y", "B", "G", "R", "R", "R", "Y", "Y", "Y", "B", "Y", "G", "G", "Y", "Y", "R", "R", "B", "R"],
        ["R", "Y", "G", "R", "Y", "Y", "G", "G", "R", "R", "B", "R", "Y", "Y", "Y", "B", "R", "G", "G", "G"],
        ["R", "Y", "Y", "Y", "R", "B", "G", "Y", "Y", "B", "B", "G", "B", "G", "B", "B", "G", "R", "Y", "G"]
    ])
    solution = solver.solve_minimum_steps(board=board, verbose=True)
    assert solution is not None, 'No solution found'


if __name__ == '__main__':
    test_toy()
    test_toy2()
    test_toy3()
    test_toy4()
    test_ground()
    test_ground2()
    test_ground3()
    test_ground4()
