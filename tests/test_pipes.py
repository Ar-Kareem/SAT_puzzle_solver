import numpy as np

from puzzle_solver import pipes_solver as solver
from puzzle_solver.core.utils import get_pos

def test_easy():
    # 4 x 4 easy
    # https://www.puzzle-pipes.com/?e=MDo3LDI2NiwyMTg=
    board=np.array([
        [ '1',  '2L', '2L', '1'  ],
        [ '2L', '3',  '2I', '2I' ],
        [ '1',  '1',  '3',  '3'  ],
        [ '2L', '2I', '2L', '1'  ]
    ])
    binst = solver.Board(board=board)
    solutions = binst.solve_and_print()
    assert len(solutions) == 1, f'unique solutions != 1, == {len(solutions)}'
    solution = solutions[0].assignment
    ground = np.array([
        ['D  ', 'DR ', 'DL ', 'D  ',],
        ['UR ', 'UDL', 'UD ', 'UD ',],
        ['D  ', 'U  ', 'UDR', 'UDL',],
        ['UR ', 'LR ', 'UL ', 'U  ',],])
    ground_assignment = {get_pos(x=x, y=y): ground[y][x].strip() for x in range(ground.shape[1]) for y in range(ground.shape[0])}
    assert set(solution.keys()) == set(ground_assignment.keys()), f'solution keys != ground assignment keys, {set(solution.keys()) ^ set(ground_assignment.keys())} \n\n\n{solution} \n\n\n{ground_assignment}'
    for pos in solution.keys():
        assert solution[pos] == ground_assignment[pos], f'solution[{pos}] != ground_assignment[{pos}], {solution[pos]} != {ground_assignment[pos]}'


def test_ground():
    # 7 x 7
    # https://www.puzzle-pipes.com/?e=MjoyNTgsNjQz
    board=np.array([
        [ '1 ', '3 ', '2I', '1 ', '2L', '1 ', '1 ' ],
        [ '1 ', '3 ', '3 ', '1 ', '2I', '2L', '2L' ],
        [ '2L', '3 ', '2L', '3 ', '3 ', '3 ', '1 ' ],
        [ '2L', '2L', '1 ', '3 ', '1 ', '2I', '1 ' ],
        [ '2I', '1 ', '3 ', '3 ', '3 ', '3 ', '2I' ],
        [ '1 ', '1 ', '3 ', '2L', '3 ', '2L', '2L' ],
        [ '1 ', '2I', '2L', '1 ', '2L', '2I', '1 ' ],
    ])
    binst = solver.Board(board=board)
    solutions = binst.solve_and_print()
    assert len(solutions) == 1, f'unique solutions != 1, == {len(solutions)}'
    solution = solutions[0].assignment


def test_ground2():
    # 10 x 10
    # https://www.puzzle-pipes.com/?e=MzoxLDE5OCw0ODU=
    board=np.array([
        [ '1 ', '3 ', '3 ', '3 ', '1 ', '1 ', '2L', '2L', '2I', '1 ' ],
        [ '1 ', '1 ', '1 ', '3 ', '2I', '1 ', '2I', '3 ', '2I', '1 ' ],
        [ '2I', '1 ', '1 ', '3 ', '2L', '1 ', '3 ', '2I', '1 ', '1 ' ],
        [ '2I', '2I', '1 ', '3 ', '3 ', '3 ', '2L', '3 ', '3 ', '2L' ],
        [ '3 ', '3 ', '2I', '3 ', '1 ', '3 ', '2I', '2L', '1 ', '2L' ],
        [ '1 ', '1 ', '3 ', '2I', '3 ', '2L', '1 ', '1 ', '2L', '2L' ],
        [ '1 ', '1 ', '3 ', '1 ', '1 ', '1 ', '3 ', '3 ', '3 ', '2L' ],
        [ '3 ', '2I', '3 ', '3 ', '2L', '3 ', '3 ', '2I', '2L', '1 ' ],
        [ '1 ', '1 ', '3 ', '3 ', '3 ', '3 ', '1 ', '2L', '3 ', '2L' ],
        [ '1 ', '2I', '3 ', '2I', '1 ', '1 ', '1 ', '3 ', '1 ', '1 ' ],
    ])
    binst = solver.Board(board=board)
    solutions = binst.solve_and_print()
    assert len(solutions) == 1, f'unique solutions != 1, == {len(solutions)}'
    solution = solutions[0].assignment


if __name__ == '__main__':
    test_easy()
    test_ground()
    test_ground2()
