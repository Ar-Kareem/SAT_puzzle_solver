# Nonograms (Puzzle Type #1)

This is a dedicated solver for Nonograms. Also known as Hanjie, Paint by Numbers, Griddlers, Pic-a-Pix, Picross, and Pattern

Below are the details of how to utilize the solver. In addition, the solver gives all possible solutions to the input thus it can be utilized to figure out if a single partial input board has multiple possible solutions.

(The solver under the hood mainly utilizes the CP-SAT solver from Google OR-Tools)

* [**Play online**](https://www.chiark.greenend.org.uk/~sgtatham/puzzles/js/pattern.html)

* [**Instructions**](https://www.chiark.greenend.org.uk/~sgtatham/puzzles/doc/pattern.html#pattern)

You have a grid of squares, which must all be filled in either black or white. Beside each row of the grid are listed, in order, the lengths of the runs of black squares on that row; above each column are listed, in order, the lengths of the runs of black squares in that column. Your aim is to fill in the entire grid black or white. 

**Unsolved puzzle**

<img src="https://raw.githubusercontent.com/Ar-Kareem/puzzle_solver/master/images/nonogram_unsolved.png" alt="Nonogram unsolved" width="500">

Code to utilize this package and solve the puzzle:
```python
from puzzle_solver import nonograms_solver as solver
top_numbers = [
  [8, 2],
  [5, 4],
  [2, 1, 4],
  [2, 4],
  [2, 1, 4],
  [2, 5],
  [2, 8],
  [3, 2],
  [1, 6],
  [1, 9],
  [1, 6, 1],
  [1, 5, 3],
  [3, 2, 1],
  [4, 2],
  [1, 5],
]
side_numbers = [
  [7, 3],
  [7, 1, 1],
  [2, 3],
  [2, 3],
  [3, 2],
  [1, 1, 1, 1, 2],
  [1, 6, 1],
  [1, 9],
  [9],
  [2, 4],
  [8],
  [11],
  [7, 1, 1],
  [4, 3],
  [3, 2],
]
binst = solver.Board(top=top_numbers, side=side_numbers)
solutions = binst.solve_and_print()
```
**Script Output**
```
Solution found
    0   0   0   0   0   0   0   0   0   0   1   1   1   1   1  
    0   1   2   3   4   5   6   7   8   9   0   1   2   3   4
  ┌───┬───┬───┬───┬───┬───┬───┬───┬───┬───┬───┬───┬───┬───┬───┐
 0│▒▒▒│▒▒▒│▒▒▒│▒▒▒│▒▒▒│▒▒▒│▒▒▒│   │▒▒▒│▒▒▒│▒▒▒│   │   │   │   │
  ├───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┤
 1│▒▒▒│▒▒▒│▒▒▒│▒▒▒│▒▒▒│▒▒▒│▒▒▒│   │   │   │   │   │▒▒▒│   │▒▒▒│
  ├───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┤
 2│▒▒▒│▒▒▒│   │   │   │   │   │   │   │   │   │▒▒▒│▒▒▒│▒▒▒│   │
  ├───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┤
 3│▒▒▒│▒▒▒│   │   │   │   │   │   │   │   │   │   │▒▒▒│▒▒▒│▒▒▒│
  ├───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┤
 4│▒▒▒│▒▒▒│▒▒▒│   │   │   │   │   │   │   │   │   │   │▒▒▒│▒▒▒│
  ├───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┤
 5│▒▒▒│   │   │   │▒▒▒│   │▒▒▒│   │   │▒▒▒│   │   │   │▒▒▒│▒▒▒│
  ├───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┤
 6│▒▒▒│   │   │   │   │   │▒▒▒│▒▒▒│▒▒▒│▒▒▒│▒▒▒│▒▒▒│   │   │▒▒▒│
  ├───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┤
 7│▒▒▒│   │   │   │   │   │▒▒▒│▒▒▒│▒▒▒│▒▒▒│▒▒▒│▒▒▒│▒▒▒│▒▒▒│▒▒▒│
  ├───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┤
 8│   │   │   │   │   │▒▒▒│▒▒▒│▒▒▒│▒▒▒│▒▒▒│▒▒▒│▒▒▒│▒▒▒│▒▒▒│   │
  ├───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┤
 9│   │   │   │   │   │▒▒▒│▒▒▒│   │▒▒▒│▒▒▒│▒▒▒│▒▒▒│   │   │   │
  ├───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┤
10│   │   │   │   │▒▒▒│▒▒▒│▒▒▒│▒▒▒│▒▒▒│▒▒▒│▒▒▒│▒▒▒│   │   │   │
  ├───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┤
11│▒▒▒│▒▒▒│▒▒▒│▒▒▒│▒▒▒│▒▒▒│▒▒▒│▒▒▒│▒▒▒│▒▒▒│▒▒▒│   │   │   │   │
  ├───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┤
12│▒▒▒│▒▒▒│▒▒▒│▒▒▒│▒▒▒│▒▒▒│▒▒▒│   │   │▒▒▒│   │▒▒▒│   │   │   │
  ├───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┤
13│   │▒▒▒│▒▒▒│▒▒▒│▒▒▒│   │   │   │   │▒▒▒│▒▒▒│▒▒▒│   │   │   │
  ├───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┤
14│   │▒▒▒│▒▒▒│▒▒▒│   │   │   │   │   │   │   │▒▒▒│▒▒▒│   │   │
  └───┴───┴───┴───┴───┴───┴───┴───┴───┴───┴───┴───┴───┴───┴───┘
Solutions found: 1
status: OPTIMAL
Time taken: 0.04 seconds
```

**Solved puzzle**

<img src="https://raw.githubusercontent.com/Ar-Kareem/puzzle_solver/master/images/nonogram_solved.png" alt="Nonogram solved" width="500">


# Nonograms Colored (Puzzle Type #57)

* [**Play online**](https://www.nonograms.org/nonograms2)


You have a grid of squares, which must all be filled in either white or one of the specified colors. Beside each row of the grid are listed, in order, the lengths of the runs of the specified colors on that row; above each column are listed, in order, the lengths of the runs of the specified colors in that column. Your aim is to fill in the entire grid white or one of the specified colors. 

**Unsolved puzzle**

<img src="https://raw.githubusercontent.com/Ar-Kareem/puzzle_solver/master/images/nonograms_colored_unsolved.png" alt="Nonograms Colored unsolved" width="500">

Code to utilize this package and solve the puzzle:

```python
import numpy as np
from puzzle_solver.puzzles.nonograms import nonograms_colored as solver
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
solutions = binst.solve_and_print(visualize_colors={
    'M': 'darkmagenta',
    'R': 'magenta',
    'G': 'green',
    'P': 'pink',
    'L': 'lime',
    'F': 'forestgreen',
})
```

**Script Output**

```python
Solution found
[
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
    ]
Solutions found: 1
status: OPTIMAL
Time taken: 36.95 seconds
```

The script also visualizes the solution:

<img src="https://raw.githubusercontent.com/Ar-Kareem/puzzle_solver/master/images/nonograms_colored_script_output.png" alt="Nonograms Colored solved" width="500">

**Solved puzzle**

<img src="https://raw.githubusercontent.com/Ar-Kareem/puzzle_solver/master/images/nonograms_colored_solved.png" alt="Nonograms Colored solved" width="500">
