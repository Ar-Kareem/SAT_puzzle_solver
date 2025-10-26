import numpy as np

from puzzle_solver import shakashaka_solver as solver
from puzzle_solver.core.utils import get_all_pos, get_pos
from puzzle_solver.core.utils_visualizer import render_bw_tiles_split


def _debug_plot_all_rectangles():
    H, V = 7, 6
    rectangles = solver.init_rectangles(V, H)
    State = solver.State
    for r in rectangles:
        black_board = np.full((V, H), 'B', dtype=object)
        for p, state in r.body:
            black_board[p[1]][p[0]] = {State.WHITE: 'W', State.BLACK: 'B', State.TOP_LEFT: 'TL', State.TOP_RIGHT: 'TR', State.BOTTOM_LEFT: 'BL', State.BOTTOM_RIGHT: 'BR'}[state]
        for p in r.disallow_white:
            if 0 <= p[1] < V and 0 <= p[0] < H:
                black_board[p[1]][p[0]] = 'B'
        print(f"Rotated {r.is_rotated} {r.width}x{r.height}")
        print(r.body)
        print(render_bw_tiles_split(black_board, cell_w=4, cell_h=2, borders=True, mode="ansi"))
    print("Found total of", len(rectangles), "rectangles")
    # for r in rectangles:
    #     print(r)


def _debug_assignment(assignment, V, H):
    res = np.full((V, H), '  ', dtype=object)
    for pos in get_all_pos(V, H):
        if pos in assignment:
            res[pos.y][pos.x] = assignment[pos]
    print('[')
    for row in res:
        row = [f"'{c}'" + ' ' * (2 - len(c)) for c in row]
        print("        [ " + ", ".join(row) + " ],")
    print('    ]')


def _debug_render_bw_tiles_split():
    board = np.array([
        ['0', '', '', '', '', '1', '', '', '2', ''],
        ['', '', '', '', '', '', '', '', '', ''],
        ['', '', '', '', '', '', '', '2', '', ''],
        ['', '', '', '', '', '', '', '', '', ''],
        ['', '', '4', '', '', '', '', '', '', ''],
        ['B', '', '', '3', '', '', '', '', '', ''],
        ['', '', '', '', '', '', '', 'B', '', ''],
        ['2', '', '', '', '', '', '', '', '', '2'],
        ['', '', '', '', '', '', '', '', '', ''],
        ['', '', '', 'B', '0', '', '', '', 'B', ''],
    ])
    ground = np.array([
        [ 'B' , 'W' , 'TL', 'TR', 'W' , 'B' , 'TL', 'TR', 'B' , 'W'  ],
        [ 'W' , 'TL', 'W' , 'W' , 'TR', 'W' , 'BL', 'BR', 'TL', 'TR' ],
        [ 'W' , 'BL', 'W' , 'W' , 'W' , 'TR', 'W' , 'B' , 'BL', 'BR' ],
        [ 'TL', 'TR', 'BL', 'W' , 'W' , 'W' , 'TR', 'W' , 'TL', 'TR' ],
        [ 'BL', 'BR', 'B' , 'BL', 'W' , 'W' , 'W' , 'TR', 'BL', 'BR' ],
        [ 'B' , 'TL', 'TR', 'B' , 'BL', 'W' , 'W' , 'BR', 'TL', 'TR' ],
        [ 'W' , 'BL', 'BR', 'W' , 'W' , 'BL', 'BR', 'B' , 'BL', 'BR' ],
        [ 'B' , 'TL', 'TR', 'W' , 'W' , 'TL', 'TR', 'TL', 'TR', 'B'  ],
        [ 'TL', 'W' , 'BR', 'W' , 'W' , 'BL', 'BR', 'BL', 'BR', 'W'  ],
        [ 'BL', 'BR', 'W' , 'B' , 'B' , 'W' , 'W' , 'W' , 'B' , 'W'  ],
    ])
    print(render_bw_tiles_split(ground, cell_w=6, cell_h=3, borders=True, mode="text", cell_text=lambda r, c: board[r][c]))


