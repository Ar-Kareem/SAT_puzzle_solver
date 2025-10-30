# Towers (Puzzle Type #9)

This is a dedicated solver for Towers

Below are the details of how to utilize the solver. In addition, the solver gives all possible solutions to the input thus it can be utilized to figure out if a single partial input board has multiple possible solutions.

(The solver under the hood mainly utilizes the CP-SAT solver from Google OR-Tools)

* [**Play online**](https://www.chiark.greenend.org.uk/~sgtatham/puzzles/js/towers.html)

* [**Instructions**](https://www.chiark.greenend.org.uk/~sgtatham/puzzles/doc/towers.html#towers)

You have a square grid. On each square of the grid you can build a tower, with its height ranging from 1 to the size of the grid. Around the edge of the grid are some numeric clues.

Your task is to build a tower on every square, in such a way that:

  - Each row contains every possible height of tower once
  - Each column contains every possible height of tower once
  - Each numeric clue describes the number of towers that can be seen if you look into the square from that direction, assuming that shorter towers are hidden behind taller ones. For example, in a 5×5 grid, a clue marked ‘5’ indicates that the five tower heights must appear in increasing order (otherwise you would not be able to see all five towers), whereas a clue marked ‘1’ indicates that the tallest tower (the one marked 5) must come first.

In harder or larger puzzles, some towers will be specified for you as well as the clues round the edge, and some edge clues may be missing. 

**Unsolved puzzle**

<img src="https://raw.githubusercontent.com/Ar-Kareem/puzzle_solver/master/images/puzzles/towers_unsolved.png" alt="Towers unsolved" width="500">

Code to utilize this package and solve the puzzle:
```python
import numpy as np
from puzzle_solver import towers_solver as solver
board = np.array([
  [' ', ' ', ' ', ' ', ' ', ' '],
  [' ', ' ', ' ', ' ', ' ', ' '],
  [' ', ' ', '3', ' ', ' ', ' '],
  [' ', ' ', ' ', ' ', ' ', ' '],
  [' ', ' ', ' ', ' ', ' ', ' '],
  [' ', ' ', ' ', ' ', ' ', ' '],
])
t = np.array([2, -1, 2, 2, 2, 3])
b = np.array([2, 4, -1, 4, -1, -1])
r = np.array([3, -1, 2, -1, -1, -1])
l = np.array([-1, -1, -1, 2, -1, 4])
binst = solver.Board(board=board, sides={'top': t, 'bottom': b, 'right': r, 'left': l})
solutions = binst.solve_and_print()
```
**Script Output**
```
Solution found
[[5 6 4 1 2 3]
 [3 4 2 6 1 5]
 [4 5 3 2 6 1]
 [2 1 6 5 3 4]
 [6 3 1 4 5 2]
 [1 2 5 3 4 6]]
Solutions found: 1
status: OPTIMAL
Time taken: 0.03 seconds
```

**Solved puzzle**

<img src="https://raw.githubusercontent.com/Ar-Kareem/puzzle_solver/master/images/puzzles/towers_solved.png" alt="Towers solved" width="500">
