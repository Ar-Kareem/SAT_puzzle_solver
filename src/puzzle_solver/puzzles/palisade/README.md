# Palisade (Puzzle Type #43)

* [**Play online**](https://www.chiark.greenend.org.uk/~sgtatham/puzzles/js/palisade.html)

* [**Instructions**](https://www.chiark.greenend.org.uk/~sgtatham/puzzles/doc/palisade.html#palisade)

You're given a grid of N squares and a region size M, some of which contain numbers. Your goal is to subdivide the grid into (N/M) contiguous regions, where every region is of size M, such that each square containing a number is adjacent to exactly that many edges (including those between the inside and the outside of the grid). 

**Unsolved puzzle**

<img src="https://raw.githubusercontent.com/Ar-Kareem/puzzle_solver/master/images/puzzles/palisade_unsolved.png" alt="Palisade unsolved" width="500">

Code to utilize this package and solve the puzzle:

(Note: it takes a few seconds for the model to be built if the region size is larger than 8 and around 10 seconds for a region size of 10)

```python
import numpy as np
from puzzle_solver import palisade_solver as solver
board = np.array([
    ['2', ' ', ' ', ' ', ' ', '3', ' ', ' ', '1', '1', '3', ' ', ' ', ' ', ' '],
    ['3', '2', '1', ' ', '2', '3', ' ', ' ', ' ', ' ', ' ', '2', ' ', '0', ' '],
    [' ', ' ', ' ', '1', '1', ' ', ' ', '1', ' ', ' ', ' ', '1', ' ', ' ', ' '],
    [' ', '3', '2', ' ', ' ', ' ', ' ', '2', '3', ' ', ' ', ' ', '1', ' ', ' '],
    [' ', '0', '1', ' ', '2', ' ', ' ', '0', ' ', ' ', ' ', '1', ' ', '3', '2'],
    ['1', '0', ' ', ' ', ' ', '2', '2', ' ', '2', ' ', '3', ' ', '0', '2', ' '],
    [' ', ' ', ' ', ' ', ' ', '3', ' ', ' ', ' ', '2', ' ', ' ', ' ', ' ', ' '],
    [' ', '1', ' ', ' ', ' ', '3', '1', ' ', '1', ' ', ' ', ' ', ' ', '1', ' '],
    [' ', ' ', ' ', '0', ' ', ' ', '0', ' ', ' ', '1', '2', ' ', ' ', ' ', '3'],
    [' ', ' ', ' ', ' ', ' ', ' ', '1', ' ', ' ', '2', ' ', ' ', '1', '2', '1'],
    [' ', ' ', ' ', ' ', '1', ' ', '2', '3', '1', ' ', ' ', ' ', '2', ' ', '1'],
    ['2', ' ', '1', ' ', '2', '2', '1', ' ', ' ', '2', ' ', ' ', ' ', ' ', ' '],
])
binst = solver.Board(board, region_size=10)
solutions = binst.solve_and_print()
```

**Script Output**

```python
Solution found
    0   0   0   0   0   0   0   0   0   0   1   1   1   1   1  
    0   1   2   3   4   5   6   7   8   9   0   1   2   3   4
  ┌───────────────────┬───────────────────────┬───────────────┐
 0│ 2   ·   ·   ·   · │ 3   ·   ·   1   1   3 │ ·   ·   ·   · │
  │   ┌───────────┐   ├───────┬───┐       ┌───┴───┐           │
 1│ 3 │ 2   1   · │ 2 │ 3   · │ · │ ·   · │ ·   2 │ ·   0   · │
  ├───┘           │   └───┐   │   └───┐   └───┐   └───┐       │
 2│ ·   ·   ·   1 │ 1   · │ · │ 1   · │ ·   · │ 1   · │ ·   · │
  │   ┌───┐       │   ┌───┘   │   ┌───┴───────┘       └───┐   │
 3│ · │ 3 │ 2   · │ · │ ·   · │ 2 │ 3   ·   ·   ·   1   · │ · │
  ├───┘   └───────┼───┘   ┌───┘   └───┬───────────────┬───┴───┤
 4│ ·   0   1   · │ 2   · │ ·   0   · │ ·   ·   1   · │ 3   2 │
  │           ┌───┘       │           │   ┌───┐       └───┐   │
 5│ 1   0   · │ ·   ·   2 │ 2   ·   2 │ · │ 3 │ ·   0   2 │ · │
  │       ┌───┴───────────┼───┬───────┴───┤   ├───┐       │   │
 6│ ·   · │ ·   ·   ·   3 │ · │ ·   ·   2 │ · │ · │ ·   · │ · │
  ├───────┘   ┌───────────┤   └───┐       │   │   └───────┘   │
 7│ ·   1   · │ ·   ·   3 │ 1   · │ 1   · │ · │ ·   ·   1   · │
  │       ┌───┘       ┌───┘       │       │   └───────┐   ┌───┤
 8│ ·   · │ ·   0   · │ ·   0   · │ ·   1 │ 2   ·   · │ · │ 3 │
  │   ┌───┘       ┌───┤           ├───┐   └───┐       ├───┘   │
 9│ · │ ·   ·   · │ · │ ·   1   · │ · │ 2   · │ ·   1 │ 2   1 │
  ├───┤   ┌───────┘   ├───────┐   │   └───┐   │       │       │
10│ · │ · │ ·   ·   1 │ ·   2 │ 3 │ 1   · │ · │ ·   2 │ ·   1 │
  │   └───┘           │       └───┘       ├───┴───────┘       │
11│ 2   ·   1   ·   2 │ 2   1   ·   ·   2 │ ·   ·   ·   ·   · │
  └───────────────────┴───────────────────┴───────────────────┘
Solutions found: 1
status: OPTIMAL
Time taken: 11.94 seconds
```

**Solved puzzle**

Applying the solution to the puzzle visually:

<img src="https://raw.githubusercontent.com/Ar-Kareem/puzzle_solver/master/images/puzzles/palisade_solved.png" alt="Palisade solved" width="500">
