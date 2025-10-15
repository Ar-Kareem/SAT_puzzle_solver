 Signpost (Puzzle Type #11)

This is a dedicated solver for Signpost

Below are the details of how to utilize the solver. In addition, the solver gives all possible solutions to the input thus it can be utilized to figure out if a single partial input board has multiple possible solutions.

(The solver under the hood mainly utilizes the CP-SAT solver from Google OR-Tools)

* [**Play online**](https://www.chiark.greenend.org.uk/~sgtatham/puzzles/js/signpost.html)

* [**Instructions**](https://www.chiark.greenend.org.uk/~sgtatham/puzzles/doc/signpost.html#signpost)

You have a grid of squares; each square (except the last one) contains an arrow, and some squares also contain numbers. Your job is to connect the squares to form a continuous list of numbers starting at 1 and linked in the direction of the arrows – so the arrow inside the square with the number 1 will point to the square containing the number 2, which will point to the square containing the number 3, etc. Each square can be any distance away from the previous one, as long as it is somewhere in the direction of the arrow.

By convention the first and last numbers are shown; one or more interim numbers may also appear at the beginning. 

**Unsolved puzzle**

<img src="../images/signpost_unsolved.png" alt="Signpost unsolved" width="500">

Code to utilize this package and solve the puzzle:
```python
import numpy as np
from . import solver
# Q = up-left, W = up, E = up-right, A = left, D = right, Z = down-left, X = down, C = down-right
bor1 = np.array([
  ['C', 'D', 'D', 'X', 'D', 'Z', 'X'],
  ['D', 'C', 'D', 'X', 'X', 'A', 'A'],
  ['X', 'X', 'D', 'Q', 'Z', 'W', 'A'],
  ['W', 'D', 'W', 'W', 'X', 'Z', 'X'],
  ['X', 'A', 'Q', 'Q', 'A', 'Q', 'X'],
  ['D', 'W', 'W', 'A', 'E', 'A', 'Z'],
  ['D', 'E', 'D', 'E', 'D', 'A', ' '],
])
bor2 = np.array([
  [ 1,  0, 23,  0,  0,  0,  0],
  [30, 32,  0,  0,  0,  0,  0],
  [ 0,  0,  2,  0,  0,  0,  0],
  [ 0,  0,  0,  0,  0,  0,  0],
  [ 0, 45,  0,  0, 33,  0,  0],
  [ 0,  0, 22,  8, 39, 10,  0],
  [ 0,  0,  0,  0,  0, 20, 49],
])

binst = solver.Board(board=bor1, values=bor2)
solutions = binst.solve_and_print()
```
**Script Output**
```
Solution found
[[1 42 23 7 43 44 24]
 [30 32 36 5 37 4 31]
 [28 12 2 41 26 3 25]
 [29 13 35 6 38 14 17]
 [46 45 27 34 33 40 18]
 [9 11 22 8 39 10 19]
 [47 21 15 16 48 20 49]]
Solutions found: 1
status: OPTIMAL
Time taken: 0.03 seconds
```

**Solved puzzle**

<img src="../images/signpost_solved.png" alt="Signpost solved" width="500">