def test_toy():
    board = np.array([
        ['B', ' ', ' ', 'B', ' '],
        ['B', ' ', ' ', ' ', ' '],
        [' ', ' ', '2', ' ', ' '],
        [' ', ' ', ' ', ' ', ' '],
        ['B', ' ', 'B', ' ', ' '],
    ])
    binst = solver.Board(board=board)
    solutions = binst.solve_and_print()
    assert len(solutions) == 1, f'unique solutions != 1, == {len(solutions)}'
    solution = solutions[0].assignment
    # _debug_assignment(solution, board.shape[0], board.shape[1])
    ground = np.array([
        [ '  ', 'W' , 'W' , '  ', 'W'  ],
        [ '  ', 'W' , 'W' , 'TL', 'TR' ],
        [ 'TL', 'TR', '  ', 'BL', 'BR' ],
        [ 'BL', 'BR', 'W' , 'TL', 'TR' ],
        [ '  ', 'W' , '  ', 'BL', 'BR' ],
    ])
    ground_assignment = {get_pos(x=x, y=y): ground[y][x] for x in range(ground.shape[1]) for y in range(ground.shape[0]) if ground[y][x].strip()}
    assert set(solution.keys()) == set(ground_assignment.keys()), f'solution keys != ground assignment keys, {set(solution.keys()) ^ set(ground_assignment.keys())} \n\n\n{solution} \n\n\n{ground_assignment}'
    for pos in solution.keys():
        assert solution[pos] == ground_assignment[pos], f'solution[{pos}] != ground_assignment[{pos}], {solution[pos]} != {ground_assignment[pos]}'


