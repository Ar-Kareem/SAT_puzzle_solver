# Tents (Puzzle Type #6)

This is a dedicated solver for Tents

Below are the details of how to utilize the solver. In addition, the solver gives all possible solutions to the input thus it can be utilized to figure out if a single partial input board has multiple possible solutions.

(The solver under the hood mainly utilizes the CP-SAT solver from Google OR-Tools)

* [**Play online**](https://www.chiark.greenend.org.uk/~sgtatham/puzzles/js/tents.html)

* [**Instructions**](https://www.chiark.greenend.org.uk/~sgtatham/puzzles/doc/tents.html#tents)

You have a grid of squares, some of which contain trees. Your aim is to place tents in some of the remaining squares, in such a way that the following conditions are met:

  - There are exactly as many tents as trees.
  - The tents and trees can be matched up in such a way that each tent is directly adjacent (horizontally or vertically, but not diagonally) to its own tree. However, a tent may be adjacent to other trees as well as its own.
  - No two tents are adjacent horizontally, vertically or diagonally.
  - The number of tents in each row, and in each column, matches the numbers given round the sides of the grid.

**Unsolved puzzle**

<img src="https://raw.githubusercontent.com/Ar-Kareem/puzzle_solver/master/images/puzzles/tents_unsolved.png" alt="Tents unsolved" width="500">

Code to utilize this package and solve the puzzle:
```python
import numpy as np
from puzzle_solver import tents_solver as solver
board = np.array([
  [' ', 'T', ' ', ' ', ' ', ' ', ' ', ' ', 'T', ' ', 'T', ' ', 'T', ' ', ' '],
  [' ', ' ', ' ', ' ', 'T', ' ', ' ', 'T', ' ', 'T', ' ', ' ', 'T', ' ', ' '],
  [' ', 'T', ' ', 'T', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
  [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'T', ' ', ' ', ' ', 'T', ' ', 'T'],
  [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
  [' ', 'T', ' ', ' ', 'T', ' ', 'T', ' ', ' ', 'T', ' ', ' ', 'T', 'T', ' '],
  [' ', 'T', ' ', ' ', 'T', ' ', ' ', ' ', 'T', ' ', ' ', ' ', ' ', ' ', ' '],
  [' ', ' ', ' ', ' ', ' ', ' ', 'T', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
  [' ', ' ', ' ', ' ', ' ', 'T', ' ', ' ', ' ', ' ', 'T', ' ', ' ', 'T', ' '],
  [' ', ' ', ' ', 'T', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'T', ' ', 'T'],
  ['T', ' ', ' ', ' ', ' ', ' ', ' ', 'T', ' ', ' ', ' ', 'T', ' ', ' ', ' '],
  ['T', ' ', ' ', ' ', 'T', ' ', 'T', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
  [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'T', ' ', 'T', ' ', ' ', ' ', 'T'],
  [' ', 'T', ' ', ' ', ' ', 'T', ' ', ' ', ' ', ' ', ' ', ' ', 'T', ' ', ' '],
  [' ', 'T', ' ', ' ', 'T', ' ', ' ', ' ', ' ', 'T', ' ', 'T', ' ', ' ', ' '],
])
side = np.array([4, 1, 6, 0, 5, 2, 3, 1, 5, 2, 3, 2, 4, 3, 4])
top = np.array([4, 2, 4, 1, 3, 3, 3, 3, 3, 3, 2, 2, 6, 2, 4])

binst = solver.Board(board=board, sides={'top': top, 'side': side})
solutions = binst.solve_and_print()
```
**Script Output**

(Note: ▲ represents a tent)

```
Solution found
    0   0   0   0   0   0   0   0   0   0   1   1   1   1   1  
    0   1   2   3   4   5   6   7   8   9   0   1   2   3   4
  ┌───┬───┬───┬───┬───┬───┬───┬───┬───┬───┬───┬───┬───┬───┬───┐
 0│   │ | │ ▲ │   │   │   │   │ ▲ │ | │   │ | │ ▲ │ | │ ▲ │   │
  ├───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┤
 1│   │   │   │   │ | │ ▲ │   │ | │   │ | │   │   │ | │   │   │
  ├───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┤
 2│ ▲ │ | │ ▲ │ | │   │   │   │ ▲ │   │ ▲ │   │   │ ▲ │   │ ▲ │
  ├───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┤
 3│   │   │   │   │   │   │   │   │ | │   │   │   │ | │   │ | │
  ├───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┤
 4│   │ ▲ │   │   │ ▲ │   │ ▲ │   │ ▲ │   │   │   │ ▲ │   │   │
  ├───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┤
 5│   │ | │   │   │ | │   │ | │   │   │ | │ ▲ │   │ | │ | │ ▲ │
  ├───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┤
 6│   │ | │   │   │ | │ ▲ │   │ ▲ │ | │   │   │   │ ▲ │   │   │
  ├───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┤
 7│   │ ▲ │   │   │   │   │ | │   │   │   │   │   │   │   │   │
  ├───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┤
 8│   │   │   │   │ ▲ │ | │ ▲ │   │   │ ▲ │ | │   │ ▲ │ | │ ▲ │
  ├───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┤
 9│ ▲ │   │ ▲ │ | │   │   │   │   │   │   │   │   │ | │   │ | │
  ├───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┤
10│ | │   │   │   │   │   │   │ | │ ▲ │   │   │ | │ ▲ │   │ ▲ │
  ├───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┤
11│ | │   │   │ ▲ │ | │ ▲ │ | │   │   │   │   │   │   │   │   │
  ├───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┤
12│ ▲ │   │   │   │   │   │   │   │ | │ ▲ │ | │ ▲ │   │ ▲ │ | │
  ├───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┤
13│   │ | │ ▲ │   │ ▲ │ | │ ▲ │   │   │   │   │   │ | │   │   │
  ├───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┤
14│ ▲ │ | │   │   │ | │   │   │   │ ▲ │ | │ ▲ │ | │ ▲ │   │   │
  └───┴───┴───┴───┴───┴───┴───┴───┴───┴───┴───┴───┴───┴───┴───┘
Solutions found: 1
status: OPTIMAL
Time taken: 0.01 seconds
```

**Solved puzzle**

<img src="https://raw.githubusercontent.com/Ar-Kareem/puzzle_solver/master/images/puzzles/tents_solved.png" alt="Tents solved" width="500">
