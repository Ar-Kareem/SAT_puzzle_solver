import numpy as np

from puzzle_solver.puzzles.nonograms import nonograms_colored as solver
from puzzle_solver.core.utils import get_pos


def viz_matplotlib(arr: list[list[str]]):
    import matplotlib.pyplot as plt
    from matplotlib.colors import ListedColormap
    V = len(arr)
    H = max(len(row) for row in arr)
    arr = np.array([['0b'] * (H - len(row)) + row for row in arr])
    # strip letter and only keep number
    arr_num = [[int(cell.strip()[:-1]) for cell in row] for row in arr]
    colors = [[cell.strip()[-1] for cell in row] for row in arr]
    colors_dict = {
        'M': 'darkmagenta',
        'R': 'magenta',
        'G': 'green',
        'P': 'pink',
        'L': 'lime',
        'F': 'brown',
        'b': 'black',
    }
    colors_as_num = [[{'M': 0, 'R': 1, 'G': 2, 'P': 3, 'L': 4, 'F': 5, 'b': 6}[c] for c in row] for row in colors]
    plt.imshow(colors_as_num,
               cmap=ListedColormap(colors_dict.values()),
               aspect='equal')
    # add text to each cell
    for i in range(V):
        for j in range(H):
            plt.text(j, i, arr_num[i][j], ha='center', va='center')
    plt.colorbar(ticks=[0, 1, 2, 3, 4, 5])
    plt.show()


def test_toy():
    top = [
        [(3, 'R'), (1, 'G')],
        [(2, 'R'), (2, 'G')],
        [(3, 'R'), (1, 'G')],
    ]
    side = [
        [(3, 'R')],
        [(3, 'R')],
        [(1, 'R'), (1, 'G'), (1, 'R')],
        [(3, 'G')]
    ]
    binst = solver.Board(top=top, side=side)
    solutions = binst.solve_and_print()
    assert len(solutions) == 1, f'unique solutions != 1, == {len(solutions)}'
    solution = solutions[0].assignment
    ground = np.array([
        ['R', 'R', 'R'],
        ['R', 'R', 'R'],
        ['R', 'G', 'R'],
        ['G', 'G', 'G']
    ])
    ground_assignment = {get_pos(x=x, y=y): ground[y][x] for x in range(ground.shape[1]) for y in range(ground.shape[0])}
    assert set(solution.keys()) == set(ground_assignment.keys()), f'solution keys != ground assignment keys, {set(solution.keys()) - set(ground_assignment.keys())} \n\n\n{solution} \n\n\n{ground_assignment}'


def test_toy2():
    top = [
        [(3, 'R'), (1, 'G')],
        [(1, 'R'), (1, 'G')],
        [(3, 'R'), (1, 'G')],
    ]
    side = [
        [(1, 'R'), (1, 'R')],
        [(3, 'R')],
        [(1, 'R'), (1, 'R')],
        [(3, 'G')]
    ]
    binst = solver.Board(top=top, side=side)
    solutions = binst.solve_and_print()
    assert len(solutions) == 1, f'unique solutions != 1, == {len(solutions)}'
    solution = solutions[0].assignment
    ground = np.array([
        ['R', ' ', 'R'],
        ['R', 'R', 'R'],
        ['R', ' ', 'R'],
        ['G', 'G', 'G']
    ])
    ground_assignment = {get_pos(x=x, y=y): ground[y][x] for x in range(ground.shape[1]) for y in range(ground.shape[0])}
    assert set(solution.keys()) == set(ground_assignment.keys()), f'solution keys != ground assignment keys, {set(solution.keys()) - set(ground_assignment.keys())} \n\n\n{solution} \n\n\n{ground_assignment}'


