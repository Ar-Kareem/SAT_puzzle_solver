# Mosaic (Puzzle Type #10)

This is a dedicated solver for Mosaic

Below are the details of how to utilize the solver. In addition, the solver gives all possible solutions to the input thus it can be utilized to figure out if a single output has multiple possible solutions.

(The solver mainly utilizes the CP-SAT solver from Google OR-Tools)

Game: https://www.chiark.greenend.org.uk/~sgtatham/puzzles/js/mosaic.html

Instructions: https://www.chiark.greenend.org.uk/~sgtatham/puzzles/doc/mosaic.html#mosaic

Unsolved puzzle:

<img src="../images/mosaic_unsolved.png" alt="Mosaic unsolved" width="500">

Code to utilize this package and solve the puzzle:
```python
import numpy as np
from . import board
bor = np.array([
  ['*', '*', '2', '1', '*', '*', '*', '3', '*', '4', '2', '2', '*', '*', '4'],
  ['3', '*', '*', '*', '4', '*', '*', '*', '*', '*', '4', '*', '2', '*', '*'],
  ['4', '*', '*', '5', '*', '5', '*', '*', '5', '*', '3', '3', '2', '5', '*'],
  ['*', '*', '7', '*', '4', '*', '*', '5', '*', '*', '*', '*', '*', '5', '*'],
  ['*', '6', '7', '*', '*', '4', '*', '7', '*', '*', '*', '*', '7', '7', '*'],
  ['3', '*', '*', '3', '*', '5', '7', '7', '6', '4', '*', '4', '*', '5', '*'],
  ['*', '*', '4', '*', '5', '7', '8', '*', '5', '*', '1', '3', '4', '5', '*'],
  ['*', '5', '*', '4', '3', '*', '*', '*', '7', '*', '3', '*', '3', '*', '*'],
  ['3', '*', '*', '*', '*', '*', '*', '5', '*', '6', '*', '*', '*', '*', '*'],
  ['4', '*', '7', '*', '5', '*', '*', '4', '6', '7', '*', '3', '*', '3', '*'],
  ['5', '*', '*', '*', '*', '*', '*', '*', '6', '*', '*', '3', '5', '*', '*'],
  ['*', '*', '*', '5', '4', '5', '3', '*', '7', '*', '*', '5', '6', '6', '*'],
  ['2', '*', '*', '*', '3', '4', '*', '*', '*', '7', '*', '*', '7', '*', '3'],
  ['1', '*', '*', '5', '*', '*', '*', '5', '*', '*', '*', '6', '*', '6', '*'],
  ['*', '*', '3', '*', '2', '*', '3', '*', '2', '*', '*', '*', '*', '*', '*']
])
binst = board.Board(board=bor)
solutions = binst.solve_and_print()
```
Output:
```
Solution found
[[' ' 'B' ' ' ' ' ' ' ' ' ' ' ' ' 'B' ' ' 'B' ' ' ' ' 'B' 'B']
 [' ' 'B' ' ' ' ' 'B' 'B' ' ' 'B' 'B' ' ' 'B' ' ' ' ' 'B' 'B']
 [' ' 'B' 'B' ' ' 'B' 'B' ' ' ' ' ' ' 'B' 'B' ' ' ' ' ' ' 'B']
 ['B' 'B' 'B' 'B' ' ' ' ' 'B' 'B' 'B' ' ' ' ' ' ' 'B' ' ' 'B']
 [' ' 'B' 'B' ' ' ' ' 'B' ' ' 'B' 'B' 'B' ' ' 'B' 'B' 'B' ' ']
 [' ' 'B' ' ' 'B' ' ' 'B' 'B' ' ' 'B' ' ' ' ' 'B' 'B' 'B' 'B']
 ['B' ' ' 'B' ' ' ' ' 'B' 'B' 'B' 'B' ' ' ' ' ' ' ' ' ' ' ' ']
 [' ' ' ' 'B' ' ' 'B' 'B' 'B' 'B' 'B' ' ' ' ' ' ' 'B' ' ' 'B']
 [' ' 'B' 'B' ' ' ' ' ' ' ' ' 'B' 'B' 'B' 'B' 'B' ' ' 'B' ' ']
 ['B' 'B' 'B' 'B' 'B' 'B' ' ' ' ' ' ' 'B' 'B' ' ' ' ' 'B' ' ']
 [' ' 'B' ' ' 'B' 'B' ' ' 'B' ' ' 'B' 'B' ' ' ' ' ' ' 'B' ' ']
 ['B' 'B' ' ' ' ' 'B' ' ' ' ' 'B' 'B' 'B' ' ' 'B' 'B' 'B' 'B']
 [' ' ' ' 'B' ' ' 'B' ' ' 'B' ' ' 'B' 'B' 'B' 'B' 'B' ' ' 'B']
 [' ' ' ' 'B' 'B' ' ' ' ' 'B' ' ' 'B' 'B' ' ' 'B' 'B' ' ' ' ']
 ['B' ' ' 'B' ' ' ' ' 'B' 'B' ' ' ' ' ' ' ' ' ' ' 'B' 'B' 'B']]
Solutions found: 1
status: OPTIMAL
```

Which exactly matches the true solutions:

<img src="../images/mosaic_solved.png" alt="Mosaic solved" width="500">
