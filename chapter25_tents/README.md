# Tents (Puzzle Type #4)

This is a dedicated solver for Tents

Below are the details of how to utilize the solver. In addition, the solver gives all possible solutions to the input thus it can be utilized to figure out if a single output has multiple possible solutions.

(The solver mainly utilizes the CP-SAT solver from Google OR-Tools)

* [**Play online**](https://www.chiark.greenend.org.uk/~sgtatham/puzzles/js/tents.html)

* [**Instructions**](https://www.chiark.greenend.org.uk/~sgtatham/puzzles/doc/tents.html#tents)

**Unsolved puzzle**

<img src="../images/tents_unsolved.png" alt="Tents unsolved" width="500">

Code to utilize this package and solve the puzzle:
```python
import numpy as np
from . import board
bor = np.array([
  ['*', 'T', '*', '*', '*', '*', '*', '*', 'T', '*', 'T', '*', 'T', '*', '*'],
  ['*', '*', '*', '*', 'T', '*', '*', 'T', '*', 'T', '*', '*', 'T', '*', '*'],
  ['*', 'T', '*', 'T', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*'],
  ['*', '*', '*', '*', '*', '*', '*', '*', 'T', '*', '*', '*', 'T', '*', 'T'],
  ['*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*'],
  ['*', 'T', '*', '*', 'T', '*', 'T', '*', '*', 'T', '*', '*', 'T', 'T', '*'],
  ['*', 'T', '*', '*', 'T', '*', '*', '*', 'T', '*', '*', '*', '*', '*', '*'],
  ['*', '*', '*', '*', '*', '*', 'T', '*', '*', '*', '*', '*', '*', '*', '*'],
  ['*', '*', '*', '*', '*', 'T', '*', '*', '*', '*', 'T', '*', '*', 'T', '*'],
  ['*', '*', '*', 'T', '*', '*', '*', '*', '*', '*', '*', '*', 'T', '*', 'T'],
  ['T', '*', '*', '*', '*', '*', '*', 'T', '*', '*', '*', 'T', '*', '*', '*'],
  ['T', '*', '*', '*', 'T', '*', 'T', '*', '*', '*', '*', '*', '*', '*', '*'],
  ['*', '*', '*', '*', '*', '*', '*', '*', 'T', '*', 'T', '*', '*', '*', 'T'],
  ['*', 'T', '*', '*', '*', 'T', '*', '*', '*', '*', '*', '*', 'T', '*', '*'],
  ['*', 'T', '*', '*', 'T', '*', '*', '*', '*', 'T', '*', 'T', '*', '*', '*'],
])
side = np.array([4, 1, 6, 0, 5, 2, 3, 1, 5, 2, 3, 2, 4, 3, 4])
top = np.array([4, 2, 4, 1, 3, 3, 3, 3, 3, 3, 2, 2, 6, 2, 4])

binst = board.Board(board=bor, sides={'top': top, 'side': side})
solutions = binst.solve_and_print()
```
**Script Output**
```
Solution found
[[' ' 'T' 'E' ' ' ' ' ' ' ' ' 'E' 'T' ' ' 'T' 'E' 'T' 'E' ' ']
 [' ' ' ' ' ' ' ' 'T' 'E' ' ' 'T' ' ' 'T' ' ' ' ' 'T' ' ' ' ']
 ['E' 'T' 'E' 'T' ' ' ' ' ' ' 'E' ' ' 'E' ' ' ' ' 'E' ' ' 'E']
 [' ' ' ' ' ' ' ' ' ' ' ' ' ' ' ' 'T' ' ' ' ' ' ' 'T' ' ' 'T']
 [' ' 'E' ' ' ' ' 'E' ' ' 'E' ' ' 'E' ' ' ' ' ' ' 'E' ' ' ' ']
 [' ' 'T' ' ' ' ' 'T' ' ' 'T' ' ' ' ' 'T' 'E' ' ' 'T' 'T' 'E']
 [' ' 'T' ' ' ' ' 'T' 'E' ' ' 'E' 'T' ' ' ' ' ' ' 'E' ' ' ' ']
 [' ' 'E' ' ' ' ' ' ' ' ' 'T' ' ' ' ' ' ' ' ' ' ' ' ' ' ' ' ']
 [' ' ' ' ' ' ' ' 'E' 'T' 'E' ' ' ' ' 'E' 'T' ' ' 'E' 'T' 'E']
 ['E' ' ' 'E' 'T' ' ' ' ' ' ' ' ' ' ' ' ' ' ' ' ' 'T' ' ' 'T']
 ['T' ' ' ' ' ' ' ' ' ' ' ' ' 'T' 'E' ' ' ' ' 'T' 'E' ' ' 'E']
 ['T' ' ' ' ' 'E' 'T' 'E' 'T' ' ' ' ' ' ' ' ' ' ' ' ' ' ' ' ']
 ['E' ' ' ' ' ' ' ' ' ' ' ' ' ' ' 'T' 'E' 'T' 'E' ' ' 'E' 'T']
 [' ' 'T' 'E' ' ' 'E' 'T' 'E' ' ' ' ' ' ' ' ' ' ' 'T' ' ' ' ']
 ['E' 'T' ' ' ' ' 'T' ' ' ' ' ' ' 'E' 'T' 'E' 'T' 'E' ' ' ' ']]
Solutions found: 1
status: OPTIMAL
```

**Solved puzzle**

<img src="../images/tents_solved.png" alt="Tents solved" width="500">
