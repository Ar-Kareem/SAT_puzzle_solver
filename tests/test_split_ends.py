import numpy as np
from puzzle_solver import split_ends_solver as solver
from puzzle_solver.core.utils import get_pos


def _solution_to_arr(assignment: dict[tuple[int, int], str]) -> np.array:
    arr = np.full((6, 6), ' ', dtype=object)
    for pos, direction in assignment.items():
        arr[pos.y, pos.x] = direction
    print('[')
    for row in arr:
        row = [f"'{c}'" + ' ' * (3 - len(c)) for c in row]
        print("        [ " + ", ".join(row) + " ],")
    print('    ]')


def test_ground():
    board = np.array([
        ['O', ' ', 'O', 'L', ' ', 'U'],
        [' ', ' ', ' ', ' ', ' ', ' '],
        [' ', 'R', ' ', ' ', 'O', ' '],
        [' ', 'O', ' ', ' ', 'L', ' '],
        [' ', ' ', ' ', ' ', ' ', ' '],
        ['U', ' ', 'L', 'D', ' ', 'R'],
    ])
    binst = solver.Board(board=board)
    solutions = binst.solve_and_print()
    assert len(solutions) == 1, f'unique solutions != 1, == {len(solutions)}'
    solution = solutions[0].assignment
    # _solution_to_arr(solution)
    ground = np.array([
        [ 'O'  , 'D'  , 'O'  , 'L'  , 'R'  , 'U'   ],
        [ 'O'  , 'L'  , 'D'  , 'R'  , 'U'  , 'O'   ],
        [ 'D'  , 'R'  , 'O'  , 'U'  , 'O'  , 'L'   ],
        [ 'R'  , 'O'  , 'U'  , 'O'  , 'L'  , 'D'   ],
        [ 'L'  , 'U'  , 'R'  , 'O'  , 'D'  , 'O'   ],
        [ 'U'  , 'O'  , 'L'  , 'D'  , 'O'  , 'R'   ],
    ])
    ground_assignment = {get_pos(x=x, y=y): ground[y][x] for x in range(ground.shape[1]) for y in range(ground.shape[0])}
    assert set(solution.keys()) == set(ground_assignment.keys()), f'solution keys != ground assignment keys, {set(solution.keys()) ^ set(ground_assignment.keys())} \n\n\n{solution} \n\n\n{ground_assignment}'
    for pos in solution.keys():
        assert solution[pos] == ground_assignment[pos], f'solution[{pos}] != ground_assignment[{pos}], {solution[pos]} != {ground_assignment[pos]}'


if __name__ == '__main__':
    test_ground()