def test_ground():
    # 24 x 29
    # https://www.nonograms.org/nonograms2/i/8778
    # colors: M (dark magenta), R (Red-Violet), G (green), P (pink), L (lime), F (forest green)
    # top = """
    # 1   2   3   4   5   6   7   8   9   10  11  12  13  14  15  16  17  18  19  20  21  22  23  24  25  26  27  28  29  30  31  32  33  34
    # .   .   .   .   .   .   .   .   1L  .   .   .   .   .   .   .   .   .   .   .   .   .   .   1L  .   .   1L  .   .   .   .   .   .   .
    # .   .   .   .   .   .   .   .   2G  2L  .   1G  .   .   .   .   .   .   .   .   .   .   .   1G  1L  .   1F  .   .   .   .   .   .   .
    # .   .   .   .   .   .   .   .   1G  2G  3L  1L  1G  1L  .   .   .   .   .   .   .   1L  .   1F  1F  .   1R  1G  1L  .   .   .   .   .
    # .   .   .   .   .   .   .   1G  2F  2F  1F  1F  2L  1G  1L  1L  1L  .   .   .   .   1G  1L  4R  6R  1L  3L  3L  1L  1G  3G  .   .   .
    # .   .   .   .   .   .   .   2M  3M  4M  1R  1R  2R  3R  3R  3R  3R  2R  .   .   1G  1F  2F  5P  2P  1F  1M  1G  3G  3L  2F  .   1L  .
    # .   .   .   .   .   .   .   2R  1R  1R  2M  2M  1M  1M  2M  1M  1M  1M  1R  .   1R  2R  3R  5R  6R  12R 3R  11M 11M 1G  2L  .   1G  .
    # .   .   1M  1M  .   .   .   3P  5P  6P  8P  8P  8P  8P  7P  8P  8P  9P  9P  10P 9P  8P  6P  3M  3M  4M  7M  7P  1R  4F  1F  4G  1F  .
    # .   .   3R  5R  8R  10R 10R 7R  6R  5R  5R  5R  5R  5R  6R  5R  5R  5R  5R  5R  5R  5R  5R  3P  4P  6P  7P  1R  6P  6M  4M  1F  1L  2F
    # 5M  8M  6M  5M  4M  4M  4M  3M  3M  3M  3M  3M  3M  3M  3M  4M  4M  3M  3M  3M  4M  6M  7M  2M  2M  1M  1M  1M  2R  9R  7R  4L  2L  1L
    # """
    # top = [[cell for cell in line.split() if cell] for line in top.split('\n')[2:] if line.strip()]
    # viz_matplotlib([[cell if cell != '.' else '0b' for cell in row] for row in top])
    # top = np.array(top).T
    # top = [[cell for cell in row if cell != '.'] for row in top]
    # side = """
    # .   .   .   .   .   .   .   .   .   1L  1G
    # .   .   .   .   .   .   .   .   .   1L  1G
    # .   .   .   .   .   .   .   .   .   1L  2G
    # .   .   .   .   .   .   .   6L  1G  2L  2G
    # .   .   .   .   2L  1G  3F  1L  2G  1F  1G
    # .   1G  1L  1G  2F  3R  1L  1G  2F  1G  1L
    # 2G  1L  1G  2F  3R  2L  1G  1F  1L  1F  1G
    # 1G  1L  2G  4L  5R  1L  1G  1M  1F  2L  1F
    # 1G  1F  3L  1G  4R  6R  1L  2M  2F  2L  1F
    # .   .   .   4F  1L  6R  3P  4R  5M  1L  1F
    # .   .   1G  1F  1M  7R  1M  6P  3R  4M  2L
    # .   .   .   .   5M  2R  3M  8P  2R  4M  2L
    # .   .   .   .   .   .   .   8M 10P  2R  4M
    # .   .   .   .   .   .   .   2M 14P  2R  4M
    # .   .   .   .   .   .   .   3R 14P  2R  4M
    # .   .   .   .   .   .   .   3R 15P  3R  3M
    # .   .   .   .   .   .   .   3R 15P  4R  3M
    # .   .   .   .   .   .   1M  3R 14P  4R  4M
    # .   .   .   .   .   1M  4R 13P  5R  3M  2R
    # .   .   .   .   1M  6R 10P  6R  3M  2P  2R
    # .   .   .   .   1M  7R  5P  9R  3M  3P  2R
    # .   .   .   .   .   .   2M 20R  3M  4P  2R
    # .   .   .   .   .   .   3M 18R  3M  5P  2R
    # .   .   .   .   .   .   4M 16R  3M  6P  2R
    # .   .   .   .   .   .   5M 13R  5M  6P  2R
    # .   .   .   .   .   .   7M  8R  8M  5P  3R
    # .   .   .   .   .   .   .   .  24M  2P  3R
    # .   .   .   .   .   .   .   .   .  16M  7M
    # .   .   .   .   .   .   .   .   .   .  12M
    # """
    # side = [[cell for cell in line.split() if cell.strip() not in ['.', '']] for line in side.split('\n')[1:] if line.strip()]
    # viz_matplotlib(side)
    top = [
        ['5M'], ['8M'], ['1M', '3R', '6M'], ['1M', '5R', '5M'], ['8R', '4M'],
        ['10R', '4M'], ['10R', '4M'], ['1G', '2M', '2R', '3P', '7R', '3M'], ['1L', '2G', '1G', '2F', '3M', '1R', '5P', '6R', '3M'], ['2L', '2G', '2F', '4M', '1R', '6P', '5R', '3M'],
        ['3L', '1F', '1R', '2M', '8P', '5R', '3M'], ['1G', '1L', '1F', '1R', '2M', '8P', '5R', '3M'], ['1G', '2L', '2R', '1M', '8P', '5R', '3M'], ['1L', '1G', '3R', '1M', '8P', '5R', '3M'], ['1L', '3R', '2M', '7P', '6R', '3M'],
        ['1L', '3R', '1M', '8P', '5R', '4M'], ['1L', '3R', '1M', '8P', '5R', '4M'], ['2R', '1M', '9P', '5R', '3M'], ['1R', '9P', '5R', '3M'], ['10P', '5R', '3M'],
        ['1G', '1R', '9P', '5R', '4M'], ['1L', '1G', '1F', '2R', '8P', '5R', '6M'], ['1L', '2F', '3R', '6P', '5R', '7M'], ['1L', '1G', '1F', '4R', '5P', '5R', '3M', '3P', '2M'], ['1L', '1F', '6R', '2P', '6R', '3M', '4P', '2M'],
        ['1L', '1F', '12R', '4M', '6P', '1M'], ['1L', '1F', '1R', '3L', '1M', '3R', '7M', '7P', '1M'], ['1G', '3L', '1G', '11M', '7P', '1R', '1M'], ['1L', '1L', '3G', '11M', '1R', '6P', '2R'], ['1G', '3L', '1G', '4F', '6M', '9R'],
        ['3G', '2F', '2L', '1F', '4M', '7R'], ['4G', '1F', '4L'], ['1L', '1G', '1F', '1L', '2L'], ['2F', '1L']
    ]
    side = [
        ['1L', '1G'], ['1L', '1G'], ['1L', '2G'], ['6L', '1G', '2L', '2G'], ['2L', '1G', '3F', '1L', '2G', '1F', '1G'],
        ['1G', '1L', '1G', '2F', '3R', '1L', '1G', '2F', '1G', '1L'], ['2G', '1L', '1G', '2F', '3R', '2L', '1G', '1F', '1L', '1F', '1G'], ['1G', '1L', '2G', '4L', '5R', '1L', '1G', '1M', '1F', '2L', '1F'], ['1G', '1F', '3L', '1G', '4R', '6R', '1L', '2M', '2F', '2L', '1F'], ['4F', '1L', '6R', '3P', '4R', '5M', '1L', '1F'],
        ['1G', '1F', '1M', '7R', '1M', '6P', '3R', '4M', '2L'], ['5M', '2R', '3M', '8P', '2R', '4M', '2L'], ['8M', '10P', '2R', '4M'], ['2M', '14P', '2R', '4M'], ['3R', '14P', '2R', '4M'],
        ['3R', '15P', '3R', '3M'], ['3R', '15P', '4R', '3M'], ['1M', '3R', '14P', '4R', '4M'], ['1M', '4R', '13P', '5R', '3M', '2R'], ['1M', '6R', '10P', '6R', '3M', '2P', '2R'],
        ['1M', '7R', '5P', '9R', '3M', '3P', '2R'], ['2M', '20R', '3M', '4P', '2R'], ['3M', '18R', '3M', '5P', '2R'], ['4M', '16R', '3M', '6P', '2R'], ['5M', '13R', '5M', '6P', '2R'],
        ['7M', '8R', '8M', '5P', '3R'], ['24M', '2P', '3R'], ['16M', '7M'], ['12M']
    ]
    binst = solver.Board(top=top, side=side)
    solutions = binst.solve_and_print()
    #     visualize_colors={
    #     'M': 'darkmagenta',
    #     'R': 'magenta',
    #     'G': 'green',
    #     'P': 'pink',
    #     'L': 'lime',
    #     'F': 'forestgreen',
    # })
    assert len(solutions) == 1, f'unique solutions != 1, == {len(solutions)}'
    solution = solutions[0].assignment
    # print(solution)
    ground = np.array([
        "                            LG    ",
        "                             LG   ",
        "                             LGG  ",
        "                     LLLLLLGLLGG  ",
        "        LL             GFFFLGGFG  ",
        "        GL           GFFRRRLGFFGL ",
        "        GGL         GFFRRRLLGFLFG ",
        "         GLGGLLLL    RRRRRLGMFLLF ",
        "        GFLLLGRRRR  RRRRRRLMMFFLLF",
        "        FFFFLRRRRRRPPPRRRRMMMMML F",
        "       GFMRRRRRRRMPPPPPPRRRMMMMLL ",
        "       MMMMMRRMMMPPPPPPPPRRMMMM LL",
        "       MMMMMMMMPPPPPPPPPPRRMMMM   ",
        "        MMPPPPPPPPPPPPPPRRMMMM    ",
        "       RRRPPPPPPPPPPPPPPRRMMMM    ",
        "     RRRPPPPPPPPPPPPPPPRRRMMM     ",
        "    RRRPPPPPPPPPPPPPPPRRRRMMM     ",
        "   MRRRPPPPPPPPPPPPPPRRRRMMMM     ",
        "  MRRRRPPPPPPPPPPPPPRRRRRMMMRR    ",
        " MRRRRRRPPPPPPPPPPRRRRRRMMMPPRR   ",
        " MRRRRRRRPPPPPRRRRRRRRRMMMPPPRR   ",
        "MMRRRRRRRRRRRRRRRRRRRRMMMPPPPRR   ",
        "MMMRRRRRRRRRRRRRRRRRRMMMPPPPPRR   ",
        "MMMMRRRRRRRRRRRRRRRRMMMPPPPPPRR   ",
        "MMMMMRRRRRRRRRRRRRMMMMMPPPPPPRR   ",
        "MMMMMMMRRRRRRRRMMMMMMMMPPPPPRRR   ",
        " MMMMMMMMMMMMMMMMMMMMMMMMPPRRR    ",
        "  MMMMMMMMMMMMMMMM   MMMMMMM      ",
        "     MMMMMMMMMMMM                 ",
    ])
    ground_assignment = {get_pos(x=x, y=y): ground[y][x] for y in range(len(ground)) for x in range(len(ground[y]))}
    assert set(solution.keys()) == set(ground_assignment.keys()), f'solution keys != ground assignment keys, {set(solution.keys()) ^ set(ground_assignment.keys())} \n\n\n{solution} \n\n\n{ground_assignment}'
    for pos in solution.keys():
        assert solution[pos] == ground_assignment[pos], f'solution[{pos}] != ground_assignment[{pos}], {solution[pos]} != {ground_assignment[pos]}'



if __name__ == '__main__':
    test_toy()
    test_toy2()
    test_ground()
