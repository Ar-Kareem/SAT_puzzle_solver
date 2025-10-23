import numpy as np

from puzzle_solver import rectangles_solver as solver
from puzzle_solver.core.utils import get_pos


def test_easy():
    # 5x5 easy
    # https://www.puzzle-shikaku.com/?e=MDo5LDM2NiwwNjg=
    board = np.array([
        [' ', ' ', ' ', '2', ' '],
        [' ', ' ', '2', '2', ' '],
        ['3', '3', ' ', '3', ' '],
        [' ', '2', ' ', ' ', '2'],
        [' ', '2', '2', ' ', '2'],
    ])
    binst = solver.Board(board=board)
    solutions = binst.solve_and_print()
    assert len(solutions) == 1, f'unique solutions != 1, == {len(solutions)}'
    solution = solutions[0].assignment
    ground = np.array([
        ['id3:N=3:3x1', 'id4:N=3:3x1', 'id1:N=2:2x1', 'id0:N=2:1x2', 'id0:N=2:1x2'],
        ['id3:N=3:3x1', 'id4:N=3:3x1', 'id1:N=2:2x1', 'id2:N=2:1x2', 'id2:N=2:1x2'],
        ['id3:N=3:3x1', 'id4:N=3:3x1', 'id5:N=3:1x3', 'id5:N=3:1x3', 'id5:N=3:1x3'],
        ['id6:N=2:1x2', 'id6:N=2:1x2', 'id9:N=2:2x1', 'id7:N=2:1x2', 'id7:N=2:1x2'],
        ['id8:N=2:1x2', 'id8:N=2:1x2', 'id9:N=2:2x1', 'id10:N=2:1x2', 'id10:N=2:1x2'],
    ])
    ground_assignment = {get_pos(x=x, y=y): ground[y][x] for x in range(ground.shape[1]) for y in range(ground.shape[0])}
    assert set(solution.keys()) == set(ground_assignment.keys()), f'solution keys != ground assignment keys, {set(solution.keys()) ^ set(ground_assignment.keys())} \n\n\n{solution} \n\n\n{ground_assignment}'
    for pos in solution.keys():
        assert solution[pos] == ground_assignment[pos], f'solution[{pos}] != ground_assignment[{pos}], {solution[pos]} != {ground_assignment[pos]}'


