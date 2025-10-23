# Binairo (Puzzle Type #41)

* [**Play online**](https://www.puzzle-binairo.com)

Binairo is played on a rectangular grid with no standard size. Some cells start out filled with black or white circles. The rest of the cells are empty. The goal is to place circles in all cells in such a way that:

1. Each row and each column must contain an equal number of white and black circles.
2. More than two circles of the same color can't be adjacent.
3. Each row and column is unique. 

**Unsolved puzzle**

<img src="https://raw.githubusercontent.com/Ar-Kareem/puzzle_solver/master/images/binairo_unsolved.png" alt="Binairo unsolved" width="500">

Code to utilize this package and solve the puzzle:

```python
import numpy as np
from puzzle_solver import binairo_solver as solver
board = np.array([
    [' ', ' ', ' ', ' ', 'W', ' ', ' ', ' ', 'W', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'B', ' ', ' ', 'W'],
    [' ', 'W', ' ', ' ', 'B', ' ', ' ', ' ', ' ', ' ', ' ', 'W', ' ', ' ', 'B', ' ', ' ', ' ', 'B', ' '],
    [' ', 'W', ' ', ' ', ' ', 'W', ' ', 'W', 'W', ' ', ' ', ' ', 'B', ' ', ' ', 'W', ' ', ' ', ' ', ' '],
    ['B', ' ', ' ', 'W', ' ', ' ', 'B', ' ', ' ', ' ', ' ', ' ', 'B', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    ['B', ' ', ' ', ' ', 'W', ' ', ' ', ' ', ' ', 'B', ' ', 'W', ' ', ' ', ' ', 'B', ' ', ' ', ' ', 'W'],
    [' ', ' ', 'W', ' ', ' ', 'W', ' ', ' ', ' ', ' ', 'W', ' ', ' ', ' ', ' ', ' ', ' ', 'W', ' ', ' '],
    ['W', ' ', ' ', ' ', ' ', ' ', 'B', ' ', ' ', 'B', ' ', ' ', 'B', 'B', ' ', ' ', 'W', ' ', 'B', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'B', ' ', ' ', ' ', ' ', ' ', 'W', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', 'W', ' ', 'B', ' ', 'W', ' ', ' ', ' ', 'B', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', 'W', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'W', ' ', ' ', ' ', 'W', 'W', ' ', ' ', ' '],
    [' ', ' ', 'B', ' ', ' ', ' ', 'B', ' ', 'B', ' ', ' ', ' ', 'B', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', 'W', 'B', ' ', 'W', ' ', 'B', ' ', ' ', ' ', ' ', ' ', 'W', 'W', ' ', 'B', ' ', ' ', 'B', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'B', ' ', ' ', ' ', 'B', 'B'],
    [' ', 'B', ' ', ' ', ' ', ' ', 'W', ' ', 'W', 'W', ' ', ' ', 'W', ' ', ' ', ' ', 'W', ' ', ' ', ' '],
    [' ', ' ', 'W', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'W', 'W', ' ', ' ', 'W', 'W', ' '],
    [' ', 'B', ' ', 'B', 'W', ' ', ' ', ' ', ' ', ' ', ' ', 'B', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', 'B', ' ', ' ', ' ', 'W', ' ', ' ', ' ', 'W', ' ', ' ', 'B', ' ', 'B', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'B', ' ', ' ', ' ', ' ', ' ', ' ', 'W', ' ', ' ', ' ', 'W'],
    [' ', ' ', ' ', 'B', 'B', ' ', ' ', 'W', ' ', 'W', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'B', ' ', ' '],
    ['B', ' ', 'B', 'B', ' ', ' ', ' ', ' ', ' ', 'W', ' ', 'B', ' ', ' ', 'B', ' ', ' ', ' ', ' ', ' ']
])
binst = solver.Board(board=board)
solutions = binst.solve_and_print()
```

**Script Output**

```python
Solution found
[
    [ 'B', 'B', 'W', 'B', 'W', 'B', 'W', 'B', 'W', 'W', 'B', 'W', 'W', 'B', 'W', 'B', 'B', 'W', 'B', 'W' ],
    [ 'W', 'W', 'B', 'W', 'B', 'B', 'W', 'B', 'B', 'W', 'B', 'W', 'W', 'B', 'B', 'W', 'W', 'B', 'B', 'W' ],
    [ 'W', 'W', 'B', 'B', 'W', 'W', 'B', 'W', 'W', 'B', 'W', 'B', 'B', 'W', 'B', 'W', 'B', 'B', 'W', 'B' ],
    [ 'B', 'B', 'W', 'W', 'B', 'W', 'B', 'W', 'B', 'W', 'W', 'B', 'B', 'W', 'W', 'B', 'W', 'W', 'B', 'B' ],
    [ 'B', 'W', 'B', 'W', 'W', 'B', 'W', 'B', 'W', 'B', 'B', 'W', 'W', 'B', 'W', 'B', 'W', 'B', 'B', 'W' ],
    [ 'W', 'B', 'W', 'B', 'B', 'W', 'W', 'B', 'B', 'W', 'W', 'B', 'B', 'W', 'B', 'W', 'B', 'W', 'W', 'B' ],
    [ 'W', 'B', 'W', 'W', 'B', 'W', 'B', 'W', 'W', 'B', 'B', 'W', 'B', 'B', 'W', 'B', 'W', 'B', 'B', 'W' ],
    [ 'B', 'W', 'B', 'W', 'W', 'B', 'W', 'B', 'B', 'W', 'B', 'B', 'W', 'W', 'B', 'W', 'W', 'B', 'W', 'B' ],
    [ 'W', 'B', 'W', 'B', 'W', 'B', 'B', 'W', 'W', 'B', 'W', 'B', 'B', 'W', 'W', 'B', 'B', 'W', 'B', 'W' ],
    [ 'B', 'W', 'W', 'B', 'B', 'W', 'W', 'B', 'W', 'B', 'B', 'W', 'W', 'B', 'B', 'W', 'W', 'B', 'W', 'B' ],
    [ 'W', 'B', 'B', 'W', 'B', 'W', 'B', 'W', 'B', 'W', 'B', 'W', 'B', 'B', 'W', 'W', 'B', 'B', 'W', 'W' ],
    [ 'B', 'W', 'B', 'W', 'W', 'B', 'B', 'W', 'B', 'B', 'W', 'B', 'W', 'W', 'B', 'B', 'W', 'W', 'B', 'W' ],
    [ 'B', 'W', 'W', 'B', 'B', 'W', 'W', 'B', 'W', 'B', 'W', 'W', 'B', 'W', 'B', 'W', 'B', 'W', 'B', 'B' ],
    [ 'W', 'B', 'B', 'W', 'B', 'B', 'W', 'B', 'W', 'W', 'B', 'B', 'W', 'B', 'W', 'B', 'W', 'B', 'W', 'W' ],
    [ 'B', 'W', 'W', 'B', 'W', 'B', 'B', 'W', 'B', 'B', 'W', 'W', 'B', 'W', 'W', 'B', 'B', 'W', 'W', 'B' ],
    [ 'W', 'B', 'W', 'B', 'W', 'W', 'B', 'W', 'B', 'B', 'W', 'B', 'W', 'B', 'B', 'W', 'B', 'W', 'B', 'W' ],
    [ 'W', 'B', 'B', 'W', 'B', 'W', 'W', 'B', 'W', 'W', 'B', 'W', 'B', 'W', 'B', 'B', 'W', 'B', 'W', 'B' ],
    [ 'B', 'W', 'B', 'W', 'W', 'B', 'B', 'W', 'B', 'B', 'W', 'W', 'B', 'B', 'W', 'W', 'B', 'W', 'B', 'W' ],
    [ 'W', 'B', 'W', 'B', 'B', 'W', 'B', 'W', 'B', 'W', 'W', 'B', 'W', 'B', 'W', 'B', 'W', 'B', 'W', 'B' ],
    [ 'B', 'W', 'B', 'B', 'W', 'B', 'W', 'B', 'W', 'W', 'B', 'B', 'W', 'W', 'B', 'W', 'B', 'W', 'W', 'B' ],
]
Solutions found: 1
status: OPTIMAL
Time taken: 0.03 seconds
```

**Solved puzzle**

Applying the solution to the puzzle visually:

<img src="https://raw.githubusercontent.com/Ar-Kareem/puzzle_solver/master/images/binairo_solved.png" alt="Binairo solved" width="500">
