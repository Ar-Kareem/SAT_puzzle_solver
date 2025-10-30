# Range (Puzzle Type #13)

This is a dedicated solver for Range. Also known as Kurodoko.

Below are the details of how to utilize the solver. In addition, the solver gives all possible solutions to the input thus it can be utilized to figure out if a single partial input board has multiple possible solutions.

(The solver under the hood mainly utilizes the CP-SAT solver from Google OR-Tools)

* [**Play online 1**](https://www.chiark.greenend.org.uk/~sgtatham/puzzles/js/range.html)

* [**Play online 2**](https://www.puzzle-kurodoko.com/)

* [**Instructions**](https://www.chiark.greenend.org.uk/~sgtatham/puzzles/doc/range.html#range)

You have a grid of squares; some squares contain numbers. Your job is to colour some of the squares black, such that several criteria are satisfied:

  - no square with a number is coloured black.
  - no two black squares are adjacent (horizontally or vertically).
  - for any two white squares, there is a path between them using only white squares.
  - for each square with a number, that number denotes the total number of white squares reachable from that square going in a straight line in any horizontal or vertical direction until hitting a wall or a black square; the square with the number is included in the total (once).

For instance, a square containing the number one must have four black squares as its neighbours by the last criterion; but then it's impossible for it to be connected to any outside white square, which violates the second to last criterion. So no square will contain the number one. 

**Unsolved puzzle**

<img src="https://raw.githubusercontent.com/Ar-Kareem/puzzle_solver/master/images/puzzles/range_unsolved.png" alt="Range unsolved" width="500">

Code to utilize this package and solve the puzzle:
```python
import numpy as np
from puzzle_solver import range_solver as solver
clues = np.array([
  ['  ', '4 ', '2 ', '  ', '  ', '3 ', '  ', '  ', '  ', '8 ', '  ', '  ', '  ', '  ', '6 ', '  '],
  ['  ', '  ', '  ', '  ', '  ', '13', '  ', '18', '  ', '  ', '14', '  ', '  ', '22', '  ', '  '],
  ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '12', '  ', '  ', '  ', '  '],
  ['  ', '  ', '  ', '  ', '12', '  ', '11', '  ', '  ', '  ', '9 ', '  ', '  ', '  ', '  ', '  '],
  ['7 ', '  ', '  ', '  ', '  ', '  ', '6 ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  '],
  ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  '],
  ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '12', '  ', '  ', '  ', '  ', '  ', '5 '],
  ['  ', '  ', '  ', '  ', '  ', '9 ', '  ', '  ', '  ', '9 ', '  ', '4 ', '  ', '  ', '  ', '  '],
  ['  ', '  ', '  ', '  ', '6 ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  '],
  ['  ', '  ', '10', '  ', '  ', '7 ', '  ', '  ', '13', '  ', '10', '  ', '  ', '  ', '  ', '  '],
  ['  ', '7 ', '  ', '  ', '  ', '  ', '6 ', '  ', '  ', '  ', '6 ', '  ', '  ', '13', '5 ', '  '],
])
binst = solver.Board(clues)
solutions = binst.solve_and_print()
```
**Script Output**
```
Solution:
    0   0   0   0   0   0   0   0   0   0   1   1   1   1   1   1  
    0   1   2   3   4   5   6   7   8   9   0   1   2   3   4   5
  ┌───┬───┬───┬───┬───┬───┬───┬───┬───┬───┬───┬───┬───┬───┬───┬───┐
 0│▒▒▒│ 4 │ 2 │▒▒▒│   │ 3 │▒▒▒│   │▒▒▒│ 8 │▒▒▒│   │▒▒▒│   │ 6 │   │
  ├───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┤
 1│   │   │▒▒▒│   │   │13 │   │18 │   │   │14 │   │   │22 │   │▒▒▒│
  ├───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┤
 2│▒▒▒│   │   │   │   │▒▒▒│   │   │   │   │   │12 │   │   │   │   │
  ├───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┤
 3│   │▒▒▒│   │▒▒▒│12 │   │11 │   │   │   │ 9 │▒▒▒│   │   │   │   │
  ├───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┤
 4│ 7 │   │   │   │   │▒▒▒│ 6 │   │▒▒▒│   │▒▒▒│   │   │   │▒▒▒│   │
  ├───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┤
 5│   │   │▒▒▒│   │   │   │   │   │   │   │   │▒▒▒│   │   │   │▒▒▒│
  ├───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┤
 6│▒▒▒│   │   │   │▒▒▒│   │▒▒▒│   │   │12 │   │   │▒▒▒│   │   │ 5 │
  ├───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┤
 7│   │   │   │   │   │ 9 │   │▒▒▒│   │ 9 │▒▒▒│ 4 │   │   │▒▒▒│   │
  ├───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┤
 8│   │▒▒▒│   │   │ 6 │▒▒▒│   │   │   │▒▒▒│   │▒▒▒│   │   │   │   │
  ├───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┤
 9│   │   │10 │   │   │ 7 │▒▒▒│   │13 │   │10 │   │   │   │   │▒▒▒│
  ├───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┤
10│▒▒▒│ 7 │   │   │   │   │ 6 │▒▒▒│   │   │ 6 │   │▒▒▒│13 │ 5 │   │
  └───┴───┴───┴───┴───┴───┴───┴───┴───┴───┴───┴───┴───┴───┴───┴───┘
Solutions found: 1
status: OPTIMAL
Time taken: 0.07 seconds
```

**Solved puzzle**

<img src="https://raw.githubusercontent.com/Ar-Kareem/puzzle_solver/master/images/puzzles/range_solved.png" alt="Range solved" width="500">
