# Mathema Grids (Puzzle Type #59)

* [**Play online**](https://www.brainbashers.com/showmathemagrids.asp)

Complete the grid using all of the numbers from 1 to 9.
When completed, all of the sums must be correct.
The sums are solved strictly from left to right, and top to bottom.
The normal order of mathematical operations is ignored.
For example, 2 + 5 x 9 is calculated as (2 + 5) x 9 = 63.
÷ 1 doesn't appear in the puzzle.
x 1 doesn't appear in the puzzle (although there might be 1 x).
At no point will any calculation go below zero, or become fractional.

**Unsolved puzzle**

<img src="https://raw.githubusercontent.com/Ar-Kareem/puzzle_solver/master/images/puzzles/mathema_grids_unsolved.png" alt="Mathema Grids unsolved" width="500">

Code to utilize this package and solve the puzzle:

```python
import numpy as np
from puzzle_solver import mathema_grids_solver as solver
board = np.array([
    [' ', '+', ' ', '-', ' ', '=', '4'],
    ['+', ' ', '+', ' ', '*', ' ', ' '],
    [' ', '*', ' ', '/', ' ', '=', '3'],
    ['*', ' ', '*', ' ', '+', ' ', ' '],
    [' ', '*', '2', '-', ' ', '=', '2'],
    ['=', ' ', '=', ' ', '=', ' ', ' '],
    ['24', ' ', '32', ' ', '30', ' ', ' '],
])
binst = solver.Board(board=board, digits=[1, 2, 3, 4, 5, 6, 7, 8, 9])
solutions = binst.solve_and_print()
```

**Script Output**

```python
Solution found

    0   1   2   3   4   5   6
  ┌───┬───┬───┬───┬───┬───┬───┐
 0│ 5 │ + │ 7 │ - │ 8 │ = │ 4 │
  ├───┼───┼───┼───┼───┼───┼───┤
 1│ + │   │ + │   │ * │   │   │
  ├───┼───┼───┼───┼───┼───┼───┤
 2│ 1 │ * │ 9 │ / │ 3 │ = │ 3 │
  ├───┼───┼───┼───┼───┼───┼───┤
 3│ * │   │ * │   │ + │   │   │
  ├───┼───┼───┼───┼───┼───┼───┤
 4│ 4 │ * │ 2 │ - │ 6 │ = │ 2 │
  ├───┼───┼───┼───┼───┼───┼───┤
 5│ = │   │ = │   │ = │   │   │
  ├───┼───┼───┼───┼───┼───┼───┤
 6│24 │   │32 │   │30 │   │   │
  └───┴───┴───┴───┴───┴───┴───┘
Solutions found: 1
status: OPTIMAL
Time taken: 0.00 seconds
```

**Solved puzzle**

<img src="https://raw.githubusercontent.com/Ar-Kareem/puzzle_solver/master/images/puzzles/mathema_grids_solved.png" alt="Mathema Grids solved" width="500">
