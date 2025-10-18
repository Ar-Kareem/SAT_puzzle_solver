# Tracks (Puzzle Type #16)

This is a dedicated solver for Tracks

Below are the details of how to utilize the solver. In addition, the solver gives all possible solutions to the input thus it can be utilized to figure out if a single partial input board has multiple possible solutions.

(The solver under the hood mainly utilizes the CP-SAT solver from Google OR-Tools)

* [**Play online**](https://www.chiark.greenend.org.uk/~sgtatham/puzzles/js/tracks.html)

* [**Instructions**](https://www.chiark.greenend.org.uk/~sgtatham/puzzles/doc/tracks.html#tracks)

Complete the track from A to B so that the rows and columns contain the same number of track segments as are indicated in the clues to the top and right of the grid. There are only straight and 90-degree curved rail sections, and the track may not cross itself. 

(Note: The solver for this puzzle is slightly slower and could take several seconds to solve a large 15x15 puzzle)

**Unsolved puzzle**

<img src="../images/tracks_unsolved.png" alt="Tracks unsolved" width="500">

Code to utilize this package and solve the puzzle:
```python
import numpy as np
from puzzle_solver import tracks_solver as solver
board = np.array([
  ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', 'LD', '  ', '  ', ], 
  ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', 'LD', '  ', '  ', '  ', '  ', ], 
  ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', ], 
  ['  ', '  ', '  ', '  ', '  ', 'LD', 'UD', 'DR', '  ', '  ', '  ', '  ', '  ', '  ', '  ', ], 
  ['DR', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', ], 
  ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', 'DR', '  ', '  ', ], 
  ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', 'DR', '  ', '  ', '  ', '  ', '  ', '  ', ], 
  ['  ', '  ', 'UL', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', ], 
  ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', 'LR', '  ', '  ', '  ', '  ', ], 
  ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', 'LD', '  ', '  ', '  ', 'UD', ], 
  ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', 'UR', '  ', '  ', '  ', '  ', 'UD', 'UD', ], 
  ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', 'LR', '  ', '  ', '  ', '  ', '  ', ], 
  ['UL', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', 'LR', 'LR', '  ', '  ', '  ', ], 
  ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', ], 
  ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', 'DR', '  ', ], 
])
side = np.array([9, 7, 7, 7, 11, 10, 9, 8, 9, 10, 7, 9, 9, 2, 2])
top = np.array([6, 5, 7, 3, 3, 2, 7, 8, 13, 8, 9, 8, 10, 13, 14])
binst = solver.Board(board=board, top=top, side=side)
solutions = binst.solve_and_print()
```
**Script Output**
```
[['  ' '  ' '  ' '  ' '  ' '  ' '┏━' '━━' '━━' '━━' '━━' '━━' '━┒' '┏━' '━┒']
 ['  ' '  ' '  ' '  ' '  ' '  ' '┃ ' '  ' '┏━' '━━' '━┒' '  ' '┗━' '━┛' '┃ ']
 ['  ' '  ' '  ' '  ' '  ' '  ' '┃ ' '  ' '┃ ' '  ' '┗━' '━━' '━━' '━━' '━┛']
 ['  ' '  ' '┏━' '━┒' '┏━' '━┒' '┃ ' '┏━' '━┛' '  ' '  ' '  ' '  ' '  ' '  ']
 ['┏━' '━━' '━┛' '┃ ' '┃ ' '┗━' '━┛' '┗━' '━┒' '  ' '  ' '  ' '  ' '┏━' '━┒']
 ['┗━' '━━' '━┒' '┗━' '━┛' '  ' '  ' '┏━' '━┛' '  ' '  ' '  ' '┏━' '━┛' '┃ ']
 ['  ' '  ' '┃ ' '  ' '  ' '  ' '┏━' '━┛' '┏━' '━━' '━━' '━━' '━┛' '  ' '┃ ']
 ['  ' '┏━' '━┛' '  ' '  ' '  ' '┗━' '━━' '━┛' '  ' '  ' '  ' '┏━' '━━' '━┛']
 ['  ' '┗━' '━┒' '  ' '  ' '  ' '  ' '  ' '┏━' '━━' '━━' '━┒' '┃ ' '┏━' '━┒']
 ['┏━' '━━' '━┛' '  ' '  ' '  ' '  ' '  ' '┃ ' '┏━' '━┒' '┗━' '━┛' '┃ ' '┃ ']
 ['┃ ' '  ' '  ' '  ' '  ' '  ' '  ' '  ' '┗━' '━┛' '┗━' '━┒' '  ' '┃ ' '┃ ']
 ['┃ ' '  ' '  ' '  ' '  ' '  ' '  ' '┏━' '━━' '━━' '━━' '━┛' '┏━' '━┛' '┃ ']
 ['━┛' '  ' '  ' '  ' '  ' '  ' '  ' '┗━' '━━' '━━' '━━' '━━' '━┛' '┏━' '━┛']
 ['  ' '  ' '  ' '  ' '  ' '  ' '  ' '  ' '  ' '  ' '  ' '  ' '  ' '┗━' '━┒']
 ['  ' '  ' '  ' '  ' '  ' '  ' '  ' '  ' '  ' '  ' '  ' '  ' '  ' '┏━' '━┛']]
Solutions found: 1
status: OPTIMAL
Time taken: 9.42 seconds
```

**Solved puzzle**

<img src="../images/tracks_solved.png" alt="Tracks solved" width="500">
