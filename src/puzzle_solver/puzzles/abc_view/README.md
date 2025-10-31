# ABC View (Puzzle Type #58)

* [**Play online**](https://www.brainbashers.com/showabcview.asp)

Fill every row and column with exactly one A, B, and C (and two blank squares).
The clues tell you which letter appears first in that direction in each row or column.

**Unsolved puzzle**

<img src="https://raw.githubusercontent.com/Ar-Kareem/puzzle_solver/master/images/puzzles/abc_view_unsolved.png" alt="ABC View unsolved" width="500">

Code to utilize this package and solve the puzzle:

```python
import numpy as np
from puzzle_solver import abc_view_solver as solver
board = np.full((5, 5), ' ')
top = np.array(['C', 'C', 'C', 'B', ''])
left = np.array(['C', 'C', '', 'A', ''])
bottom = np.array(['', 'A', 'A', 'C', 'B'])
right = np.array(['', '', 'C', '', ''])
binst = solver.Board(board=board, top=top, left=left, bottom=bottom, right=right, characters=['A', 'B', 'C'])
solutions = binst.solve_and_print()
```

**Script Output**

```python
Solution found

    0   1   2   3   4
  ┌───┬───┬───┬───┬───┐
 0│   │ C │   │ B │ A │
  ├───┼───┼───┼───┼───┤
 1│ C │ B │   │ A │   │
  ├───┼───┼───┼───┼───┤
 2│ B │ A │ C │   │   │
  ├───┼───┼───┼───┼───┤
 3│ A │   │ B │   │ C │
  ├───┼───┼───┼───┼───┤
 4│   │   │ A │ C │ B │
  └───┴───┴───┴───┴───┘
Solutions found: 1
status: OPTIMAL
Time taken: 0.01 seconds
```

**Solved puzzle**

<img src="https://raw.githubusercontent.com/Ar-Kareem/puzzle_solver/master/images/puzzles/abc_view_solved.png" alt="ABC View solved" width="500">
