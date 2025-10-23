# Thermometers (Puzzle Type #26)

This is a dedicated solver for Thermometers

Below are the details of how to utilize the solver. In addition, the solver gives all possible solutions to the input thus it can be utilized to figure out if a single partial input board has multiple possible solutions.

(The solver under the hood mainly utilizes the CP-SAT solver from Google OR-Tools)

* [**Play online**](https://www.puzzle-thermometers.com/)

You have to fill some thermometers with mercury starting from the bulb and going toward the end without gaps.
The numbers outside the grid show the number of filled cells horizontally and vertically. 

**Unsolved puzzle**

<img src="https://raw.githubusercontent.com/Ar-Kareem/puzzle_solver/master/images/thermometers_unsolved.png" alt="Thermometers unsolved" width="500">

Code to utilize this package and solve the puzzle:

```python
import numpy as np
from puzzle_solver import thermometers_solver as solver
board = np.array([
  ['R', 'R', 'D', 'R', 'D', 'R', 'X', 'D', 'L', 'X', 'L', 'L', 'L', 'L', 'L'],
  ['D', 'D', 'D', 'U', 'X', 'U', 'X', 'R', 'R', 'R', 'R', 'D', 'D', 'R', 'U'],
  ['D', 'D', 'D', 'U', 'X', 'U', 'U', 'R', 'R', 'R', 'X', 'D', 'D', 'D', 'D'],
  ['X', 'D', 'D', 'U', 'U', 'U', 'L', 'U', 'R', 'R', 'D', 'X', 'D', 'X', 'X'],
  ['X', 'D', 'D', 'U', 'U', 'R', 'R', 'R', 'R', 'X', 'R', 'X', 'D', 'R', 'X'],
  ['U', 'D', 'D', 'U', 'U', 'R', 'X', 'R', 'R', 'R', 'R', 'D', 'D', 'R', 'D'],
  ['U', 'D', 'D', 'R', 'R', 'X', 'R', 'R', 'R', 'R', 'D', 'D', 'R', 'X', 'D'],
  ['U', 'D', 'D', 'U', 'X', 'L', 'X', 'L', 'R', 'X', 'X', 'R', 'X', 'X', 'L'],
  ['U', 'D', 'D', 'R', 'X', 'U', 'L', 'L', 'L', 'L', 'L', 'L', 'L', 'L', 'L'],
  ['X', 'D', 'X', 'U', 'R', 'R', 'R', 'R', 'R', 'R', 'R', 'R', 'R', 'D', 'U'],
  ['U', 'D', 'X', 'U', 'R', 'R', 'X', 'R', 'R', 'R', 'R', 'X', 'X', 'L', 'U'],
  ['U', 'R', 'U', 'U', 'R', 'X', 'R', 'X', 'R', 'X', 'R', 'R', 'R', 'R', 'U'],
  ['U', 'R', 'X', 'R', 'R', 'R', 'R', 'R', 'R', 'R', 'R', 'R', 'X', 'X', 'L'],
  ['U', 'U', 'R', 'R', 'X', 'D', 'R', 'R', 'D', 'R', 'X', 'X', 'L', 'L', 'U'],
  ['U', 'U', 'U', 'L', 'L', 'R', 'X', 'X', 'L', 'U', 'R', 'R', 'R', 'U', 'U'],
])
top = np.array([7, 4, 12, 8, 4, 6, 5, 7, 5, 4, 8, 9, 13, 8, 12])
side = np.array([8, 10, 9, 10, 6, 10, 4, 6, 6, 10, 5, 7, 6, 6, 9])
binst = solver.Board(board=board, top=top, side=side)
solutions = binst.solve_and_print()
```
**Script Output**

```python
Solution found
[['X' 'X' 'X' ' ' ' ' ' ' ' ' 'X' 'X' ' ' ' ' ' ' 'X' 'X' 'X']
 ['X' ' ' 'X' ' ' ' ' ' ' ' ' 'X' 'X' 'X' 'X' 'X' 'X' 'X' 'X']
 ['X' ' ' 'X' 'X' ' ' 'X' 'X' 'X' ' ' ' ' ' ' 'X' 'X' ' ' 'X']
 [' ' ' ' 'X' 'X' ' ' 'X' 'X' 'X' 'X' 'X' 'X' ' ' 'X' ' ' 'X']
 [' ' ' ' 'X' 'X' ' ' ' ' ' ' ' ' ' ' ' ' 'X' ' ' 'X' 'X' 'X']
 [' ' ' ' 'X' 'X' ' ' ' ' ' ' 'X' 'X' 'X' 'X' 'X' 'X' 'X' 'X']
 [' ' ' ' 'X' ' ' ' ' ' ' ' ' ' ' ' ' ' ' ' ' 'X' 'X' ' ' 'X']
 [' ' ' ' 'X' ' ' ' ' ' ' 'X' 'X' ' ' ' ' ' ' 'X' 'X' ' ' 'X']
 [' ' ' ' 'X' ' ' ' ' ' ' ' ' ' ' ' ' ' ' 'X' 'X' 'X' 'X' 'X']
 [' ' ' ' ' ' ' ' 'X' 'X' 'X' 'X' 'X' 'X' 'X' 'X' 'X' ' ' 'X']
 [' ' ' ' ' ' 'X' 'X' 'X' 'X' ' ' ' ' ' ' ' ' ' ' ' ' ' ' 'X']
 ['X' ' ' ' ' 'X' ' ' ' ' ' ' ' ' ' ' ' ' 'X' 'X' 'X' 'X' 'X']
 ['X' 'X' 'X' 'X' 'X' 'X' ' ' ' ' ' ' ' ' ' ' ' ' ' ' ' ' ' ']
 ['X' 'X' 'X' ' ' ' ' 'X' ' ' ' ' ' ' ' ' ' ' ' ' 'X' 'X' ' ']
 ['X' 'X' 'X' 'X' 'X' ' ' ' ' ' ' ' ' ' ' 'X' 'X' 'X' 'X' ' ']]
Solutions found: 1
status: OPTIMAL
Time taken: 0.01 seconds
```

**Solved puzzle**

<img src="https://raw.githubusercontent.com/Ar-Kareem/puzzle_solver/master/images/thermometers_solved.png" alt="Thermometers solved" width="500">
