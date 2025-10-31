# Unruly (Puzzle Type #15)

This is a dedicated solver for Unruly. Also known as "3-In-A-Row".

Below are the details of how to utilize the solver. In addition, the solver gives all possible solutions to the input thus it can be utilized to figure out if a single partial input board has multiple possible solutions.

(The solver under the hood mainly utilizes the CP-SAT solver from Google OR-Tools)

* [**Play online**](https://www.chiark.greenend.org.uk/~sgtatham/puzzles/js/unruly.html)

* [**Instructions**](https://www.chiark.greenend.org.uk/~sgtatham/puzzles/doc/unruly.html#unruly)

You are given a grid of squares, which you must colour either black or white. Some squares are provided as clues; the rest are left for you to fill in. Each row and column must contain the same number of black and white squares, and no row or column may contain three consecutive squares of the same colour. 

**Unsolved puzzle**

<img src="https://raw.githubusercontent.com/Ar-Kareem/puzzle_solver/master/images/puzzles/unruly_unsolved.png" alt="Unruly unsolved" width="500">

Code to utilize this package and solve the puzzle:
```python
import numpy as np
from puzzle_solver import unruly_solver as solver
board = np.array([
  ['W', 'W', ' ', 'B', ' ', ' ', ' ', ' ', 'B', ' ', ' ', ' ', ' ', ' '],
  [' ', ' ', ' ', ' ', ' ', ' ', ' ', 'W', ' ', ' ', ' ', ' ', ' ', 'W'],
  [' ', ' ', ' ', ' ', ' ', 'B', ' ', 'W', ' ', ' ', 'B', ' ', ' ', ' '],
  [' ', ' ', 'W', ' ', ' ', ' ', ' ', ' ', ' ', 'W', ' ', 'W', ' ', ' '],
  ['B', ' ', ' ', 'W', ' ', ' ', ' ', ' ', 'B', ' ', ' ', ' ', ' ', ' '],
  [' ', ' ', ' ', ' ', ' ', 'B', ' ', ' ', ' ', 'B', ' ', 'B', ' ', ' '],
  [' ', 'B', 'B', ' ', ' ', 'B', ' ', ' ', ' ', ' ', ' ', 'B', ' ', ' '],
  [' ', ' ', 'B', ' ', ' ', ' ', ' ', 'W', ' ', 'B', 'B', ' ', ' ', 'W'],
  [' ', ' ', ' ', ' ', ' ', ' ', ' ', 'W', ' ', ' ', ' ', ' ', ' ', 'W'],
  [' ', ' ', ' ', 'B', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
  [' ', ' ', 'W', ' ', ' ', ' ', 'W', ' ', ' ', 'W', ' ', 'W', ' ', ' '],
  [' ', 'W', ' ', 'W', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'B'],
  [' ', ' ', ' ', ' ', 'B', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
  ['W', ' ', ' ', ' ', 'W', ' ', ' ', ' ', 'B', ' ', 'W', ' ', 'B', ' '],
])
binst = solver.Board(board=board)
solutions = binst.solve_and_print()
```
**Script Output**
```
Solution found
    0   0   0   0   0   0   0   0   0   0   1   1   1   1  
    0   1   2   3   4   5   6   7   8   9   0   1   2   3
  ┌───┬───┬───┬───┬───┬───┬───┬───┬───┬───┬───┬───┬───┬───┐
 0│   │   │▒▒▒│▒▒▒│   │▒▒▒│   │▒▒▒│▒▒▒│   │▒▒▒│   │   │▒▒▒│
  ├───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┤
 1│▒▒▒│▒▒▒│   │   │▒▒▒│   │▒▒▒│   │   │▒▒▒│   │▒▒▒│▒▒▒│   │
  ├───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┤
 2│   │   │▒▒▒│   │   │▒▒▒│▒▒▒│   │▒▒▒│   │▒▒▒│▒▒▒│   │▒▒▒│
  ├───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┤
 3│   │▒▒▒│   │▒▒▒│▒▒▒│   │   │▒▒▒│   │   │▒▒▒│   │▒▒▒│▒▒▒│
  ├───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┤
 4│▒▒▒│   │▒▒▒│   │▒▒▒│   │▒▒▒│   │▒▒▒│▒▒▒│   │   │▒▒▒│   │
  ├───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┤
 5│▒▒▒│   │   │▒▒▒│   │▒▒▒│▒▒▒│   │▒▒▒│▒▒▒│   │▒▒▒│   │   │
  ├───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┤
 6│   │▒▒▒│▒▒▒│   │   │▒▒▒│   │▒▒▒│   │   │▒▒▒│▒▒▒│   │▒▒▒│
  ├───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┤
 7│▒▒▒│   │▒▒▒│   │▒▒▒│   │▒▒▒│   │   │▒▒▒│▒▒▒│   │▒▒▒│   │
  ├───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┤
 8│▒▒▒│▒▒▒│   │▒▒▒│▒▒▒│   │▒▒▒│   │▒▒▒│   │   │▒▒▒│   │   │
  ├───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┤
 9│   │   │▒▒▒│▒▒▒│   │▒▒▒│   │▒▒▒│   │▒▒▒│   │   │▒▒▒│▒▒▒│
  ├───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┤
10│▒▒▒│▒▒▒│   │   │▒▒▒│   │   │▒▒▒│▒▒▒│   │▒▒▒│   │▒▒▒│   │
  ├───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┤
11│▒▒▒│   │▒▒▒│   │   │▒▒▒│▒▒▒│   │   │▒▒▒│   │▒▒▒│   │▒▒▒│
  ├───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┤
12│   │▒▒▒│   │▒▒▒│▒▒▒│   │   │▒▒▒│   │▒▒▒│▒▒▒│   │   │▒▒▒│
  ├───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┤
13│   │▒▒▒│   │▒▒▒│   │▒▒▒│   │▒▒▒│▒▒▒│   │   │▒▒▒│▒▒▒│   │
  └───┴───┴───┴───┴───┴───┴───┴───┴───┴───┴───┴───┴───┴───┘
Solutions found: 1
status: OPTIMAL
Time taken: 0.02 seconds
```

**Solved puzzle**

<img src="https://raw.githubusercontent.com/Ar-Kareem/puzzle_solver/master/images/puzzles/unruly_solved.png" alt="Unruly solved" width="500">
