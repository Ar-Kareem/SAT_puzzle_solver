# Filling (Puzzle Type #7)

This is a dedicated solver for Filling (also known as Fillomino).

Below are the details of how to utilize the solver. In addition, the solver gives all possible solutions to the input thus it can be utilized to figure out if a single partial input board has multiple possible solutions.

(The solver under the hood mainly utilizes the CP-SAT solver from Google OR-Tools)

* [**Play online**](https://www.chiark.greenend.org.uk/~sgtatham/puzzles/js/filling.html)

* [**Instructions**](https://www.chiark.greenend.org.uk/~sgtatham/puzzles/doc/filling.html#filling)

You have a grid of squares, some of which contain digits, and the rest of which are empty. Your job is to fill in digits in the empty squares, in such a way that each connected region of squares all containing the same digit has an area equal to that digit.

(‘Connected region’, for the purposes of this game, does not count diagonally separated squares as adjacent.)

For example, it follows that no square can contain a zero, and that two adjacent squares can not both contain a one. No region has an area greater than 9 (because then its area would not be a single digit).

Note: It may take a few seconds for the model to be built.

**Unsolved puzzle**

<img src="https://raw.githubusercontent.com/Ar-Kareem/puzzle_solver/master/images/filling_unsolved.png" alt="Filling unsolved" width="500">

Code to utilize this package and solve the puzzle:
```python
import numpy as np
from puzzle_solver import filling_solver as solver
board = np.array([
  [' ', '4', '2', ' ', ' ', '2', ' '],
  [' ', ' ', '7', ' ', ' ', '3', ' '],
  [' ', ' ', ' ', ' ', '4', ' ', '3'],
  [' ', '6', '6', ' ', '3', ' ', ' '],
  [' ', '7', ' ', '6', '4', '5', ' '],
  [' ', '6', ' ', ' ', ' ', ' ', '4'],
])
binst = solver.Board(board=board)
solutions = binst.solve_and_print()
assert len(solutions) == 1, f'unique solutions != 1, == {len(solutions)}'
```
**Script Output**
```
Solution found

    0   1   2   3   4   5   6
  ┌───────┬───────┬───┬───────┐
 0│ 4   4 │ 2   2 │ 4 │ 2   2 │
  │       ├───┬───┘   ├───────┤
 1│ 4   4 │ 7 │ 4   4 │ 3   3 │
  ├───────┘   ├───┐   ├───┐   │
 2│ 7   7   7 │ 3 │ 4 │ 5 │ 3 │
  │   ┌───────┤   └───┤   └───┤
 3│ 7 │ 6   6 │ 3   3 │ 5   5 │
  │   └───┐   └───┬───┤       │
 4│ 7   7 │ 6   6 │ 4 │ 5   5 │
  ├───┬───┘   ┌───┤   └───────┤
 5│ 1 │ 6   6 │ 1 │ 4   4   4 │
  └───┴───────┴───┴───────────┘
Solutions found: 1
status: OPTIMAL
Time taken: 0.15 seconds
```

**Solved puzzle**

<img src="https://raw.githubusercontent.com/Ar-Kareem/puzzle_solver/master/images/filling_solved.png" alt="Filling solved" width="500">
