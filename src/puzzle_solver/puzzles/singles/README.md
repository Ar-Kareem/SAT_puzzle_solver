# Singles (Puzzle Type #10)

This is a dedicated solver for Singles. Also known as Hitori.

Below are the details of how to utilize the solver. In addition, the solver gives all possible solutions to the input thus it can be utilized to figure out if a single partial input board has multiple possible solutions.

(The solver under the hood mainly utilizes the CP-SAT solver from Google OR-Tools)


* [**Play online 1**](https://www.chiark.greenend.org.uk/~sgtatham/puzzles/js/singles.html)

* [**Play online 2**](https://www.puzzle-hitori.com/)

* [**Instructions**](https://www.chiark.greenend.org.uk/~sgtatham/puzzles/doc/singles.html#singles)

You have a grid of white squares, all of which contain numbers. Your task is to colour some of the squares black (removing the number) so as to satisfy all of the following conditions:

  - No number occurs more than once in any row or column.
  - No black square is horizontally or vertically adjacent to any other black square.
  - The remaining white squares must all form one contiguous region (connected by edges, not just touching at corners).

**Unsolved puzzle**

<img src="https://raw.githubusercontent.com/Ar-Kareem/puzzle_solver/master/images/singles_unsolved.png" alt="Singles unsolved" width="500">

Code to utilize this package and solve the puzzle:
```python
import numpy as np
from puzzle_solver import singles_solver as solver
board = np.array([
  [1, 6, 5, 4, 9, 8, 9, 3, 5, 1, 3, 7],
  [2, 8, 5, 7, 1, 1, 4, 3, 6, 3, 10, 7],
  [6, 7, 7, 11, 2, 6, 3, 10, 10, 2, 3, 3],
  [11, 9, 4, 3, 6, 1, 2, 5, 3, 10, 7, 8], 
  [5, 5, 4, 9, 7, 9, 6, 6, 11, 5, 4, 11],
  [1, 3, 7, 9, 12, 5, 4, 2, 9, 6, 12, 4],
  [6, 11, 1, 3, 6, 4, 11, 2, 2, 10, 8, 10],
  [3, 11, 12, 6, 2, 9, 9, 1, 4, 8, 12, 5],
  [4, 8, 8, 5, 11, 3, 3, 6, 5, 9, 1, 4],
  [2, 4, 6, 2, 1, 10, 1, 10, 8, 5, 4, 6],
  [5, 1, 6, 10, 9, 4, 8, 4, 8, 3, 2, 12],
  [11, 2, 12, 10, 8, 3, 5, 4, 10, 4, 8, 11],
])
binst = solver.Board(board=board)
solutions = binst.solve_and_print()
```

**Script Output**

```python
Solution found
    0   0   0   0   0   0   0   0   0   0   1   1  
    0   1   2   3   4   5   6   7   8   9   0   1
  ┌───┬───┬───┬───┬───┬───┬───┬───┬───┬───┬───┬───┐
 0│▒▒▒│ 6 │▒▒▒│ 4 │▒▒▒│ 8 │ 9 │▒▒▒│ 5 │ 1 │ 3 │ 7 │
  ├───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┤
 1│ 2 │ 8 │ 5 │ 7 │ 1 │▒▒▒│ 4 │ 3 │ 6 │▒▒▒│10 │▒▒▒│
  ├───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┤
 2│▒▒▒│ 7 │▒▒▒│11 │▒▒▒│ 6 │▒▒▒│10 │▒▒▒│ 2 │▒▒▒│ 3 │
  ├───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┤
 3│11 │ 9 │ 4 │▒▒▒│ 6 │ 1 │ 2 │ 5 │ 3 │10 │ 7 │ 8 │
  ├───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┤
 4│▒▒▒│ 5 │▒▒▒│ 9 │ 7 │▒▒▒│ 6 │▒▒▒│11 │▒▒▒│ 4 │▒▒▒│
  ├───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┤
 5│ 1 │ 3 │ 7 │▒▒▒│12 │ 5 │▒▒▒│ 2 │ 9 │ 6 │▒▒▒│ 4 │
  ├───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┤
 6│ 6 │▒▒▒│ 1 │ 3 │▒▒▒│ 4 │11 │▒▒▒│ 2 │▒▒▒│ 8 │10 │
  ├───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┤
 7│ 3 │11 │▒▒▒│ 6 │ 2 │ 9 │▒▒▒│ 1 │ 4 │ 8 │12 │ 5 │
  ├───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┤
 8│ 4 │▒▒▒│ 8 │ 5 │11 │▒▒▒│ 3 │ 6 │▒▒▒│ 9 │ 1 │▒▒▒│
  ├───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┤
 9│▒▒▒│ 4 │▒▒▒│ 2 │▒▒▒│10 │ 1 │▒▒▒│ 8 │ 5 │▒▒▒│ 6 │
  ├───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┤
10│ 5 │ 1 │ 6 │10 │ 9 │▒▒▒│ 8 │ 4 │▒▒▒│ 3 │ 2 │12 │
  ├───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┤
11│▒▒▒│ 2 │12 │▒▒▒│ 8 │ 3 │ 5 │▒▒▒│10 │ 4 │▒▒▒│11 │
  └───┴───┴───┴───┴───┴───┴───┴───┴───┴───┴───┴───┘
Solutions found: 1
status: OPTIMAL
Time taken: 0.04 seconds
```

**Solved puzzle**

<img src="https://raw.githubusercontent.com/Ar-Kareem/puzzle_solver/master/images/singles_solved.png" alt="Singles solved" width="500">
