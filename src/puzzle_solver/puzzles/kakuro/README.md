# Kakuro (Puzzle Type #51)

* [**Play online**](https://www.puzzle-kakuro.com/)

Kakuro is played on a rectangular grid by placing numbers in the white cells such that:
   1. Each white cell should contain a number from 1 through 9
   2. The clues in the black cells tells the sum of the numbers in the consecutive white cells next to that clue. (on the right or down)
   3. The numbers in consecutive white cells must be unique.

**Unsolved puzzle**

<img src="https://raw.githubusercontent.com/Ar-Kareem/puzzle_solver/master/images/kakuro_unsolved.png" alt="Kakuro unsolved" width="500">

Code to utilize this package and solve the puzzle:

```python
import numpy as np
from puzzle_solver import kakuro_solver as solver
board = np.array([
    ['#', '#', ' ', ' ', '#', ' ', ' ', '#', ' ', ' '],
    [' ', ' ', ' ', ' ', '#', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', '#', ' ', ' ', '#', ' ', ' ', '#'],
    ['#', '#', ' ', ' ', ' ', '#', '#', ' ', ' ', '#'],
    [' ', ' ', '#', ' ', ' ', ' ', ' ', '#', ' ', ' '],
    [' ', ' ', '#', ' ', ' ', ' ', ' ', '#', ' ', ' '],
    ['#', ' ', ' ', '#', '#', ' ', ' ', ' ', '#', '#'],
    ['#', ' ', ' ', '#', ' ', ' ', '#', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', '#', ' ', ' ', ' ', ' '],
    [' ', ' ', '#', ' ', ' ', '#', ' ', ' ', '#', '#'],
])
row_sums = [[7, 16, 12, ], [28, 23, ], [22, 16, 9, ], [18, 15, ], [12, 11, 16, ], [9, 24, 8, ], [7, 9, ], [14, 7, 20, ], [23, 30, ], [11, 3, 4, ]]
col_sums = [[14, 12, 8, ], [15, 21, ], [29, 23, ], [8, 10, 11, ], [24, 8, ], [21, 13, ], [17, 12, 11, ], [21, 15, ], [29, 17, ], [4, 16, 15]]
binst = solver.Board(board=board, row_sums=row_sums, col_sums=col_sums)
solutions = binst.solve_and_print()
```

**Script Output**

```python
Solution found
    0   0   0   0   0   0   0   0   0   0
    0   1   2   3   4   5   6   7   8   9
  ┌───┬───┬───┬───┬───┬───┬───┬───┬───┬───┐
 0│▒▒▒│▒▒▒│ 5 │ 2 │▒▒▒│ 7 │ 9 │▒▒▒│ 9 │ 3 │
  ├───┼───┼───┼───┼───┼───┼───┼───┼───┼───┤
 1│ 5 │ 9 │ 8 │ 6 │▒▒▒│ 5 │ 8 │ 7 │ 2 │ 1 │
  ├───┼───┼───┼───┼───┼───┼───┼───┼───┼───┤
 2│ 9 │ 6 │ 7 │▒▒▒│ 7 │ 9 │▒▒▒│ 5 │ 4 │▒▒▒│
  ├───┼───┼───┼───┼───┼───┼───┼───┼───┼───┤
 3│▒▒▒│▒▒▒│ 9 │ 3 │ 6 │▒▒▒│▒▒▒│ 9 │ 6 │▒▒▒│
  ├───┼───┼───┼───┼───┼───┼───┼───┼───┼───┤
 4│ 9 │ 3 │▒▒▒│ 2 │ 3 │ 1 │ 5 │▒▒▒│ 7 │ 9 │
  ├───┼───┼───┼───┼───┼───┼───┼───┼───┼───┤
 5│ 3 │ 6 │▒▒▒│ 5 │ 8 │ 7 │ 4 │▒▒▒│ 1 │ 7 │
  ├───┼───┼───┼───┼───┼───┼───┼───┼───┼───┤
 6│▒▒▒│ 1 │ 6 │▒▒▒│▒▒▒│ 2 │ 3 │ 4 │▒▒▒│▒▒▒│
  ├───┼───┼───┼───┼───┼───┼───┼───┼───┼───┤
 7│▒▒▒│ 5 │ 9 │▒▒▒│ 4 │ 3 │▒▒▒│ 3 │ 8 │ 9 │
  ├───┼───┼───┼───┼───┼───┼───┼───┼───┼───┤
 8│ 1 │ 2 │ 8 │ 9 │ 3 │▒▒▒│ 8 │ 7 │ 9 │ 6 │
  ├───┼───┼───┼───┼───┼───┼───┼───┼───┼───┤
 9│ 7 │ 4 │▒▒▒│ 2 │ 1 │▒▒▒│ 3 │ 1 │▒▒▒│▒▒▒│
  └───┴───┴───┴───┴───┴───┴───┴───┴───┴───┘
Solutions found: 1
status: OPTIMAL
Time taken: 0.00 seconds
```

**Solved puzzle**

<img src="https://raw.githubusercontent.com/Ar-Kareem/puzzle_solver/master/images/kakuro_solved.png" alt="Kakuro solved" width="500">
