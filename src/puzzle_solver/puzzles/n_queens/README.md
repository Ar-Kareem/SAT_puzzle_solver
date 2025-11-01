# N-Queens (Puzzle Type #60)

Can also solve puzzles such as 7-Queens.

* [**Play online**](https://krazydad.com/play/queens/)

7-Queens Variant: Within each of the seven realms lives a lone queen. To maintain the peace, queens must not threaten each other: no row, column, diagonal, nor region may have more than one queen!

**Unsolved puzzle**

<img src="https://raw.githubusercontent.com/Ar-Kareem/puzzle_solver/master/images/puzzles/7_queens_unsolved.png" alt="7 Queens unsolved" width="500">

Code to utilize this package and solve the puzzle:

```python
import numpy as np
from puzzle_solver import n_queens_solver as solver
board = np.array([
  ['00', '00', '00', '00', '01', '01', '02', '02'],
  ['00', '00', '03', '03', '01', '01', '02', '04'],
  ['00', '00', '03', '03', '01', '01', '01', '04'],
  ['03', '03', '03', '03', '01', '01', '01', '05'],
  ['03', '03', '03', '03', '01', '01', '01', '05'],
  ['03', '03', '06', '06', '06', '05', '05', '05'],
  ['06', '06', '06', '06', '06', '06', '05', '05'],
  ['06', '06', '06', '06', '06', '06', '05', '05']
])
binst = solver.Board(board=board)
solutions = binst.solve_and_print()
```

**Script Output**

```python
Solution found

    0   1   2   3   4   5   6   7
  ┌───┬───┬───┬───┬───┬───┬───┬───┐
 0│   │   │   │   │   │   │▒▒▒│   │
  ├───┼───┼───┼───┼───┼───┼───┼───┤
 1│▒▒▒│   │   │   │   │   │   │   │
  ├───┼───┼───┼───┼───┼───┼───┼───┤
 2│   │   │   │   │   │   │   │▒▒▒│
  ├───┼───┼───┼───┼───┼───┼───┼───┤
 3│   │   │   │   │▒▒▒│   │   │   │
  ├───┼───┼───┼───┼───┼───┼───┼───┤
 4│   │▒▒▒│   │   │   │   │   │   │
  ├───┼───┼───┼───┼───┼───┼───┼───┤
 5│   │   │   │   │   │▒▒▒│   │   │
  ├───┼───┼───┼───┼───┼───┼───┼───┤
 6│   │   │▒▒▒│   │   │   │   │   │
  ├───┼───┼───┼───┼───┼───┼───┼───┤
 7│   │   │   │   │   │   │   │   │
  └───┴───┴───┴───┴───┴───┴───┴───┘
Solutions found: 1
status: OPTIMAL
Time taken: 0.00 seconds
```

**Solved puzzle**

<img src="https://raw.githubusercontent.com/Ar-Kareem/puzzle_solver/master/images/puzzles/7_queens_solved.png" alt="7 Queens solved" width="500">
