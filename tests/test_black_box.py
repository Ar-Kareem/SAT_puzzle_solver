import pytest

from puzzle_solver import black_box_solver as solver


def test_5x5_3_balls():
    # simple 5x5 board
    # https://www.chiark.greenend.org.uk/~sgtatham/puzzles/js/blackbox.html#w5h5m3M3:ea3e663bd73f2e86
    top = ['H', '1', '2', 'H', 'H']
    left = ['3', 'R', 'H', 'H', 'R']
    right = ['3', '1', 'H', 'R', 'H']
    bottom = ['H', 'H', '2', 'R', 'H']
    solver.Board(top=top, left=left, bottom=bottom, right=right, ball_count=(3, 3)).solve_and_print()

def test_6x6_4_balls():
    # https://www.chiark.greenend.org.uk/~sgtatham/puzzles/js/blackbox.html#w6h6m4M4:c5afcdaa057df836d906
    top = ['H', 'R', '1', 'H', '2', '3']
    left = ['H', 'R', 'H', '1', 'H', '6']
    right = ['H', '2', '3', 'H', '4', '5']
    bottom = ['H', '6', 'H', '5', 'H', '4']
    solver.Board(top=top, left=left, bottom=bottom, right=right, ball_count=(4, 4)).solve_and_print()

@pytest.mark.slow
def test_8x8_3_6_balls():
    # 8x8 board 3-6 balls
    # https://www.chiark.greenend.org.uk/~sgtatham/puzzles/js/blackbox.html#w8h8m3M6:0b41bc0d0c95e1a9578c46a4
    top = ['1', 'H', 'R', 'R', 'H', 'R', '2', '3']
    left = ['H', '1', 'H', '7', '5', '6', 'H', 'H']
    right = ['2', 'H', '4', 'H', '5', '6', 'H', 'H']
    bottom = ['7', 'R', 'H', 'R', 'H', 'R', '4', '3']
    solver.Board(top=top, left=left, bottom=bottom, right=right, ball_count=(3, 6)).solve_and_print()

# def dummy():
    # solver.Board(top=[1, 'H', 2], left=[1, 'H', 4], bottom=[4, 'H', 3], right=[2, 'H', 3]).solve_and_print()
    # solver.Board(top=range(8), right=range(8), bottom=range(8), left=range(8)).solve_and_print()
    # solver.Board(top=range(3), right=range(3), bottom=range(3), left=range(3)).solve_and_print()

if __name__ == '__main__':
    test_5x5_3_balls()
    test_6x6_4_balls()
    test_8x8_3_6_balls()
