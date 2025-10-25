import numpy as np

from puzzle_solver import shakashaka_solver as solver
from puzzle_solver.puzzles.shakashaka.shakashaka import State
from puzzle_solver.core.utils_visualizer import render_bw_tiles_split

def _debug_plot_all_rectangles():
    H, V = 7, 6
    rectangles = solver.init_rectangles(V, H)
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
    # for r in binst.rectangles_on_board:
    #     print(f'rectangle {r.translate} {r.width}x{r.height}:{r.rectangle.is_rotated}')


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
    


if __name__ == '__main__':
    test_toy()
    test_medium()
    # _debug_plot_all_rectangles()