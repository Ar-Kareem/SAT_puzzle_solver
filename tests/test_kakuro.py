import numpy as np

from puzzle_solver import kakuro_solver as solver
from puzzle_solver.core.utils import get_pos


def _assignment_to_board(assignment, V, H) -> np.array:
    res = np.full((V, H), ' ', dtype=object)
    for pos, var in assignment.items():
        res[pos.y][pos.x] = str(var)
    print('[')
    for row in res:
        row = [c if c != ' ' else "''" for c in row]
        row = [f"{c}" + ' ' * (3 - len(c)) for c in row]
        print("        [ " + ", ".join(row) + " ],")
    print('    ]')


def test_easy():
    # 6 x 6 diamond easy
    # https://www.puzzle-kakuro.com/?e=MDo2LDY2MCwxMzk=
    board = np.array([
        ['#', '#', ' ', ' ', '#', '#'],
        ['#', ' ', ' ', ' ', ' ', '#'],
        [' ', ' ', '#', '#', ' ', ' '],
        [' ', ' ', '#', '#', ' ', ' '],
        ['#', ' ', ' ', ' ', ' ', '#'],
        ['#', '#', ' ', ' ', '#', '#'],
    ])
    row_sums = [[3], [11], [4, 3], [6, 6], [11], [7]]
    col_sums = [[3], [14], [5, 6], [6, 4], [10], [3]]
    binst = solver.Board(board=board, row_sums=row_sums, col_sums=col_sums)
    solutions = binst.solve_and_print()
    assert len(solutions) == 1, f'unique solutions != 1, == {len(solutions)}'
    solution = solutions[0].assignment
    # print(_assignment_to_board(solution, board.shape[0], board.shape[1]))
    ground = np.array([
        [ '' , '' , 2  , 1  , '' , ''  ],
        [ '' , 2  , 3  , 5  , 1  , ''  ],
        [ 1  , 3  , '' , '' , 2  , 1   ],
        [ 2  , 4  , '' , '' , 4  , 2   ],
        [ '' , 5  , 2  , 1  , 3  , ''  ],
        [ '' , '' , 4  , 3  , '' , ''  ],
    ])
    ground_assignment = {get_pos(x=x, y=y): int(ground[y][x]) for x in range(ground.shape[1]) for y in range(ground.shape[0]) if ground[y][x] != ''}
    assert set(solution.keys()) == set(ground_assignment.keys()), f'solution keys != ground assignment keys, {set(solution.keys()) ^ set(ground_assignment.keys())} \n\n\n{solution} \n\n\n{ground_assignment}'
    for pos in solution.keys():
        assert solution[pos] == ground_assignment[pos], f'solution[{pos}] != ground_assignment[{pos}], {solution[pos]} != {ground_assignment[pos]}'


def test_ground():
    # 10 x 10 hard
    # https://www.puzzle-kakuro.com/?e=NTo0LDYyMCw1NTQ=
    board = np.array([
        ['#', '#', ' ', ' ', '#', ' ', ' ', '#', ' ', ' '],
        [' ', ' ', ' ', ' ', '#', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', '#', ' ', ' ', '#', ' ', ' ', '#'],
        ['#', '#', ' ', ' ', ' ', '#', '#', ' ', ' ', '#'],
        [' ', ' ', '#', ' ', ' ', ' ', ' ', '#', ' ', ' '],
        [' ', ' ', '#', ' ', ' ', ' ', ' ', '#', ' ', ' '],
        ['#', ' ', ' ', '#', '#', ' ', ' ', ' ', '#', '#'],
        ['#', ' ', ' ', '#', ' ', ' ', '#', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', '#', ' ', ' ', ' ', ' '],
        [' ', ' ', '#', ' ', ' ', '#', ' ', ' ', '#', '#'],
    ])
    row_sums = [[7, 16, 12, ], [28, 23, ], [22, 16, 9, ], [18, 15, ], [12, 11, 16, ], [9, 24, 8, ], [7, 9, ], [14, 7, 20, ], [23, 30, ], [11, 3, 4, ]]
    col_sums = [[14, 12, 8, ], [15, 21, ], [29, 23, ], [8, 10, 11, ], [24, 8, ], [21, 13, ], [17, 12, 11, ], [21, 15, ], [29, 17, ], [4, 16, 15]]
    binst = solver.Board(board=board, row_sums=row_sums, col_sums=col_sums)
    solutions = binst.solve_and_print()
    assert len(solutions) == 1, f'unique solutions != 1, == {len(solutions)}'
    solution = solutions[0].assignment
    # print(_assignment_to_board(solution, board.shape[0], board.shape[1]))
    ground = np.array([
        [ '' , '' , 5  , 2  , '' , 7  , 9  , '' , 9  , 3   ],
        [ 5  , 9  , 8  , 6  , '' , 5  , 8  , 7  , 2  , 1   ],
        [ 9  , 6  , 7  , '' , 7  , 9  , '' , 5  , 4  , ''  ],
        [ '' , '' , 9  , 3  , 6  , '' , '' , 9  , 6  , ''  ],
        [ 9  , 3  , '' , 2  , 3  , 1  , 5  , '' , 7  , 9   ],
        [ 3  , 6  , '' , 5  , 8  , 7  , 4  , '' , 1  , 7   ],
        [ '' , 1  , 6  , '' , '' , 2  , 3  , 4  , '' , ''  ],
        [ '' , 5  , 9  , '' , 4  , 3  , '' , 3  , 8  , 9   ],
        [ 1  , 2  , 8  , 9  , 3  , '' , 8  , 7  , 9  , 6   ],
        [ 7  , 4  , '' , 2  , 1  , '' , 3  , 1  , '' , ''  ],
    ])
    ground_assignment = {get_pos(x=x, y=y): int(ground[y][x]) for x in range(ground.shape[1]) for y in range(ground.shape[0]) if ground[y][x] != ''}
    assert set(solution.keys()) == set(ground_assignment.keys()), f'solution keys != ground assignment keys, {set(solution.keys()) ^ set(ground_assignment.keys())} \n\n\n{solution} \n\n\n{ground_assignment}'
    for pos in solution.keys():
        assert solution[pos] == ground_assignment[pos], f'solution[{pos}] != ground_assignment[{pos}], {solution[pos]} != {ground_assignment[pos]}'


if __name__ == '__main__':
    test_easy()
    test_ground()

