import numpy as np

from puzzle_solver import connect_the_dots_solver as solver
from puzzle_solver.core.utils import get_pos


def _debug_assignment_to_array(assignment, V, H):
    res = np.full((V, H), ' ', dtype=object)
    for y in range(V):
        for x in range(H):
            res[y][x] = assignment[get_pos(x=x, y=y)]
    print('[')
    for row in res:
        row = [c if c != ' ' else "''" for c in row]
        row = [f"'{c}'" + ' ' * (3 - len(c)) for c in row]
        print("        [ " + ", ".join(row) + " ],")
    print('    ]')


def test_easy():
    board = np.array([
        ['B', 'Y', 'R', ' ', ' '],
        [' ', ' ', ' ', ' ', ' '],
        [' ', 'B', 'G', ' ', ' '],
        [' ', ' ', ' ', ' ', ' '],
        ['G', 'Y', ' ', ' ', 'R'],
    ])
    binst = solver.Board(board=board)
    solutions = binst.solve_and_print()
    assert len(solutions) == 1, f'unique solutions != 1, == {len(solutions)}'
    solution = solutions[0].assignment
    # _debug_assignment_to_array(solution, board.shape[0], board.shape[1])
    ground = np.array([
        [ 'B'  , 'Y'  , 'R'  , 'R'  , 'R'   ],
        [ 'B'  , 'Y'  , 'Y'  , 'Y'  , 'R'   ],
        [ 'B'  , 'B'  , 'G'  , 'Y'  , 'R'   ],
        [ 'G'  , 'G'  , 'G'  , 'Y'  , 'R'   ],
        [ 'G'  , 'Y'  , 'Y'  , 'Y'  , 'R'   ],
    ])
    ground_assignment = {get_pos(x=x, y=y): ground[y][x] for x in range(ground.shape[1]) for y in range(ground.shape[0])}
    assert set(solution.keys()) == set(ground_assignment.keys()), f'solution keys != ground assignment keys, {set(solution.keys()) ^ set(ground_assignment.keys())} \n\n\n{solution} \n\n\n{ground_assignment}'
    for pos in solution.keys():
        assert solution[pos] == ground_assignment[pos], f'solution[{pos}] != ground_assignment[{pos}], {solution[pos]} != {ground_assignment[pos]}'


def test_medium():
    board = np.array([
        ['C', ' ', ' ', ' ', ' ', ' ', 'R'],
        ['M', ' ', 'M', 'C', 'R', ' ', 'B'],
        [' ', ' ', ' ', ' ', ' ', ' ', 'Y'],
        [' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', 'Y', ' ', ' ', ' ', ' ', ' '],
        [' ', 'G', ' ', ' ', ' ', 'B', ' '],
        [' ', ' ', ' ', ' ', 'G', ' ', ' '],
    ])
    binst = solver.Board(board=board)
    solutions = binst.solve_and_print()
    assert len(solutions) == 1, f'unique solutions != 1, == {len(solutions)}'
    solution = solutions[0].assignment
    # _debug_assignment_to_array(solution, board.shape[0], board.shape[1])
    ground = np.array([
        [ 'C'  , 'C'  , 'C'  , 'C'  , 'R'  , 'R'  , 'R'   ],
        [ 'M'  , 'M'  , 'M'  , 'C'  , 'R'  , 'B'  , 'B'   ],
        [ 'B'  , 'B'  , 'B'  , 'B'  , 'B'  , 'B'  , 'Y'   ],
        [ 'B'  , 'Y'  , 'Y'  , 'Y'  , 'Y'  , 'Y'  , 'Y'   ],
        [ 'B'  , 'Y'  , 'G'  , 'G'  , 'G'  , 'G'  , 'G'   ],
        [ 'B'  , 'G'  , 'G'  , 'B'  , 'B'  , 'B'  , 'G'   ],
        [ 'B'  , 'B'  , 'B'  , 'B'  , 'G'  , 'G'  , 'G'   ],
    ])
    ground_assignment = {get_pos(x=x, y=y): ground[y][x] for x in range(ground.shape[1]) for y in range(ground.shape[0])}
    assert set(solution.keys()) == set(ground_assignment.keys()), f'solution keys != ground assignment keys, {set(solution.keys()) ^ set(ground_assignment.keys())} \n\n\n{solution} \n\n\n{ground_assignment}'
    for pos in solution.keys():
        assert solution[pos] == ground_assignment[pos], f'solution[{pos}] != ground_assignment[{pos}], {solution[pos]} != {ground_assignment[pos]}'


