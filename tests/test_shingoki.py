import numpy as np

from puzzle_solver import shingoki_solver as solver
from puzzle_solver.core.utils import Pos


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
    print(solution)
    ground_assignment = {(Pos(x=0, y=0), Pos(x=1, y=0)): 0, (Pos(x=0, y=0), Pos(x=0, y=1)): 0, (Pos(x=1, y=0), Pos(x=2, y=0)): 1, (Pos(x=1, y=0), Pos(x=0, y=0)): 0, (Pos(x=1, y=0), Pos(x=1, y=1)): 1, (Pos(x=2, y=0), Pos(x=3, y=0)): 1, (Pos(x=2, y=0), Pos(x=1, y=0)): 1, (Pos(x=2, y=0), Pos(x=2, y=1)): 0, (Pos(x=3, y=0), Pos(x=4, y=0)): 1, (Pos(x=3, y=0), Pos(x=2, y=0)): 1, (Pos(x=3, y=0), Pos(x=3, y=1)): 0, (Pos(x=4, y=0), Pos(x=5, y=0)): 0, (Pos(x=4, y=0), Pos(x=3, y=0)): 1, (Pos(x=4, y=0), Pos(x=4, y=1)): 1, (Pos(x=5, y=0), Pos(x=4, y=0)): 0, (Pos(x=5, y=0), Pos(x=5, y=1)): 0, (Pos(x=0, y=1), Pos(x=1, y=1)): 0, (Pos(x=0, y=1), Pos(x=0, y=2)): 0, (Pos(x=0, y=1), Pos(x=0, y=0)): 0, (Pos(x=1, y=1), Pos(x=2, y=1)): 0, (Pos(x=1, y=1), Pos(x=0, y=1)): 0, (Pos(x=1, y=1), Pos(x=1, y=2)): 1, (Pos(x=1, y=1), Pos(x=1, y=0)): 1, (Pos(x=2, y=1), Pos(x=3, y=1)): 1, (Pos(x=2, y=1), Pos(x=1, y=1)): 0, (Pos(x=2, y=1), Pos(x=2, y=2)): 1, (Pos(x=2, y=1), Pos(x=2, y=0)): 0, (Pos(x=3, y=1), Pos(x=4, y=1)): 0, (Pos(x=3, y=1), Pos(x=2, y=1)): 1, (Pos(x=3, y=1), Pos(x=3, y=2)): 1, (Pos(x=3, y=1), Pos(x=3, y=0)): 0, (Pos(x=4, y=1), Pos(x=5, y=1)): 0, (Pos(x=4, y=1), Pos(x=3, y=1)): 0, (Pos(x=4, y=1), Pos(x=4, y=2)): 1, (Pos(x=4, y=1), Pos(x=4, y=0)): 1, (Pos(x=5, y=1), Pos(x=4, y=1)): 0, (Pos(x=5, y=1), Pos(x=5, y=2)): 0, (Pos(x=5, y=1), Pos(x=5, y=0)): 0, (Pos(x=0, y=2), Pos(x=1, y=2)): 0, (Pos(x=0, y=2), Pos(x=0, y=3)): 0, (Pos(x=0, y=2), Pos(x=0, y=1)): 0, (Pos(x=1, y=2), Pos(x=2, y=2)): 0, (Pos(x=1, y=2), Pos(x=0, y=2)): 0, (Pos(x=1, y=2), Pos(x=1, y=3)): 1, (Pos(x=1, y=2), Pos(x=1, y=1)): 1, (Pos(x=2, y=2), Pos(x=3, y=2)): 0, (Pos(x=2, y=2), Pos(x=1, y=2)): 0, (Pos(x=2, y=2), Pos(x=2, y=3)): 1, (Pos(x=2, y=2), Pos(x=2, y=1)): 1, (Pos(x=3, y=2), Pos(x=4, y=2)): 0, (Pos(x=3, y=2), Pos(x=2, y=2)): 0, (Pos(x=3, y=2), Pos(x=3, y=3)): 1, (Pos(x=3, y=2), Pos(x=3, y=1)): 1, (Pos(x=4, y=2), Pos(x=5, y=2)): 1, (Pos(x=4, y=2), Pos(x=3, y=2)): 0, (Pos(x=4, y=2), Pos(x=4, y=3)): 0, (Pos(x=4, y=2), Pos(x=4, y=1)): 1, (Pos(x=5, y=2), Pos(x=4, y=2)): 1, (Pos(x=5, y=2), Pos(x=5, y=3)): 1, (Pos(x=5, y=2), Pos(x=5, y=1)): 0, (Pos(x=0, y=3), Pos(x=1, y=3)): 1, (Pos(x=0, y=3), Pos(x=0, y=4)): 1, (Pos(x=0, y=3), Pos(x=0, y=2)): 0, (Pos(x=1, y=3), Pos(x=2, y=3)): 0, (Pos(x=1, y=3), Pos(x=0, y=3)): 1, (Pos(x=1, y=3), Pos(x=1, y=4)): 0, (Pos(x=1, y=3), Pos(x=1, y=2)): 1, (Pos(x=2, y=3), Pos(x=3, y=3)): 0, (Pos(x=2, y=3), Pos(x=1, y=3)): 0, (Pos(x=2, y=3), Pos(x=2, y=4)): 1, (Pos(x=2, y=3), Pos(x=2, y=2)): 1, (Pos(x=3, y=3), Pos(x=4, y=3)): 0, (Pos(x=3, y=3), Pos(x=2, y=3)): 0, (Pos(x=3, y=3), Pos(x=3, y=4)): 1, (Pos(x=3, y=3), Pos(x=3, y=2)): 1, (Pos(x=4, y=3), Pos(x=5, y=3)): 1, (Pos(x=4, y=3), Pos(x=3, y=3)): 0, (Pos(x=4, y=3), Pos(x=4, y=4)): 1, (Pos(x=4, y=3), Pos(x=4, y=2)): 0, (Pos(x=5, y=3), Pos(x=4, y=3)): 1, (Pos(x=5, y=3), Pos(x=5, y=4)): 0, (Pos(x=5, y=3), Pos(x=5, y=2)): 1, (Pos(x=0, y=4), Pos(x=1, y=4)): 1, (Pos(x=0, y=4), Pos(x=0, y=5)): 0, (Pos(x=0, y=4), Pos(x=0, y=3)): 1, (Pos(x=1, y=4), Pos(x=2, y=4)): 1, (Pos(x=1, y=4), Pos(x=0, y=4)): 1, (Pos(x=1, y=4), Pos(x=1, y=5)): 0, (Pos(x=1, y=4), Pos(x=1, y=3)): 0, (Pos(x=2, y=4), Pos(x=3, y=4)): 0, (Pos(x=2, y=4), Pos(x=1, y=4)): 1, (Pos(x=2, y=4), Pos(x=2, y=5)): 0, (Pos(x=2, y=4), Pos(x=2, y=3)): 1, (Pos(x=3, y=4), Pos(x=4, y=4)): 0, (Pos(x=3, y=4), Pos(x=2, y=4)): 0, (Pos(x=3, y=4), Pos(x=3, y=5)): 1, (Pos(x=3, y=4), Pos(x=3, y=3)): 1, (Pos(x=4, y=4), Pos(x=5, y=4)): 1, (Pos(x=4, y=4), Pos(x=3, y=4)): 0, (Pos(x=4, y=4), Pos(x=4, y=5)): 0, (Pos(x=4, y=4), Pos(x=4, y=3)): 1, (Pos(x=5, y=4), Pos(x=4, y=4)): 1, (Pos(x=5, y=4), Pos(x=5, y=5)): 1, (Pos(x=5, y=4), Pos(x=5, y=3)): 0, (Pos(x=0, y=5), Pos(x=1, y=5)): 0, (Pos(x=0, y=5), Pos(x=0, y=4)): 0, (Pos(x=1, y=5), Pos(x=2, y=5)): 0, (Pos(x=1, y=5), Pos(x=0, y=5)): 0, (Pos(x=1, y=5), Pos(x=1, y=4)): 0, (Pos(x=2, y=5), Pos(x=3, y=5)): 0, (Pos(x=2, y=5), Pos(x=1, y=5)): 0, (Pos(x=2, y=5), Pos(x=2, y=4)): 0, (Pos(x=3, y=5), Pos(x=4, y=5)): 1, (Pos(x=3, y=5), Pos(x=2, y=5)): 0, (Pos(x=3, y=5), Pos(x=3, y=4)): 1, (Pos(x=4, y=5), Pos(x=5, y=5)): 1, (Pos(x=4, y=5), Pos(x=3, y=5)): 1, (Pos(x=4, y=5), Pos(x=4, y=4)): 0, (Pos(x=5, y=5), Pos(x=4, y=5)): 1, (Pos(x=5, y=5), Pos(x=5, y=4)): 1}
    assert set(solution.keys()) == set(ground_assignment.keys()), f'solution keys != ground assignment keys, {set(solution.keys()) ^ set(ground_assignment.keys())} \n\n\n{solution} \n\n\n{ground_assignment}'
    for pos in solution.keys():
        assert solution[pos] == ground_assignment[pos], f'solution[{pos}] != ground_assignment[{pos}], {solution[pos]} != {ground_assignment[pos]}'


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
    print(solution)




if __name__ == '__main__':
    test_small()
    test_ground()
