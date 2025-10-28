# Connect the Dots (Puzzle Type #56)

* [**Mobile App (Android)**](https://play.google.com/store/apps/details?id=com.playvalve.connect.dots&hl=en_US)

* [**Mobile App (iOS)**](https://apps.apple.com/us/app/dot-link-connect-the-dots/id6444312485)

You are given a grid of empty cells and 2 filled cell per color. The goal is to connect the dots of the same color to form a single fully connected graph for each color.

**Unsolved puzzle**

<img src="https://raw.githubusercontent.com/Ar-Kareem/puzzle_solver/master/images/connect_the_dots_unsolved.png" alt="Connect the Dots unsolved" width="500">

Code to utilize this package and solve the puzzle:

```python
import numpy as np
from puzzle_solver import connect_the_dots_solver as solver
board = np.array([
    ['R', ' ', 'B', ' ', ' ', ' ', ' ', ' '],
    ['Y', ' ', ' ', 'R', 'G', ' ', 'G', ' '],
    [' ', 'M', ' ', ' ', ' ', 'P', ' ', ' '],
    [' ', 'O', ' ', ' ', ' ', 'M', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    ['Br', 'B', ' ', ' ', 'Y', 'O', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', 'P', ' ', ' '],
    [' ', ' ', ' ', 'Br', ' ', ' ', ' ', ' '],
])
binst = solver.Board(board=board)
solutions = binst.solve_and_print()
```

**Script Output**

```python
Solution found
    0   1   2   3   4   5   6   7
  ┌───────┬───────────────────────┐
 0│ R   R │ B   B   B   B   B   B │
  ├───┐   └───────┬───────────┐   │
 1│ Y │ R   R   R │ G   G   G │ B │
  │   ├───────────┴───┬───────┤   │
 2│ Y │ M   M   M   M │ P   P │ B │
  │   ├───────────┐   └───┐   │   │
 3│ Y │ O   O   O │ M   M │ P │ B │
  │   └───────┐   └───────┤   │   │
 4│ Y   Y   Y │ O   O   O │ P │ B │
  ├───┬───┐   └───────┐   │   │   │
 5│Br │ B │ Y   Y   Y │ O │ P │ B │
  │   │   └───────────┼───┘   │   │
 6│Br │ B   B   B   B │ P   P │ B │
  │   └───────────┐   └───────┘   │
 7│Br  Br  Br  Br │ B   B   B   B │
  └───────────────┴───────────────┘
Solutions found: 1
status: OPTIMAL
Time taken: 2.91 seconds
```

**Solved puzzle**

<img src="https://raw.githubusercontent.com/Ar-Kareem/puzzle_solver/master/images/connect_the_dots_solved.png" alt="Connect the Dots solved" width="500">
