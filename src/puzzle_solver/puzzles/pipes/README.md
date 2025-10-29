# Pipes (Puzzle Type #55)

Also known as Net.

* [**Play online 1**](https://www.chiark.greenend.org.uk/~sgtatham/puzzles/js/net.html)

* [**Play online 2**](https://www.puzzle-pipes.com/)

* [**Instructions**](https://www.chiark.greenend.org.uk/~sgtatham/puzzles/doc/net.html#net)

You are given a grid of cells where each cell has 1, 2, 3, or 4 connections to its neighbors. Each cell can be freely rotated in multiple of 90 degrees, thus your can rotate the cells to be one of four possible states.

The goal is to create a single fully connected graph where each cell's connection must be towards another cell's connection. No loose ends or loops are allowed.

**Unsolved puzzle**

<img src="https://raw.githubusercontent.com/Ar-Kareem/puzzle_solver/master/images/pipes_unsolved.png" alt="Pipes unsolved" width="500">

Code to utilize this package and solve the puzzle:

(Note: cells with 1 or 3 active connections only have 1 unique orientation under rotational symmetry. However, cells with 2 active connections can be either a straight line (2I) or curved line (2L))

```python
import numpy as np
from puzzle_solver import pipes_solver as solver
board=np.array([
    [ '1 ', '3 ', '3 ', '3 ', '1 ', '1 ', '2L', '2L', '2I', '1 ' ],
    [ '1 ', '1 ', '1 ', '3 ', '2I', '1 ', '2I', '3 ', '2I', '1 ' ],
    [ '2I', '1 ', '1 ', '3 ', '2L', '1 ', '3 ', '2I', '1 ', '1 ' ],
    [ '2I', '2I', '1 ', '3 ', '3 ', '3 ', '2L', '3 ', '3 ', '2L' ],
    [ '3 ', '3 ', '2I', '3 ', '1 ', '3 ', '2I', '2L', '1 ', '2L' ],
    [ '1 ', '1 ', '3 ', '2I', '3 ', '2L', '1 ', '1 ', '2L', '2L' ],
    [ '1 ', '1 ', '3 ', '1 ', '1 ', '1 ', '3 ', '3 ', '3 ', '2L' ],
    [ '3 ', '2I', '3 ', '3 ', '2L', '3 ', '3 ', '2I', '2L', '1 ' ],
    [ '1 ', '1 ', '3 ', '3 ', '3 ', '3 ', '1 ', '2L', '3 ', '2L' ],
    [ '1 ', '2I', '3 ', '2I', '1 ', '1 ', '1 ', '3 ', '1 ', '1 ' ],
])
binst = solver.Board(board=board)
solutions = binst.solve_and_print()
```

**Script Output**

```python
Solution found
    0   0   0   0   0   0   0   0   0   0  
    0   1   2   3   4   5   6   7   8   9

 0  O───┬───┬───┬───O   O───┐   ┌───────O
        │   │   │           │   │
 1  O   O   O   ├───────O   │   ├───────O
    │           │           │   │
 2  │   O   O───┴───┐   O───┤   │   O   O
    │   │           │       │   │   │   │
 3  │   │   O───┬───┴───┬───┘   ├───┴───┘
    │   │       │       │       │
 4  ├───┴───────┴───O   ├───────┘   O───┐
    │                   │               │
 5  O   O───┬───────┬───┘   O   O   ┌───┘
            │       │       │   │   │
 6  O   O───┤   O   O   O   ├───┴───┴───┐
    │       │   │       │   │           │
 7  ├───────┴───┤   ┌───┴───┴───────┐   O
    │           │   │               │
 8  O   O───┬───┴───┴───┬───O   ┌───┴───┐
            │           │       │       │
 9  O───────┴───────O   O   O───┴───O   O

Solutions found: 1
status: OPTIMAL
Time taken: 5.65 seconds
```

**Solved puzzle**

<img src="https://raw.githubusercontent.com/Ar-Kareem/puzzle_solver/master/images/pipes_solved.png" alt="Pipes solved" width="500">
