import numpy as np

from puzzle_solver import slitherlink_solver as solver
from puzzle_solver.core.utils import get_pos, set_char


def _ground_to_assignment(ground, shape):
    res = np.full(shape, ' ', dtype=object)
    print(shape)
    for pos in ground.keys():
        set_char(res, pos, ground[pos])
    print('[')
    for row in res:
        row = [f"'{c}'" + ' ' * (3 - len(c)) for c in row]
        print("        [ " + ", ".join(row) + " ],")
    print('    ]')


def test_dummy():
    board = np.array([
        [' ', ' ', ' '],
        [' ', '2', ' '],
        [' ', ' ', ' '],
    ])
    binst = solver.Board(board=board)
    solutions = binst.solve_and_print()
    assert len(solutions) == 80, f'expected 80 solutions, == {len(solutions)}'


def test_easy():
    # 5x5 easy
    # https://www.puzzle-loop.com/
    board = np.array([
        [' ', '2', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' '],
        ['3', '3', '2', '1', ' '],
        ['1', ' ', ' ', ' ', '2'],
        [' ', '3', '3', '2', '0'],
    ])
    binst = solver.Board(board=board)
    solutions = binst.solve_and_print()
    assert len(solutions) == 1, f'unique solutions != 1, == {len(solutions)}'
    solution = solutions[0].assignment
    # _ground_to_assignment(solution, board.shape)
    ground = np.array([
        [ 'DUL', 'DU' , 'DU' , 'DU' , 'RU'  ],
        [ 'D'  , ' '  , 'D'  , 'RD' , 'R'   ],
        [ 'RL' , 'RD' , ' '  , ' '  , 'RD'  ],
        [ 'L'  , 'D'  , ' '  , 'RD' , ' '   ],
        [ 'RDL', 'R'  , 'RD' , ' '  , ' '   ],
    ])
    ground_assignment = {get_pos(x=x, y=y): ground[y][x] for x in range(ground.shape[1]) for y in range(ground.shape[0]) if ground[y][x].strip()}
    assert set(solution.keys()) == set(ground_assignment.keys()), f'solution keys != ground assignment keys, {set(solution.keys()) ^ set(ground_assignment.keys())} \n\n\n{solution} \n\n\n{ground_assignment}'
    for pos in solution.keys():
        assert solution[pos] == ground_assignment[pos], f'solution[{pos}] != ground_assignment[{pos}], {solution[pos]} != {ground_assignment[pos]}'