def test_medium():
    # 10 x 10 
    # https://www.puzzle-shakashaka.com/?e=MTo0LDE5OSwyNzM=
    board = np.array([
        ['0', ' ', ' ', ' ', ' ', '1', ' ', ' ', '2', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', '2', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', '4', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        ['B', ' ', ' ', '3', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', 'B', ' ', ' '],
        ['2', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '2'],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', 'B', '0', ' ', ' ', ' ', 'B', ' '],
    ])
    binst = solver.Board(board=board)
    solutions = binst.solve_and_print()
    assert len(solutions) == 1, f'unique solutions != 1, == {len(solutions)}'
    solution = solutions[0].assignment
    # _debug_assignment(solution, board.shape[0], board.shape[1])
    ground = np.array([
        [ '  ', 'W' , 'TL', 'TR', 'W' , '  ', 'TL', 'TR', '  ', 'W'  ],
        [ 'W' , 'TL', 'W' , 'W' , 'TR', 'W' , 'BL', 'BR', 'TL', 'TR' ],
        [ 'W' , 'BL', 'W' , 'W' , 'W' , 'TR', 'W' , '  ', 'BL', 'BR' ],
        [ 'TL', 'TR', 'BL', 'W' , 'W' , 'W' , 'TR', 'W' , 'TL', 'TR' ],
        [ 'BL', 'BR', '  ', 'BL', 'W' , 'W' , 'W' , 'TR', 'BL', 'BR' ],
        [ '  ', 'TL', 'TR', '  ', 'BL', 'W' , 'W' , 'BR', 'TL', 'TR' ],
        [ 'W' , 'BL', 'BR', 'W' , 'W' , 'BL', 'BR', '  ', 'BL', 'BR' ],
        [ '  ', 'TL', 'TR', 'W' , 'W' , 'TL', 'TR', 'TL', 'TR', '  ' ],
        [ 'TL', 'W' , 'BR', 'W' , 'W' , 'BL', 'BR', 'BL', 'BR', 'W'  ],
        [ 'BL', 'BR', 'W' , '  ', '  ', 'W' , 'W' , 'W' , '  ', 'W'  ],
    ])
    ground_assignment = {get_pos(x=x, y=y): ground[y][x] for x in range(ground.shape[1]) for y in range(ground.shape[0]) if ground[y][x].strip()}
    assert set(solution.keys()) == set(ground_assignment.keys()), f'solution keys != ground assignment keys, {set(solution.keys()) ^ set(ground_assignment.keys())} \n\n\n{solution} \n\n\n{ground_assignment}'
    for pos in solution.keys():
        assert solution[pos] == ground_assignment[pos], f'solution[{pos}] != ground_assignment[{pos}], {solution[pos]} != {ground_assignment[pos]}'


def test_ground():
    # 25 x 25
    # https://www.puzzle-shakashaka.com/?e=NDo3LDc4Myw4Mzk=
    board = np.array([
        [' ', ' ', 'B', ' ', '1', ' ', ' ', '1', ' ', ' ', 'B', 'B', ' ', ' ', ' ', '2', ' ', ' ', ' ', ' ', 'B', ' ', 'B', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'B', ' ', ' ', ' ', ' ', 'B', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', '3', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '4', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'B', ' ', ' ', ' ', ' ', ' ', ' ', '3', ' ', ' ', ' ', ' ', ' ', 'B'],
        ['1', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '2', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '4', ' ', ' ', ' ', ' '],
        [' ', ' ', '3', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'B', ' ', ' '],
        [' ', ' ', ' ', '1', ' ', ' ', '2', ' ', ' ', ' ', ' ', 'B', ' ', '3', ' ', ' ', ' ', 'B', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', 'B', ' ', ' ', 'B', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '3', ' ', ' ', ' ', '4', ' ', ' ', ' ', 'B'],
        [' ', 'B', '2', ' ', ' ', 'B', ' ', ' ', ' ', ' ', '3', ' ', ' ', ' ', '2', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '4', ' ', ' '],
        ['B', ' ', ' ', ' ', ' ', 'B', ' ', ' ', '1', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        ['0', ' ', ' ', 'B', ' ', ' ', ' ', ' ', 'B', ' ', ' ', ' ', 'B', 'B', 'B', ' ', ' ', ' ', ' ', '3', ' ', ' ', ' ', ' ', 'B'],
        ['0', ' ', ' ', 'B', ' ', ' ', ' ', 'B', ' ', ' ', ' ', '1', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '3', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '2', ' ', 'B', ' ', ' ', 'B', ' ', ' ', ' ', ' ', ' ', 'B', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', 'B', ' ', ' ', 'B', ' ', 'B', ' ', 'B', ' ', 'B', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', '4', ' ', ' ', '3', ' ', 'B', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'B', ' ', ' ', '4', ' ', ' ', ' ', ' '],
        [' ', 'B', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'B', ' ', ' ', ' ', ' ', '3', ' ', ' ', 'B', ' ', ' ', ' ', ' ', ' ', '3'],
        ['B', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'B', ' ', ' ', ' ', '1', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '4', ' ', ' ', ' '],
        [' ', ' ', 'B', ' ', 'B', ' ', ' ', '2', ' ', ' ', ' ', ' ', ' ', 'B', ' ', ' ', 'B', ' ', ' ', 'B', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '0', ' ', ' ', ' ', ' ', ' ', 'B', ' ', ' '],
        ['B', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'B', ' ', ' ', ' ', ' ', ' ', ' ', 'B', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', '2', 'B', ' ', ' ', '2', ' ', ' ', ' ', ' ', 'B', ' ', ' ', ' ', ' ', '1', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', '3', ' ', ' ', ' ', '2', ' ', ' ', '1', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'B', ' ', 'B', ' ', ' ', ' ', ' '],
        [' ', ' ', 'B', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'B', ' ', ' ', ' ', 'B', ' ', ' ', 'B', ' ', ' ', ' ', ' ', ' ', ' ', '2'],
        ['2', ' ', ' ', 'B', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '3', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'B', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', '3', ' ', ' ', ' ', ' ', ' ', '2', ' ', ' ', ' ', ' ', '0', ' ', ' ', ' ', ' ', ' ', '2', ' '],
    ])
    binst = solver.Board(board=board)
    solutions = binst.solve_and_print()
    assert len(solutions) == 1, f'unique solutions != 1, == {len(solutions)}'
    solution = solutions[0].assignment
    # _debug_assignment(solution, board.shape[0], board.shape[1])
    ground = np.array([
        [ 'TL', 'TR', '  ', 'W' , '  ', 'TL', 'TR', '  ', 'W' , 'W' , '  ', '  ', 'W' , 'TL', 'TR', '  ', 'W' , 'TL', 'TR', 'W' , '  ', 'W' , '  ', 'TL', 'TR' ],
        [ 'BL', 'BR', 'TL', 'TR', 'W' , 'BL', 'BR', 'W' , 'TL', 'TR', 'W' , '  ', 'W' , 'BL', 'W' , 'TR', '  ', 'BL', 'W' , 'TR', 'W' , 'TL', 'TR', 'BL', 'BR' ],
        [ 'W' , 'TL', 'W' , 'W' , 'TR', 'TL', 'TR', '  ', 'BL', 'W' , 'TR', 'W' , 'TL', 'TR', 'BL', 'W' , 'TR', '  ', 'BL', 'BR', 'TL', 'W' , 'W' , 'TR', 'W'  ],
        [ 'W' , 'BL', 'W' , 'W' , 'BR', 'BL', 'BR', 'TL', 'TR', 'BL', 'BR', '  ', 'BL', 'BR', 'W' , 'BL', 'W' , 'TR', '  ', 'W' , 'BL', 'W' , 'W' , 'BR', '  ' ],
        [ '  ', 'W' , 'BL', 'BR', 'TL', 'TR', 'TL', 'W' , 'BR', 'W' , '  ', 'TL', 'TR', 'TL', 'TR', 'W' , 'BL', 'BR', 'TL', 'TR', '  ', 'BL', 'BR', 'W' , 'W'  ],
        [ 'TL', 'TR', '  ', 'W' , 'BL', 'BR', 'BL', 'BR', 'TL', 'TR', 'W' , 'BL', 'BR', 'BL', 'BR', 'TL', 'TR', 'W' , 'BL', 'BR', 'TL', 'TR', '  ', 'TL', 'TR' ],
        [ 'BL', 'W' , 'TR', '  ', 'W' , 'W' , '  ', 'TL', 'W' , 'W' , 'TR', '  ', 'W' , '  ', 'TL', 'W' , 'BR', '  ', 'TL', 'TR', 'BL', 'W' , 'TR', 'BL', 'BR' ],
        [ 'W' , 'BL', 'BR', '  ', 'W' , 'W' , '  ', 'BL', 'W' , 'W' , 'BR', 'W' , 'TL', 'TR', 'BL', 'BR', '  ', 'W' , 'BL', 'BR', '  ', 'BL', 'BR', 'W' , '  ' ],
        [ 'W' , '  ', '  ', 'TL', 'TR', '  ', 'W' , 'W' , 'BL', 'BR', '  ', 'TL', 'W' , 'BR', '  ', 'W' , 'TL', 'TR', 'TL', 'TR', 'TL', 'TR', '  ', 'TL', 'TR' ],
        [ '  ', 'W' , 'W' , 'BL', 'BR', '  ', 'W' , 'W' , '  ', 'W' , 'W' , 'BL', 'BR', 'W' , 'W' , 'TL', 'W' , 'BR', 'BL', 'BR', 'BL', 'BR', 'TL', 'W' , 'BR' ],
        [ '  ', 'W' , 'W' , '  ', 'TL', 'TR', 'W' , 'W' , '  ', 'TL', 'TR', 'W' , '  ', '  ', '  ', 'BL', 'BR', 'TL', 'TR', '  ', 'W' , 'TL', 'W' , 'BR', '  ' ],
        [ '  ', 'W' , 'W' , '  ', 'BL', 'W' , 'TR', '  ', 'TL', 'W' , 'BR', '  ', 'W' , 'TL', 'TR', 'W' , 'TL', 'W' , 'W' , 'TR', 'W' , 'BL', 'BR', '  ', 'W'  ],
        [ 'W' , 'TL', 'TR', 'TL', 'TR', 'BL', 'W' , 'TR', 'BL', 'BR', '  ', 'W' , '  ', 'BL', 'BR', '  ', 'BL', 'W' , 'W' , 'W' , 'TR', '  ', 'TL', 'TR', 'W'  ],
        [ 'TL', 'W' , 'BR', 'BL', 'BR', '  ', 'BL', 'BR', '  ', 'W' , '  ', 'W' , '  ', 'W' , '  ', 'TL', 'TR', 'BL', 'W' , 'W' , 'BR', 'W' , 'BL', 'W' , 'TR' ],
        [ 'BL', 'BR', 'TL', 'TR', '  ', 'TL', 'TR', '  ', 'W' , '  ', 'W' , 'TL', 'TR', 'TL', 'TR', 'BL', 'BR', '  ', 'BL', 'BR', '  ', 'TL', 'TR', 'BL', 'BR' ],
        [ 'W' , '  ', 'BL', 'W' , 'TR', 'BL', 'BR', 'TL', 'TR', 'W' , '  ', 'BL', 'BR', 'BL', 'BR', '  ', 'TL', 'TR', '  ', 'TL', 'TR', 'BL', 'W' , 'TR', '  ' ],
        [ '  ', 'W' , 'W' , 'BL', 'BR', 'W' , 'W' , 'BL', 'BR', '  ', 'TL', 'TR', 'W' , '  ', 'W' , 'W' , 'BL', 'W' , 'TR', 'BL', 'BR', '  ', 'BL', 'W' , 'TR' ],
        [ 'TL', 'TR', '  ', 'W' , '  ', 'W' , 'W' , '  ', 'W' , 'TL', 'W' , 'W' , 'TR', '  ', 'W' , 'W' , '  ', 'BL', 'BR', '  ', 'TL', 'TR', 'W' , 'BL', 'BR' ],
        [ 'BL', 'BR', 'W' , 'TL', 'TR', 'W' , 'W' , 'TL', 'TR', 'BL', 'W' , 'W' , 'W' , 'TR', 'W' , 'W' , '  ', 'W' , 'TL', 'TR', 'BL', 'BR', '  ', 'TL', 'TR' ],
        [ '  ', 'W' , 'TL', 'W' , 'BR', 'W' , 'W' , 'BL', 'BR', '  ', 'BL', 'W' , 'W' , 'BR', 'W' , 'W' , '  ', 'TL', 'W' , 'BR', 'W' , 'W' , 'W' , 'BL', 'BR' ],
        [ 'W' , 'TL', 'W' , 'BR', 'TL', 'TR', '  ', '  ', 'W' , 'W' , '  ', 'BL', 'BR', 'TL', 'TR', '  ', 'TL', 'W' , 'BR', 'W' , '  ', 'TL', 'TR', 'TL', 'TR' ],
        [ 'TL', 'W' , 'BR', '  ', 'BL', 'W' , 'TR', '  ', 'W' , 'W' , '  ', 'TL', 'TR', 'BL', 'BR', 'W' , 'BL', 'BR', '  ', 'W' , '  ', 'BL', 'BR', 'BL', 'BR' ],
        [ 'BL', 'BR', '  ', 'W' , 'W' , 'BL', 'W' , 'TR', 'W' , 'W' , '  ', 'BL', 'W' , 'TR', '  ', 'TL', 'TR', '  ', 'TL', 'TR', 'W' , 'W' , 'TL', 'TR', '  ' ],
        [ '  ', 'TL', 'TR', '  ', 'TL', 'TR', 'BL', 'W' , 'TR', 'TL', 'TR', '  ', 'BL', 'W' , 'TR', 'BL', 'BR', 'W' , 'BL', 'BR', '  ', 'TL', 'W' , 'BR', 'W'  ],
        [ 'W' , 'BL', 'BR', 'W' , 'BL', 'BR', '  ', 'BL', 'BR', 'BL', 'BR', 'W' , '  ', 'BL', 'BR', 'W' , 'W' , '  ', 'W' , 'W' , 'W' , 'BL', 'BR', '  ', 'W'  ],
    ])
    ground_assignment = {get_pos(x=x, y=y): ground[y][x] for x in range(ground.shape[1]) for y in range(ground.shape[0]) if ground[y][x].strip()}
    assert set(solution.keys()) == set(ground_assignment.keys()), f'solution keys != ground assignment keys, {set(solution.keys()) ^ set(ground_assignment.keys())} \n\n\n{solution} \n\n\n{ground_assignment}'
    for pos in solution.keys():
        assert solution[pos] == ground_assignment[pos], f'solution[{pos}] != ground_assignment[{pos}], {solution[pos]} != {ground_assignment[pos]}'


if __name__ == '__main__':
    # _debug_render_bw_tiles_split()
    test_toy()
    test_medium()
    test_ground()
    # _debug_plot_all_rectangles()