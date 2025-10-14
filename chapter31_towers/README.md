# Towers (Puzzle Type #5)

This is a dedicated solver for Towers

Below are the details of how to utilize the solver. In addition, the solver gives all possible solutions to the input thus it can be utilized to figure out if a single output has multiple possible solutions.

(The solver mainly utilizes the CP-SAT solver from Google OR-Tools)

* [**Play online**](https://www.chiark.greenend.org.uk/~sgtatham/puzzles/js/towers.html)

* [**Instructions**](https://www.chiark.greenend.org.uk/~sgtatham/puzzles/doc/towers.html#towers)

**Unsolved puzzle**

<img src="../images/towers_unsolved.png" alt="Towers unsolved" width="500">

Code to utilize this package and solve the puzzle:
```python
import numpy as np
from . import board
bor = np.array([
  ['*', '*', '*', '*', '*', '*'],
  ['*', '*', '*', '*', '*', '*'],
  ['*', '*', '3', '*', '*', '*'],
  ['*', '*', '*', '*', '*', '*'],
  ['*', '*', '*', '*', '*', '*'],
  ['*', '*', '*', '*', '*', '*'],
])
t = np.array([2, -1, 2, 2, 2, 3])
b = np.array([2, 4, -1, 4, -1, -1])
r = np.array([3, -1, 2, -1, -1, -1])
l = np.array([-1, -1, -1, 2, -1, 4])
binst = board.Board(board=bor, sides={'top': t, 'bottom': b, 'right': r, 'left': l})
solutions = binst.solve_and_print()
```
**Script Output**
```
Solution found
[['5' '6' '4' '1' '2' '3']
 ['3' '4' '2' '6' '1' '5']
 ['4' '5' '3' '2' '6' '1']
 ['2' '1' '6' '5' '3' '4']
 ['6' '3' '1' '4' '5' '2']
 ['1' '2' '5' '3' '4' '6']]
Solutions found: 1
status: OPTIMAL
```

**Solved puzzle**

<img src="../images/towers_solved.png" alt="Towers solved" width="500">
