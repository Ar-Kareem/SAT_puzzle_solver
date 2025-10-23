# Yin-Yang (Puzzle Type #40)

* [**Play online**](https://www.puzzle-yin-yang.com)

Yin-Yang is played on a rectangular grid with no standard size. Some cells start out filled with black or white. The rest of the cells are empty. The goal is to color all cells in such a way that:
1. All black cells should be connected orthogonally in a single group.
2. All white cells should be connected orthogonally in a single group.
3. 2x2 areas of the same color are not allowed.

**Unsolved puzzle**

<img src="https://raw.githubusercontent.com/Ar-Kareem/puzzle_solver/master/images/yin_yang_unsolved.png" alt="Yin-Yang unsolved" width="500">

Code to utilize this package and solve the puzzle:

```python
import numpy as np
from puzzle_solver import yin_yang_solver as solver
board = np.array([
  [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
  [' ', ' ', ' ', ' ', ' ', 'W', ' ', ' ', ' ', 'B', ' ', ' ', 'W', ' ', 'W', ' ', ' ', 'W', ' ', ' '],
  [' ', ' ', 'B', ' ', 'B', ' ', 'W', ' ', ' ', 'W', 'B', ' ', ' ', ' ', ' ', 'W', ' ', 'W', ' ', ' '],
  [' ', ' ', ' ', ' ', ' ', 'W', ' ', 'W', ' ', 'B', ' ', ' ', ' ', ' ', 'W', ' ', ' ', 'W', ' ', ' '],
  [' ', 'W', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'W', 'W', ' ', ' ', ' ', ' ', ' ', ' ', 'W', ' ', ' '],
  [' ', ' ', ' ', ' ', 'W', ' ', ' ', ' ', 'W', 'B', ' ', ' ', ' ', ' ', ' ', 'W', ' ', 'W', ' ', ' '],
  [' ', ' ', ' ', ' ', ' ', 'W', ' ', ' ', ' ', ' ', 'B', ' ', 'B', ' ', 'B', 'W', ' ', 'W', ' ', ' '],
  [' ', ' ', 'B', 'W', 'W', ' ', 'W', ' ', ' ', ' ', 'B', ' ', 'B', ' ', 'B', ' ', ' ', ' ', ' ', ' '],
  [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'B', ' ', 'B', ' ', 'B', ' ', 'B', ' ', 'B', ' ', 'B', ' '],
  [' ', 'W', ' ', 'W', ' ', ' ', 'W', ' ', ' ', ' ', 'B', ' ', 'B', ' ', 'B', ' ', 'B', ' ', 'B', ' '],
  [' ', ' ', ' ', ' ', 'W', 'B', ' ', ' ', ' ', 'B', ' ', ' ', 'B', ' ', 'B', ' ', 'B', ' ', 'B', ' '],
  [' ', ' ', 'B', ' ', ' ', ' ', 'B', 'B', ' ', 'W', 'B', ' ', 'B', ' ', 'B', ' ', ' ', 'B', ' ', ' '],
  [' ', 'W', 'W', 'W', ' ', 'B', ' ', 'W', ' ', ' ', 'B', ' ', 'B', ' ', 'B', ' ', ' ', ' ', 'B', ' '],
  [' ', ' ', ' ', ' ', ' ', ' ', 'W', ' ', ' ', 'B', ' ', 'B', ' ', ' ', 'B', ' ', 'B', ' ', 'B', ' '],
  [' ', 'W', ' ', 'B', 'W', 'B', ' ', 'W', ' ', ' ', ' ', ' ', 'B', 'B', ' ', ' ', 'B', ' ', 'B', ' '],
  [' ', ' ', ' ', ' ', 'W', ' ', ' ', 'B', 'B', 'B', 'B', 'B', ' ', ' ', ' ', 'B', ' ', ' ', 'B', ' '],
  [' ', 'W', ' ', ' ', ' ', 'W', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'B', ' ', 'B', ' '],
  ['W', ' ', ' ', 'W', ' ', ' ', 'B', ' ', ' ', 'B', 'B', 'B', 'B', 'B', ' ', ' ', 'B', ' ', 'B', ' '],
  [' ', 'W', 'W', ' ', 'W', ' ', ' ', 'B', ' ', ' ', ' ', ' ', ' ', ' ', 'B', ' ', 'B', ' ', 'B', ' '],
  ['B', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'B', 'W']
])
binst = solver.Board(board=board)
solutions = binst.solve_and_print()
```

**Script Output**

```python
Solution found
[
    [ 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W' ],
    [ 'W', 'B', 'B', 'W', 'B', 'W', 'B', 'B', 'B', 'B', 'B', 'B', 'W', 'B', 'W', 'B', 'B', 'W', 'B', 'W' ],
    [ 'W', 'W', 'B', 'W', 'B', 'W', 'W', 'W', 'W', 'W', 'B', 'W', 'W', 'B', 'W', 'W', 'B', 'W', 'B', 'W' ],
    [ 'W', 'B', 'B', 'B', 'B', 'W', 'B', 'W', 'B', 'B', 'B', 'B', 'B', 'B', 'W', 'B', 'B', 'W', 'B', 'W' ],
    [ 'W', 'W', 'W', 'B', 'W', 'W', 'B', 'W', 'W', 'W', 'W', 'W', 'B', 'W', 'W', 'W', 'B', 'W', 'B', 'W' ],
    [ 'W', 'B', 'W', 'B', 'W', 'B', 'B', 'B', 'W', 'B', 'B', 'W', 'B', 'W', 'B', 'W', 'B', 'W', 'B', 'W' ],
    [ 'W', 'B', 'B', 'B', 'W', 'W', 'W', 'B', 'W', 'W', 'B', 'W', 'B', 'W', 'B', 'W', 'B', 'W', 'B', 'W' ],
    [ 'W', 'W', 'B', 'W', 'W', 'B', 'W', 'B', 'B', 'W', 'B', 'W', 'B', 'W', 'B', 'W', 'B', 'W', 'B', 'W' ],
    [ 'W', 'B', 'B', 'B', 'B', 'B', 'W', 'W', 'B', 'W', 'B', 'W', 'B', 'W', 'B', 'W', 'B', 'W', 'B', 'W' ],
    [ 'W', 'W', 'W', 'W', 'W', 'B', 'W', 'B', 'B', 'W', 'B', 'W', 'B', 'W', 'B', 'W', 'B', 'W', 'B', 'W' ],
    [ 'W', 'B', 'W', 'B', 'W', 'B', 'W', 'W', 'B', 'B', 'B', 'W', 'B', 'W', 'B', 'W', 'B', 'W', 'B', 'W' ],
    [ 'W', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'W', 'B', 'W', 'B', 'W', 'B', 'W', 'B', 'B', 'B', 'W' ],
    [ 'W', 'W', 'W', 'W', 'W', 'B', 'W', 'W', 'W', 'W', 'B', 'W', 'B', 'W', 'B', 'W', 'W', 'W', 'B', 'W' ],
    [ 'W', 'B', 'B', 'B', 'B', 'B', 'W', 'B', 'B', 'B', 'B', 'B', 'B', 'W', 'B', 'W', 'B', 'W', 'B', 'W' ],
    [ 'W', 'W', 'W', 'B', 'W', 'B', 'W', 'W', 'W', 'W', 'W', 'W', 'B', 'B', 'B', 'W', 'B', 'W', 'B', 'W' ],
    [ 'W', 'B', 'B', 'B', 'W', 'B', 'W', 'B', 'B', 'B', 'B', 'B', 'B', 'W', 'B', 'B', 'B', 'W', 'B', 'W' ],
    [ 'W', 'W', 'B', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'B', 'W', 'B', 'W' ],
    [ 'W', 'B', 'B', 'W', 'B', 'B', 'B', 'B', 'W', 'B', 'B', 'B', 'B', 'B', 'B', 'W', 'B', 'W', 'B', 'W' ],
    [ 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'B', 'W', 'W', 'W', 'W', 'W', 'W', 'B', 'W', 'B', 'W', 'B', 'W' ],
    [ 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'W' ],
]
Solutions found: 1
status: OPTIMAL
Time taken: 3.10 seconds
```

**Solved puzzle**

Applying the solution to the puzzle visually:

<img src="https://raw.githubusercontent.com/Ar-Kareem/puzzle_solver/master/images/yin_yang_solved.png" alt="Yin-Yang solved" width="500">
