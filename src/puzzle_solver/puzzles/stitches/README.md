# Stitches (Puzzle Type #28)

* [**Play online**](https://www.puzzle-stitches.com/)

- Connect each block with ALL its neighbor blocks with exactly 1 "stitch" each.
- A "stitch" connects 2 orthogonally adjacent cells from different blocks.
- 2 stitches cannot share a hole.
- The clues outside the grid indicate the number of holes on that row/column
- For 2÷ puzzles, you have to use 2 stitches to connect neighbor blocks, for 3÷ puzzles - 3 stitches etc.

**Unsolved puzzle**

<img src="https://raw.githubusercontent.com/Ar-Kareem/puzzle_solver/master/images/stitches_unsolved.png" alt="Stitches unsolved" width="500">

Code to utilize this package and solve the puzzle:

```python
import numpy as np
from puzzle_solver import stitches_solver as solver
board = np.array([
  ["00", "00", "00", "00", "00", "01", "01", "01", "01", "01", "01", "01", "01", "02", "02"],
  ["00", "03", "03", "04", "00", "00", "01", "05", "05", "05", "05", "05", "01", "01", "02"],
  ["00", "03", "04", "04", "04", "00", "05", "05", "05", "05", "05", "05", "05", "05", "02"],
  ["00", "03", "04", "04", "04", "04", "05", "05", "06", "05", "02", "02", "02", "02", "02"],
  ["07", "03", "03", "03", "03", "04", "06", "06", "06", "06", "06", "06", "06", "02", "02"],
  ["07", "07", "07", "03", "03", "04", "04", "06", "08", "08", "08", "06", "02", "02", "02"],
  ["07", "07", "03", "03", "03", "04", "04", "08", "08", "08", "08", "06", "06", "06", "02"],
  ["07", "07", "07", "07", "07", "08", "08", "08", "09", "09", "08", "06", "08", "06", "02"],
  ["10", "10", "07", "07", "09", "09", "09", "09", "09", "09", "08", "08", "08", "11", "02"],
  ["10", "10", "07", "09", "09", "09", "09", "09", "09", "09", "09", "08", "08", "11", "02"],
  ["10", "09", "09", "09", "12", "12", "12", "13", "09", "09", "11", "11", "11", "11", "11"],
  ["10", "10", "10", "09", "12", "12", "12", "13", "09", "11", "11", "11", "13", "13", "11"],
  ["14", "15", "10", "12", "12", "16", "17", "13", "13", "11", "13", "13", "13", "13", "11"],
  ["14", "15", "10", "12", "16", "16", "17", "17", "13", "13", "13", "13", "13", "13", "11"],
  ["14", "15", "15", "12", "16", "16", "17", "17", "17", "17", "17", "13", "13", "13", "13"]
])
top = np.array([6, 6, 9, 5, 3, 8, 9, 3, 1, 4, 4, 1, 4, 8, 5])
side = np.array([0, 10, 6, 4, 4, 1, 5, 8, 2, 6, 5, 11, 4, 3, 7])
binst = solver.Board(board=board, top=top, side=side)
solutions = binst.solve_and_print()
```

Note: `solver.Board` accepts an optional `connection_count=N` parameter to specify the (÷N) stitches puzzle (by default, 1 stitch).

**Script Output**

```python
Solution found
[[' ' ' ' ' ' ' ' ' ' ' ' ' ' ' ' ' ' ' ' ' ' ' ' ' ' ' ' ' ']
 ['R' 'L' 'D' 'R' 'L' 'R' 'L' ' ' ' ' ' ' ' ' ' ' 'D' 'R' 'L']
 [' ' ' ' 'U' ' ' ' ' 'R' 'L' ' ' ' ' ' ' ' ' ' ' 'U' 'R' 'L']
 ['D' ' ' ' ' ' ' ' ' 'R' 'L' ' ' ' ' 'D' ' ' ' ' ' ' ' ' ' ']
 ['U' ' ' ' ' ' ' ' ' 'R' 'L' ' ' ' ' 'U' ' ' ' ' ' ' ' ' ' ']
 [' ' ' ' ' ' ' ' ' ' ' ' ' ' ' ' ' ' ' ' ' ' ' ' ' ' 'D' ' ']
 [' ' ' ' 'D' ' ' ' ' ' ' 'R' 'L' ' ' 'D' ' ' ' ' ' ' 'U' ' ']
 [' ' 'D' 'U' ' ' 'R' 'L' ' ' ' ' ' ' 'U' ' ' 'R' 'L' 'D' ' ']
 [' ' 'U' ' ' ' ' ' ' ' ' ' ' ' ' ' ' ' ' ' ' ' ' ' ' 'U' ' ']
 [' ' ' ' 'R' 'L' ' ' ' ' ' ' ' ' ' ' ' ' 'D' ' ' 'R' 'L' 'D']
 [' ' ' ' 'D' ' ' ' ' ' ' 'R' 'L' ' ' ' ' 'U' ' ' ' ' ' ' 'U']
 ['D' 'D' 'U' 'R' 'L' 'D' 'D' 'R' 'L' ' ' ' ' ' ' ' ' 'R' 'L']
 ['U' 'U' ' ' ' ' ' ' 'U' 'U' ' ' ' ' ' ' ' ' ' ' ' ' ' ' ' ']
 [' ' ' ' 'R' 'L' ' ' ' ' ' ' ' ' ' ' ' ' 'D' ' ' ' ' ' ' ' ']
 ['R' 'L' 'R' 'L' ' ' 'R' 'L' ' ' ' ' ' ' 'U' ' ' ' ' ' ' ' ']]
Solutions found: 1
status: OPTIMAL
Time taken: 0.01 seconds
```

**Solved puzzle**

<img src="https://raw.githubusercontent.com/Ar-Kareem/puzzle_solver/master/images/stitches_solved.png" alt="Stitches solved" width="500">
