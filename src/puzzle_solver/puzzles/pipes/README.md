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
[['R' 'DLR' 'DLR' 'DLR' 'L' 'R' 'DL' 'DR' 'LR' 'L']
 ['D' 'U' 'U' 'UDR' 'LR' 'L' 'UD' 'UDR' 'LR' 'L']
 ['UD' 'D' 'R' 'ULR' 'DL' 'R' 'UDL' 'UD' 'D' 'D']
 ['UD' 'UD' 'R' 'DLR' 'ULR' 'DLR' 'UL' 'UDR' 'ULR' 'UL']
 ['UDR' 'ULR' 'LR' 'ULR' 'L' 'UDR' 'LR' 'UL' 'R' 'DL']
 ['U' 'R' 'DLR' 'LR' 'DLR' 'UL' 'D' 'D' 'DR' 'UL']
 ['D' 'R' 'UDL' 'D' 'U' 'D' 'UDR' 'ULR' 'ULR' 'DL']
 ['UDR' 'LR' 'ULR' 'UDL' 'DR' 'ULR' 'ULR' 'LR' 'DL' 'U']
 ['U' 'R' 'DLR' 'ULR' 'ULR' 'DLR' 'L' 'DR' 'ULR' 'DL']
 ['R' 'LR' 'ULR' 'LR' 'L' 'U' 'R' 'ULR' 'L' 'U']]
Solutions found: 1
status: OPTIMAL
Time taken: 5.65 seconds
```

**Solved puzzle**

<img src="https://raw.githubusercontent.com/Ar-Kareem/puzzle_solver/master/images/pipes_solved.png" alt="Pipes solved" width="500">
