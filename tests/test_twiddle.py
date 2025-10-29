import numpy as np
import pytest

from puzzle_solver import twiddle_solver as solver


@pytest.mark.very_slow
def test_toy():
    board = np.array([
        [6, 8, 2],
        [7, 9, 3],
        [5, 1, 4],
    ])
    binst = solver.Board(board=board, time_horizon=20)
    solutions = binst.solve_and_print()
    assert len(solutions) == 1, f'unique solutions != 1, == {len(solutions)}'
    # solution = solutions[0].assignment


def test_toy2():
    board = np.array([
        [2, 5, 3],
        [4, 8, 6],
        [1, 7, 9],
    ])
    binst = solver.Board(board=board, time_horizon=20)
    solutions = binst.solve_and_print()
    assert len(solutions) == 1, f'unique solutions != 1, == {len(solutions)}'


def test_toy3():
    board = np.array([
        [2, 5, 3],
        [4, 8, 6],
        [1, 7, 9],
    ])
    binst = solver.Board(board=board, time_horizon=20)
    solutions = binst.solve_and_print()
    assert len(solutions) == 1, f'unique solutions != 1, == {len(solutions)}'


if __name__ == '__main__':
    test_toy()
    # test_toy2()
    test_toy3()
