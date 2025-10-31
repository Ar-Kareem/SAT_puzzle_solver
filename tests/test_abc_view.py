import numpy as np
from puzzle_solver import abc_view_solver as solver
from puzzle_solver.core.utils import get_pos


def test_toy():
    board = np.full((5, 5), ' ')
    top = np.array(['C', 'C', 'C', 'B', ''])
    left = np.array(['C', 'C', '', 'A', ''])
    bottom = np.array(['', 'A', 'A', 'C', 'B'])
    right = np.array(['', '', 'C', '', ''])
    binst = solver.Board(board=board, top=top, left=left, bottom=bottom, right=right, characters=['A', 'B', 'C'])
    solutions = binst.solve_and_print()
    assert len(solutions) == 1, f'unique solutions != 1, == {len(solutions)}'
    # arr = np.array([[solutions[0].assignment.get(get_pos(x=x, y=y), '') for x in range(board.shape[1])] for y in range(board.shape[0])])
    ground = np.array([
        ['', 'C', '', 'B', 'A'],
        ['C', 'B', '', 'A', ''],
        ['B', 'A', 'C', '', ''],
        ['A', '', 'B', '', 'C'],
        ['', '', 'A', 'C', 'B']])
    ground_assignment = {get_pos(x=x, y=y): ground[y][x] for x in range(ground.shape[1]) for y in range(ground.shape[0]) if ground[y][x]}
    assert set(solutions[0].assignment.keys()) == set(ground_assignment.keys()), f'solution keys != ground assignment keys, {set(solutions[0].assignment.keys()) ^ set(ground_assignment.keys())} \n\n\n{solutions[0].assignment} \n\n\n{ground_assignment}'
    for pos in solutions[0].assignment.keys():
        assert solutions[0].assignment[pos] == ground_assignment[pos], f'solution[{pos}] != ground_assignment[{pos}], {solutions[0].assignment[pos]} != {ground_assignment[pos]}'


if __name__ == '__main__':
    test_toy()