def test_medium2():
    board = np.array([
        ['Y', ' ', ' ', ' ', 'B', 'R'],
        [' ', ' ', 'G', ' ', ' ', ' '],
        [' ', 'Y', ' ', ' ', ' ', ' '],
        [' ', 'M', ' ', 'M', ' ', ' '],
        [' ', 'B', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', 'G', 'R'],
    ])
    binst = solver.Board(board=board)
    solutions = binst.solve_and_print()
    assert len(solutions) == 1, f'unique solutions != 1, == {len(solutions)}'
    solution = solutions[0].assignment
    # _debug_assignment_to_array(solution, board.shape[0], board.shape[1])
    ground = np.array([
        [ 'Y'  , 'Y'  , 'Y'  , 'Y'  , 'B'  , 'R'   ],
        [ 'G'  , 'G'  , 'G'  , 'Y'  , 'B'  , 'R'   ],
        [ 'G'  , 'Y'  , 'Y'  , 'Y'  , 'B'  , 'R'   ],
        [ 'G'  , 'M'  , 'M'  , 'M'  , 'B'  , 'R'   ],
        [ 'G'  , 'B'  , 'B'  , 'B'  , 'B'  , 'R'   ],
        [ 'G'  , 'G'  , 'G'  , 'G'  , 'G'  , 'R'   ],
    ])
    ground_assignment = {get_pos(x=x, y=y): ground[y][x] for x in range(ground.shape[1]) for y in range(ground.shape[0])}
    assert set(solution.keys()) == set(ground_assignment.keys()), f'solution keys != ground assignment keys, {set(solution.keys()) ^ set(ground_assignment.keys())} \n\n\n{solution} \n\n\n{ground_assignment}'
    for pos in solution.keys():
        assert solution[pos] == ground_assignment[pos], f'solution[{pos}] != ground_assignment[{pos}], {solution[pos]} != {ground_assignment[pos]}'


def test_ground():
    board = np.array([
        ['R', ' ', 'B', ' ', ' ', ' ', ' ', ' '],
        ['Y', ' ', ' ', 'R', 'G', ' ', 'G', ' '],
        [' ', 'M', ' ', ' ', ' ', 'P', ' ', ' '],
        [' ', 'O', ' ', ' ', ' ', 'M', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        ['Br', 'B', ' ', ' ', 'Y', 'O', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', 'P', ' ', ' '],
        [' ', ' ', ' ', 'Br', ' ', ' ', ' ', ' '],
    ])
    binst = solver.Board(board=board)
    solutions = binst.solve_and_print()
    assert len(solutions) == 1, f'unique solutions != 1, == {len(solutions)}'
    solution = solutions[0].assignment
    # _debug_assignment_to_array(solution, board.shape[0], board.shape[1])
    ground = np.array([
        [ 'R'  , 'R'  , 'B'  , 'B'  , 'B'  , 'B'  , 'B'  , 'B'   ],
        [ 'Y'  , 'R'  , 'R'  , 'R'  , 'G'  , 'G'  , 'G'  , 'B'   ],
        [ 'Y'  , 'M'  , 'M'  , 'M'  , 'M'  , 'P'  , 'P'  , 'B'   ],
        [ 'Y'  , 'O'  , 'O'  , 'O'  , 'M'  , 'M'  , 'P'  , 'B'   ],
        [ 'Y'  , 'Y'  , 'Y'  , 'O'  , 'O'  , 'O'  , 'P'  , 'B'   ],
        [ 'Br' , 'B'  , 'Y'  , 'Y'  , 'Y'  , 'O'  , 'P'  , 'B'   ],
        [ 'Br' , 'B'  , 'B'  , 'B'  , 'B'  , 'P'  , 'P'  , 'B'   ],
        [ 'Br' , 'Br' , 'Br' , 'Br' , 'B'  , 'B'  , 'B'  , 'B'   ],
    ])
    ground_assignment = {get_pos(x=x, y=y): ground[y][x] for x in range(ground.shape[1]) for y in range(ground.shape[0])}
    assert set(solution.keys()) == set(ground_assignment.keys()), f'solution keys != ground assignment keys, {set(solution.keys()) ^ set(ground_assignment.keys())} \n\n\n{solution} \n\n\n{ground_assignment}'
    for pos in solution.keys():
        assert solution[pos] == ground_assignment[pos], f'solution[{pos}] != ground_assignment[{pos}], {solution[pos]} != {ground_assignment[pos]}'


if __name__ == "__main__":
    test_easy()
    # test_medium()
    test_medium2()
    test_ground()