def test_easy_2():
    # 9x9
    # https://www.chiark.greenend.org.uk/~sgtatham/puzzles/js/rect.html#9x9:a2c4_6a2c6f12b2q2_2d2b2c8a2_4c3c6e8e8d
    board = np.array([
        [' ', '2', ' ', ' ', ' ', '4', '6', ' ', '2'],
        [' ', ' ', ' ', '6', ' ', ' ', ' ', ' ', ' '],
        [' ', '12',' ', ' ', '2', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', '2', '2', ' ', ' ', ' '],
        [' ', '2', ' ', ' ', '2', ' ', ' ', ' ', '8'],
        [' ', '2', '4', ' ', ' ', ' ', '3', ' ', ' '],
        [' ', '6', ' ', ' ', ' ', ' ', ' ', '8', ' '],
        [' ', ' ', ' ', ' ', '8', ' ', ' ', ' ', ' '],
    ])
    binst = solver.Board(board=board)
    solutions = binst.solve_and_print()
    assert len(solutions) == 1, f'unique solutions != 1, == {len(solutions)}'
    solution = solutions[0].assignment
    ground = np.array([
        ['id0:N=2:1x2', 'id0:N=2:1x2', 'id1:N=4:1x4', 'id1:N=4:1x4', 'id1:N=4:1x4', 'id1:N=4:1x4', 'id2:N=6:6x1', 'id3:N=2:1x2', 'id3:N=2:1x2'],
        ['id4:N=6:1x6', 'id4:N=6:1x6', 'id4:N=6:1x6', 'id4:N=6:1x6', 'id4:N=6:1x6', 'id4:N=6:1x6', 'id2:N=6:6x1', 'id16:N=8:8x1', 'id11:N=8:8x1'],
        ['id5:N=12:3x4', 'id5:N=12:3x4', 'id5:N=12:3x4', 'id5:N=12:3x4', 'id6:N=2:1x2', 'id6:N=2:1x2', 'id2:N=6:6x1', 'id16:N=8:8x1', 'id11:N=8:8x1'],
        ['id5:N=12:3x4', 'id5:N=12:3x4', 'id5:N=12:3x4', 'id5:N=12:3x4', 'id7:N=2:2x1', 'id8:N=2:2x1', 'id2:N=6:6x1', 'id16:N=8:8x1', 'id11:N=8:8x1'],
        ['id5:N=12:3x4', 'id5:N=12:3x4', 'id5:N=12:3x4', 'id5:N=12:3x4', 'id7:N=2:2x1', 'id8:N=2:2x1', 'id2:N=6:6x1', 'id16:N=8:8x1', 'id11:N=8:8x1'],
        ['id9:N=2:1x2', 'id9:N=2:1x2', 'id13:N=4:2x2', 'id13:N=4:2x2', 'id10:N=2:1x2', 'id10:N=2:1x2', 'id2:N=6:6x1', 'id16:N=8:8x1', 'id11:N=8:8x1'],
        ['id12:N=2:1x2', 'id12:N=2:1x2', 'id13:N=4:2x2', 'id13:N=4:2x2', 'id14:N=3:1x3', 'id14:N=3:1x3', 'id14:N=3:1x3', 'id16:N=8:8x1', 'id11:N=8:8x1'],
        ['id15:N=6:2x3', 'id15:N=6:2x3', 'id15:N=6:2x3', 'id17:N=8:2x4', 'id17:N=8:2x4', 'id17:N=8:2x4', 'id17:N=8:2x4', 'id16:N=8:8x1', 'id11:N=8:8x1'],
        ['id15:N=6:2x3', 'id15:N=6:2x3', 'id15:N=6:2x3', 'id17:N=8:2x4', 'id17:N=8:2x4', 'id17:N=8:2x4', 'id17:N=8:2x4', 'id16:N=8:8x1', 'id11:N=8:8x1'],
    ])
    ground_assignment = {get_pos(x=x, y=y): ground[y][x] for x in range(ground.shape[1]) for y in range(ground.shape[0])}
    assert set(solution.keys()) == set(ground_assignment.keys()), f'solution keys != ground assignment keys, {set(solution.keys()) ^ set(ground_assignment.keys())} \n\n\n{solution} \n\n\n{ground_assignment}'
    for pos in solution.keys():
        assert solution[pos] == ground_assignment[pos], f'solution[{pos}] != ground_assignment[{pos}], {solution[pos]} != {ground_assignment[pos]}'


def test_ground():
    # 19 x 19
    # https://www.chiark.greenend.org.uk/~sgtatham/puzzles/js/rect.html#19x19%23216859691507309
    board = np.array([
        ['3', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '15',' ', ' ', ' ', ' ' ],
        [' ', ' ', '2', '2', ' ', ' ', ' ', ' ', ' ', ' ', '11',' ', ' ', ' ', ' ', ' ', ' ', '3', '2' ],
        [' ', ' ', ' ', ' ', '2', ' ', ' ', ' ', '11',' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '2', ' ' ],
        [' ', ' ', ' ', '2', ' ', ' ', ' ', ' ', ' ', ' ', '6', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ' ],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '3', ' ', ' ', ' ', ' ', ' ', ' ', ' ' ],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '2', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ' ],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '2', ' ', ' ', ' ', ' ', ' ', ' ', ' ' ],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '28','4', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ' ],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '10',' ', '10',' ', ' ', ' ', ' ', '45',' ' ],
        [' ', ' ', '3', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ' ],
        [' ', '22',' ', ' ', ' ', ' ', ' ', '28',' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '17'],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ' ],
        [' ', '8', '3', ' ', ' ', '2', '2', ' ', ' ', ' ', '5', ' ', ' ', '4', ' ', ' ', ' ', ' ', ' ' ],
        [' ', ' ', ' ', ' ', '4', ' ', ' ', '8', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '2', ' ', ' ', ' ' ],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '3', ' ' ],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ' ],
        ['2', ' ', ' ', ' ', '12',' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ' ],
        ['2', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ' ],
        [' ', ' ', '3', '2', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '60',' ', ' ', ' ', ' ', ' ', '4', ' ' ],
    ])
    binst = solver.Board(board=board)
    solutions = binst.solve_and_print()
    assert len(solutions) == 1, f'unique solutions != 1, == {len(solutions)}'
    solution = solutions[0].assignment
    ground = np.array([
        ['id0:N=3:1x3', 'id0:N=3:1x3', 'id0:N=3:1x3', 'id1:N=15:1x15', 'id1:N=15:1x15', 'id1:N=15:1x15', 'id1:N=15:1x15', 'id1:N=15:1x15', 'id1:N=15:1x15', 'id1:N=15:1x15', 'id1:N=15:1x15', 'id1:N=15:1x15', 'id1:N=15:1x15', 'id1:N=15:1x15', 'id1:N=15:1x15', 'id1:N=15:1x15', 'id1:N=15:1x15', 'id1:N=15:1x15', 'id6:N=2:2x1'],
        ['id21:N=22:11x2', 'id21:N=22:11x2', 'id2:N=2:2x1', 'id3:N=2:2x1', 'id4:N=11:1x11', 'id4:N=11:1x11', 'id4:N=11:1x11', 'id4:N=11:1x11', 'id4:N=11:1x11', 'id4:N=11:1x11', 'id4:N=11:1x11', 'id4:N=11:1x11', 'id4:N=11:1x11', 'id4:N=11:1x11', 'id4:N=11:1x11', 'id5:N=3:1x3', 'id5:N=3:1x3', 'id5:N=3:1x3', 'id6:N=2:2x1'],
        ['id21:N=22:11x2', 'id21:N=22:11x2', 'id2:N=2:2x1', 'id3:N=2:2x1', 'id7:N=2:2x1', 'id8:N=11:1x11', 'id8:N=11:1x11', 'id8:N=11:1x11', 'id8:N=11:1x11', 'id8:N=11:1x11', 'id8:N=11:1x11', 'id8:N=11:1x11', 'id8:N=11:1x11', 'id8:N=11:1x11', 'id8:N=11:1x11', 'id8:N=11:1x11', 'id9:N=2:1x2', 'id9:N=2:1x2', 'id23:N=17:17x1'],
        ['id21:N=22:11x2', 'id21:N=22:11x2', 'id10:N=2:1x2', 'id10:N=2:1x2', 'id7:N=2:2x1', 'id11:N=6:1x6', 'id11:N=6:1x6', 'id11:N=6:1x6', 'id11:N=6:1x6', 'id11:N=6:1x6', 'id11:N=6:1x6', 'id12:N=3:3x1', 'id18:N=10:10x1', 'id19:N=45:9x5', 'id19:N=45:9x5', 'id19:N=45:9x5', 'id19:N=45:9x5', 'id19:N=45:9x5', 'id23:N=17:17x1'],
        ['id21:N=22:11x2', 'id21:N=22:11x2', 'id15:N=28:4x7', 'id15:N=28:4x7', 'id15:N=28:4x7', 'id15:N=28:4x7', 'id15:N=28:4x7', 'id15:N=28:4x7', 'id15:N=28:4x7', 'id16:N=4:4x1', 'id13:N=2:2x1', 'id12:N=3:3x1', 'id18:N=10:10x1', 'id19:N=45:9x5', 'id19:N=45:9x5', 'id19:N=45:9x5', 'id19:N=45:9x5', 'id19:N=45:9x5', 'id23:N=17:17x1'],
        ['id21:N=22:11x2', 'id21:N=22:11x2', 'id15:N=28:4x7', 'id15:N=28:4x7', 'id15:N=28:4x7', 'id15:N=28:4x7', 'id15:N=28:4x7', 'id15:N=28:4x7', 'id15:N=28:4x7', 'id16:N=4:4x1', 'id13:N=2:2x1', 'id12:N=3:3x1', 'id18:N=10:10x1', 'id19:N=45:9x5', 'id19:N=45:9x5', 'id19:N=45:9x5', 'id19:N=45:9x5', 'id19:N=45:9x5', 'id23:N=17:17x1'],
        ['id21:N=22:11x2', 'id21:N=22:11x2', 'id15:N=28:4x7', 'id15:N=28:4x7', 'id15:N=28:4x7', 'id15:N=28:4x7', 'id15:N=28:4x7', 'id15:N=28:4x7', 'id15:N=28:4x7', 'id16:N=4:4x1', 'id14:N=2:1x2', 'id14:N=2:1x2', 'id18:N=10:10x1', 'id19:N=45:9x5', 'id19:N=45:9x5', 'id19:N=45:9x5', 'id19:N=45:9x5', 'id19:N=45:9x5', 'id23:N=17:17x1'],
        ['id21:N=22:11x2', 'id21:N=22:11x2', 'id15:N=28:4x7', 'id15:N=28:4x7', 'id15:N=28:4x7', 'id15:N=28:4x7', 'id15:N=28:4x7', 'id15:N=28:4x7', 'id15:N=28:4x7', 'id16:N=4:4x1', 'id17:N=10:5x2', 'id17:N=10:5x2', 'id18:N=10:10x1', 'id19:N=45:9x5', 'id19:N=45:9x5', 'id19:N=45:9x5', 'id19:N=45:9x5', 'id19:N=45:9x5', 'id23:N=17:17x1'],
        ['id21:N=22:11x2', 'id21:N=22:11x2', 'id20:N=3:3x1', 'id22:N=28:4x7', 'id22:N=28:4x7', 'id22:N=28:4x7', 'id22:N=28:4x7', 'id22:N=28:4x7', 'id22:N=28:4x7', 'id22:N=28:4x7', 'id17:N=10:5x2', 'id17:N=10:5x2', 'id18:N=10:10x1', 'id19:N=45:9x5', 'id19:N=45:9x5', 'id19:N=45:9x5', 'id19:N=45:9x5', 'id19:N=45:9x5', 'id23:N=17:17x1'],
        ['id21:N=22:11x2', 'id21:N=22:11x2', 'id20:N=3:3x1', 'id22:N=28:4x7', 'id22:N=28:4x7', 'id22:N=28:4x7', 'id22:N=28:4x7', 'id22:N=28:4x7', 'id22:N=28:4x7', 'id22:N=28:4x7', 'id17:N=10:5x2', 'id17:N=10:5x2', 'id18:N=10:10x1', 'id19:N=45:9x5', 'id19:N=45:9x5', 'id19:N=45:9x5', 'id19:N=45:9x5', 'id19:N=45:9x5', 'id23:N=17:17x1'],
        ['id21:N=22:11x2', 'id21:N=22:11x2', 'id20:N=3:3x1', 'id22:N=28:4x7', 'id22:N=28:4x7', 'id22:N=28:4x7', 'id22:N=28:4x7', 'id22:N=28:4x7', 'id22:N=28:4x7', 'id22:N=28:4x7', 'id17:N=10:5x2', 'id17:N=10:5x2', 'id18:N=10:10x1', 'id19:N=45:9x5', 'id19:N=45:9x5', 'id19:N=45:9x5', 'id19:N=45:9x5', 'id19:N=45:9x5', 'id23:N=17:17x1'],
        ['id21:N=22:11x2', 'id21:N=22:11x2', 'id25:N=3:3x1', 'id22:N=28:4x7', 'id22:N=28:4x7', 'id22:N=28:4x7', 'id22:N=28:4x7', 'id22:N=28:4x7', 'id22:N=28:4x7', 'id22:N=28:4x7', 'id17:N=10:5x2', 'id17:N=10:5x2', 'id18:N=10:10x1', 'id19:N=45:9x5', 'id19:N=45:9x5', 'id19:N=45:9x5', 'id19:N=45:9x5', 'id19:N=45:9x5', 'id23:N=17:17x1'],
        ['id24:N=8:4x2', 'id24:N=8:4x2', 'id25:N=3:3x1', 'id30:N=4:2x2', 'id30:N=4:2x2', 'id26:N=2:2x1', 'id27:N=2:2x1', 'id28:N=5:1x5', 'id28:N=5:1x5', 'id28:N=5:1x5', 'id28:N=5:1x5', 'id28:N=5:1x5', 'id18:N=10:10x1', 'id29:N=4:1x4', 'id29:N=4:1x4', 'id29:N=4:1x4', 'id29:N=4:1x4', 'id33:N=3:3x1', 'id23:N=17:17x1'],
        ['id24:N=8:4x2', 'id24:N=8:4x2', 'id25:N=3:3x1', 'id30:N=4:2x2', 'id30:N=4:2x2', 'id26:N=2:2x1', 'id27:N=2:2x1', 'id31:N=8:1x8', 'id31:N=8:1x8', 'id31:N=8:1x8', 'id31:N=8:1x8', 'id31:N=8:1x8', 'id31:N=8:1x8', 'id31:N=8:1x8', 'id31:N=8:1x8', 'id32:N=2:1x2', 'id32:N=2:1x2', 'id33:N=3:3x1', 'id23:N=17:17x1'],
        ['id24:N=8:4x2', 'id24:N=8:4x2', 'id35:N=12:4x3', 'id35:N=12:4x3', 'id35:N=12:4x3', 'id39:N=60:5x12', 'id39:N=60:5x12', 'id39:N=60:5x12', 'id39:N=60:5x12', 'id39:N=60:5x12', 'id39:N=60:5x12', 'id39:N=60:5x12', 'id39:N=60:5x12', 'id39:N=60:5x12', 'id39:N=60:5x12', 'id39:N=60:5x12', 'id39:N=60:5x12', 'id33:N=3:3x1', 'id23:N=17:17x1'],
        ['id24:N=8:4x2', 'id24:N=8:4x2', 'id35:N=12:4x3', 'id35:N=12:4x3', 'id35:N=12:4x3', 'id39:N=60:5x12', 'id39:N=60:5x12', 'id39:N=60:5x12', 'id39:N=60:5x12', 'id39:N=60:5x12', 'id39:N=60:5x12', 'id39:N=60:5x12', 'id39:N=60:5x12', 'id39:N=60:5x12', 'id39:N=60:5x12', 'id39:N=60:5x12', 'id39:N=60:5x12', 'id40:N=4:4x1', 'id23:N=17:17x1'],
        ['id34:N=2:1x2', 'id34:N=2:1x2', 'id35:N=12:4x3', 'id35:N=12:4x3', 'id35:N=12:4x3', 'id39:N=60:5x12', 'id39:N=60:5x12', 'id39:N=60:5x12', 'id39:N=60:5x12', 'id39:N=60:5x12', 'id39:N=60:5x12', 'id39:N=60:5x12', 'id39:N=60:5x12', 'id39:N=60:5x12', 'id39:N=60:5x12', 'id39:N=60:5x12', 'id39:N=60:5x12', 'id40:N=4:4x1', 'id23:N=17:17x1'],
        ['id36:N=2:1x2', 'id36:N=2:1x2', 'id35:N=12:4x3', 'id35:N=12:4x3', 'id35:N=12:4x3', 'id39:N=60:5x12', 'id39:N=60:5x12', 'id39:N=60:5x12', 'id39:N=60:5x12', 'id39:N=60:5x12', 'id39:N=60:5x12', 'id39:N=60:5x12', 'id39:N=60:5x12', 'id39:N=60:5x12', 'id39:N=60:5x12', 'id39:N=60:5x12', 'id39:N=60:5x12', 'id40:N=4:4x1', 'id23:N=17:17x1'],
        ['id37:N=3:1x3', 'id37:N=3:1x3', 'id37:N=3:1x3', 'id38:N=2:1x2', 'id38:N=2:1x2', 'id39:N=60:5x12', 'id39:N=60:5x12', 'id39:N=60:5x12', 'id39:N=60:5x12', 'id39:N=60:5x12', 'id39:N=60:5x12', 'id39:N=60:5x12', 'id39:N=60:5x12', 'id39:N=60:5x12', 'id39:N=60:5x12', 'id39:N=60:5x12', 'id39:N=60:5x12', 'id40:N=4:4x1', 'id23:N=17:17x1'],
    ])
    ground_assignment = {get_pos(x=x, y=y): ground[y][x] for x in range(ground.shape[1]) for y in range(ground.shape[0])}
    assert set(solution.keys()) == set(ground_assignment.keys()), f'solution keys != ground assignment keys, {set(solution.keys()) ^ set(ground_assignment.keys())} \n\n\n{solution} \n\n\n{ground_assignment}'
    for pos in solution.keys():
        assert solution[pos] == ground_assignment[pos], f'solution[{pos}] != ground_assignment[{pos}], {solution[pos]} != {ground_assignment[pos]}'


if __name__ == '__main__':
    test_easy()
    test_easy_2()
    test_ground()
