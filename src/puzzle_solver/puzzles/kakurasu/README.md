# Kakurasu (Puzzle Type #30)

* [**Play online**](https://www.puzzle-kakurasu.com/)

The goal is to make some of the cells black in such a way that:

1. The black cells on each row sum up to the number on the right.

2. The black cells on each column sum up to the number on the bottom.

3. If a black cell is first on its row/column its value is 1. If it is second its value is 2 etc. 

**Unsolved puzzle**

<img src="https://raw.githubusercontent.com/Ar-Kareem/puzzle_solver/master/images/kakurasu_unsolved.png" alt="Kakurasu unsolved" width="500">

Code to utilize this package and solve the puzzle:

```python
import numpy as np
from puzzle_solver import kakurasu_solver as solver
side = np.array([27, 6, 1, 12, 37, 37, 11, 4, 29, 23, 66, 55])
bottom = np.array([22, 1, 25, 36, 10, 22, 25, 35, 32, 28, 45, 45])
binst = solver.Board(side=side, bottom=bottom)
solutions = binst.solve_and_print()
```


**Script Output**

```python
Solution found
    0   0   0   0   0   0   0   0   0   0   1   1
    0   1   2   3   4   5   6   7   8   9   0   1
  ┌───┬───┬───┬───┬───┬───┬───┬───┬───┬───┬───┬───┐
 0│▒▒▒│▒▒▒│   │▒▒▒│   │   │   │▒▒▒│   │   │   │▒▒▒│
  ├───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┤
 1│   │   │   │   │   │▒▒▒│   │   │   │   │   │   │
  ├───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┤
 2│▒▒▒│   │   │   │   │   │   │   │   │   │   │   │
  ├───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┤
 3│   │   │   │   │▒▒▒│   │▒▒▒│   │   │   │   │   │
  ├───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┤
 4│   │   │▒▒▒│▒▒▒│   │   │   │▒▒▒│   │▒▒▒│   │▒▒▒│
  ├───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┤
 5│▒▒▒│   │   │   │▒▒▒│   │   │▒▒▒│   │   │▒▒▒│▒▒▒│
  ├───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┤
 6│   │   │   │   │   │   │   │   │   │   │▒▒▒│   │
  ├───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┤
 7│   │   │   │▒▒▒│   │   │   │   │   │   │   │   │
  ├───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┤
 8│   │   │▒▒▒│   │   │▒▒▒│   │   │▒▒▒│   │▒▒▒│   │
  ├───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┤
 9│   │   │   │▒▒▒│   │   │▒▒▒│   │   │   │   │▒▒▒│
  ├───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┤
10│   │   │▒▒▒│   │   │▒▒▒│▒▒▒│▒▒▒│▒▒▒│▒▒▒│▒▒▒│▒▒▒│
  ├───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┤
11│▒▒▒│   │   │▒▒▒│   │   │   │▒▒▒│▒▒▒│▒▒▒│▒▒▒│▒▒▒│
  └───┴───┴───┴───┴───┴───┴───┴───┴───┴───┴───┴───┘
Solutions found: 1
status: OPTIMAL
Time taken: 0.00 seconds
```

**Solved puzzle**

<img src="https://raw.githubusercontent.com/Ar-Kareem/puzzle_solver/master/images/kakurasu_solved.png" alt="Kakurasu solved" width="500">