def test_ground():
    # 20x20 hard
    # https://www.puzzle-loop.com/?e=Nzo0LDM1NCw5MTY=
    board = np.array([
        ['3', ' ', ' ', '2', ' ', ' ', ' ', ' ', ' ', '3', ' ', ' ', ' ', ' ', ' ', '3', ' ', ' ', '1', ' '],
        [' ', ' ', '3', ' ', '3', ' ', ' ', ' ', '3', ' ', '2', '2', ' ', '2', ' ', '2', '2', ' ', '2', '3'],
        ['2', '2', ' ', ' ', ' ', '2', '1', ' ', '1', '1', ' ', ' ', '3', '1', ' ', '2', ' ', ' ', ' ', '2'],
        [' ', ' ', '2', ' ', ' ', '2', '2', ' ', ' ', ' ', '3', ' ', ' ', ' ', ' ', ' ', '2', '2', '3', ' '],
        ['1', '2', '1', ' ', ' ', ' ', '2', '1', ' ', '3', '2', ' ', '3', '2', '2', '3', ' ', '3', '2', '2'],
        [' ', '3', '2', '2', '1', '2', ' ', '3', ' ', ' ', ' ', ' ', '2', '2', '3', ' ', '1', '1', ' ', '2'],
        ['1', ' ', ' ', ' ', ' ', ' ', '2', ' ', ' ', '2', ' ', '1', '3', ' ', ' ', ' ', ' ', '2', '2', '2'],
        [' ', '3', ' ', '2', '0', '1', '2', '1', ' ', '1', '3', ' ', '2', ' ', ' ', '2', ' ', '2', '1', ' '],
        ['2', ' ', ' ', ' ', '2', ' ', '3', ' ', ' ', ' ', ' ', '2', ' ', ' ', '1', '2', ' ', ' ', '1', '3'],
        [' ', ' ', '1', ' ', ' ', ' ', ' ', '2', '0', ' ', '1', ' ', '2', ' ', '0', ' ', '2', ' ', '3', '2'],
        [' ', '3', ' ', '3', ' ', '1', '3', ' ', '3', ' ', '2', ' ', ' ', '2', '2', '2', '3', ' ', ' ', ' '],
        ['3', ' ', ' ', ' ', ' ', ' ', ' ', '0', '2', '1', ' ', ' ', '2', ' ', ' ', '1', ' ', '0', '2', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', '3', ' ', '3', '2', '3', ' ', ' ', '2', ' ', '1', ' ', ' ', ' ', ' '],
        ['2', '2', ' ', '3', '0', ' ', ' ', '3', ' ', ' ', '2', ' ', ' ', ' ', ' ', '2', '2', ' ', '3', ' '],
        [' ', '2', '0', ' ', ' ', '3', ' ', '1', ' ', ' ', '2', ' ', '2', '2', ' ', ' ', ' ', '2', ' ', '2'],
        [' ', ' ', '1', '3', '1', ' ', ' ', ' ', ' ', ' ', '2', ' ', '2', '1', ' ', '1', '2', '2', ' ', ' '],
        ['2', ' ', '2', '2', ' ', '1', '3', ' ', '2', ' ', '3', '1', '2', ' ', '3', '2', ' ', '1', '1', ' '],
        [' ', ' ', '2', ' ', '1', ' ', ' ', ' ', '2', ' ', ' ', ' ', '2', ' ', '1', '0', ' ', ' ', ' ', '3'],
        [' ', '2', ' ', ' ', '2', ' ', '2', '3', '2', ' ', '2', '2', ' ', '3', '2', '2', '3', '3', '1', ' '],
        ['0', '0', ' ', '3', '2', ' ', ' ', ' ', ' ', ' ', '2', '1', '2', '1', ' ', ' ', ' ', '2', '1', ' '],
    ])
    binst = solver.Board(board=board)
    solutions = binst.solve_and_print()
    assert len(solutions) == 1, f'unique solutions != 1, == {len(solutions)}'
    solution = solutions[0].assignment
    # _ground_to_assignment(solution, board.shape)
    ground = np.array([
        [ 'RUL', 'R'  , 'DU' , 'RU' , 'R'  , 'U'  , 'DU' , 'DU' , 'U'  , 'RDU', ' '  , 'RD' , 'U'  , 'RDU', 'R'  , 'RU' , 'R'  , 'DU' , 'U'  , 'RDU' ],
        [ 'RL' , ' '  , 'RD' , 'R'  , 'RD' , 'R'  , ' '  , 'R'  , 'RD' , ' '  , 'RD' , ' '  , 'RD' , ' '  , 'R'  , 'R'  , 'D'  , 'RD' , 'R'  , 'D'   ],
        [ 'RL' , 'R'  , ' '  , 'D'  , 'D'  , 'RD' , ' '  , 'D'  , ' '  , 'R'  , 'D'  , 'R'  , 'D'  , 'D'  , 'R'  , 'D'  , 'D'  , ' '  , 'D'  , 'R'   ],
        [ 'RL' , 'RD' , 'R'  , 'D'  , 'D'  , 'D'  , 'RD' , 'R'  , 'D'  , ' '  , 'RD' , ' '  , 'D'  , 'R'  , ' '  , 'D'  , 'R'  , 'R'  , 'R'  , 'R'   ],
        [ 'L'  , 'D'  , 'D'  , 'D'  , 'D'  , 'D'  , 'D'  , 'D'  , 'R'  , 'RD' , ' '  , 'RD' , 'R'  , 'R'  , 'R'  , 'R'  , 'R'  , 'RD' , 'R'  , 'R'   ],
        [ 'RL' , 'D'  , 'D'  , 'D'  , ' '  , 'D'  , 'D'  , 'RD' , ' '  , 'D'  , 'RD' , ' '  , 'RD' , 'R'  , 'RD' , 'R'  , ' '  , ' '  , 'RD' , 'R'   ],
        [ 'L'  , 'D'  , 'D'  , 'RD' , 'R'  , 'D'  , 'D'  , 'D'  , 'RD' , ' '  , 'D'  , 'R'  , 'D'  , 'D'  , 'D'  , 'R'  , 'D'  , 'RD' , ' '  , 'RD'  ],
        [ 'RL' , 'D'  , ' '  , 'D'  , ' '  , ' '  , 'D'  , ' '  , 'D'  , 'R'  , 'R'  , 'D'  , 'D'  , 'D'  , 'R'  , 'D'  , ' '  , 'D'  , 'R'  , 'D'   ],
        [ 'DL' , 'R'  , 'RD' , 'R'  , 'D'  , 'R'  , 'R'  , 'RD' , 'R'  , 'RD' , ' '  , 'D'  , ' '  , 'RD' , ' '  , 'R'  , 'RD' , 'R'  , ' '  , 'RD'  ],
        [ 'R'  , 'D'  , ' '  , 'D'  , 'RD' , 'R'  , ' '  , 'D'  , ' '  , 'D'  , 'R'  , 'R'  , 'R'  , ' '  , ' '  , 'D'  , 'D'  , 'R'  , 'RD' , ' '   ],
        [ 'D'  , 'RD' , 'R'  , 'D'  , 'D'  , 'R'  , 'RD' , 'R'  , 'RD' , 'R'  , 'R'  , 'R'  , 'R'  , 'D'  , 'RD' , ' '  , 'RD' , ' '  , ' '  , 'D'   ],
        [ 'DL' , ' '  , 'D'  , 'D'  , 'R'  , ' '  , 'D'  , ' '  , 'D'  , 'R'  , 'R'  , 'R'  , 'D'  , ' '  , 'D'  , 'R'  , 'D'  , ' '  , 'RD' , 'R'   ],
        [ 'RD' , 'R'  , ' '  , 'RD' , 'R'  , 'RD' , 'R'  , 'R'  , 'R'  , 'R'  , 'RD' , ' '  , 'RD' , 'R'  , 'R'  , ' '  , 'RD' , 'R'  , 'D'  , 'R'   ],
        [ 'L'  , 'RD' , 'R'  , 'D'  , ' '  , 'D'  , 'R'  , 'RD' , 'R'  , 'D'  , 'D'  , 'RD' , ' '  , 'RD' , 'R'  , 'R'  , ' '  , 'D'  , 'RD' , 'R'   ],
        [ 'RL' , ' '  , ' '  , 'RD' , 'R'  , 'R'  , ' '  , ' '  , 'D'  , 'D'  , 'D'  , 'D'  , 'RD' , ' '  , 'R'  , 'RD' , 'R'  , ' '  , 'D'  , 'RD'  ],
        [ 'RL' , 'D'  , 'R'  , 'D'  , 'R'  , 'R'  , 'D'  , 'R'  , ' '  , ' '  , 'D'  , 'D'  , 'D'  , 'D'  , 'D'  , ' '  , 'RD' , 'R'  , 'D'  , 'D'   ],
        [ 'DL' , 'R'  , 'D'  , 'R'  , 'RD' , ' '  , 'RD' , 'R'  , 'D'  , 'R'  , 'D'  , ' '  , 'D'  , 'D'  , 'RD' , 'R'  , 'D'  , 'D'  , ' '  , 'RD'  ],
        [ 'R'  , 'D'  , 'R'  , 'D'  , ' '  , 'RD' , ' '  , 'D'  , 'R'  , ' '  , 'R'  , 'R'  , ' '  , 'D'  , ' '  , ' '  , 'D'  , 'R'  , 'R'  , 'D'   ],
        [ ' '  , 'R'  , 'D'  , 'R'  , 'R'  , ' '  , 'RD' , 'R'  , 'R'  , 'D'  , 'RD' , 'R'  , 'RD' , 'R'  , 'D'  , 'RD' , 'R'  , 'RD' , ' '  , 'R'   ],
        [ ' '  , ' '  , 'R'  , 'RD' , 'R'  , 'RD' , ' '  , 'R'  , 'D'  , 'D'  , 'D'  , 'D'  , 'D'  , 'D'  , 'D'  , 'D'  , 'D'  , 'D'  , 'D'  , 'RD'  ],
    ])
    ground_assignment = {get_pos(x=x, y=y): ground[y][x] for x in range(ground.shape[1]) for y in range(ground.shape[0]) if ground[y][x].strip()}
    assert set(solution.keys()) == set(ground_assignment.keys()), f'solution keys != ground assignment keys, {set(solution.keys()) ^ set(ground_assignment.keys())} \n\n\n{solution} \n\n\n{ground_assignment}'
    for pos in solution.keys():
        assert solution[pos] == ground_assignment[pos], f'solution[{pos}] != ground_assignment[{pos}], {solution[pos]} != {ground_assignment[pos]}'

if __name__ == '__main__':
    test_dummy()
    test_easy()
    test_ground()
