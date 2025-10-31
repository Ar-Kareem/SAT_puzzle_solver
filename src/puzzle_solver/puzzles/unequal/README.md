# Unequal (Puzzle Type #37)

Also called "Futoshiki", the "Adjacent" variant is also known as "Renzoku" or "Neighbours".

* [**Play online 1**](https://www.chiark.greenend.org.uk/~sgtatham/puzzles/js/unequal.html)

* [**Play online 2**](https://www.puzzle-futoshiki.com/futoshiki-4x4-easy/) (Futoshiki variant)

* [**Play online 3**](https://www.puzzle-futoshiki.com/renzoku-4x4-easy/) (Renzoku variant)

* [**Instructions**](https://www.chiark.greenend.org.uk/~sgtatham/puzzles/doc/unequal.html#unequal)

 You have a square grid; each square may contain a digit from 1 to the size of the grid, and some squares have clue signs between them. Your aim is to fully populate the grid with numbers such that:

  - Each row contains only one occurrence of each digit
  - Each column contains only one occurrence of each digit
  - All the clue signs are satisfied.

There are two modes for this game, 'Unequal' and 'Adjacent'.

In 'Unequal' mode, the clue signs are greater-than symbols indicating one square's value is greater than its neighbour's. In this mode not all clues may be visible, particularly at higher difficulty levels.

In 'Adjacent' mode, the clue signs are bars indicating one square's value is numerically adjacent (i.e. one higher or one lower) than its neighbour. In this mode all clues are always visible: absence of a bar thus means that a square's value is definitely not numerically adjacent to that neighbour's.

In 'Trivial' difficulty level (available via the 'Custom' game type selector), there are no greater-than signs in 'Unequal' mode; the puzzle is to solve the Latin square only. 

**Unsolved puzzle**

<img src="https://raw.githubusercontent.com/Ar-Kareem/puzzle_solver/master/images/puzzles/unequal_unsolved.png" alt="Unequal unsolved" width="500">

Code to utilize this package and solve the puzzle:

Note: For an NxM board you need an (2N-1)x(2M-1) array because the puzzle involves input in between the cells. Each numbered cell has neighbors horizontally to represent ">", "<", and "|" (where "|" represents adjacency) and vertically to represent "∧", "∨" and "-" (where "-" represents adjacency). The "X" in the input are unused corners that shouldnt contain anything (just a corner). The numbers should never appear orthogonal to an "X", only diagonally to it. vice-versa for the comparison operators.

```python
import numpy as np
from puzzle_solver import unequal_solver as solver
board = np.array([
    [' ', ' ', ' ', ' ', '9', ' ', '1', ' ', '7', '>', ' ', '>', ' ', ' ', ' ', ' ', ' ', '>', ' '],
    [' ', 'X', 'V', 'X', ' ', 'X', ' ', 'X', ' ', 'X', ' ', 'X', '∧', 'X', ' ', 'X', ' ', 'X', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', '6', ' ', ' ', ' ', '9', ' ', ' ', ' ', '5', ' ', '3', ' ', ' '],
    [' ', 'X', ' ', 'X', '∧', 'X', ' ', 'X', '∧', 'X', ' ', 'X', ' ', 'X', ' ', 'X', ' ', 'X', ' '],
    [' ', ' ', ' ', '>', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '6', ' ', '9', ' ', ' ', ' ', ' '],
    [' ', 'X', ' ', 'X', 'V', 'X', 'V', 'X', 'V', 'X', ' ', 'X', ' ', 'X', ' ', 'X', ' ', 'X', 'V'],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '<', ' ', '<', ' ', '>', ' ', ' ', ' ', ' ', ' '],
    [' ', 'X', ' ', 'X', '∧', 'X', 'V', 'X', ' ', 'X', ' ', 'X', ' ', 'X', ' ', 'X', ' ', 'X', ' '],
    [' ', ' ', '3', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '<', ' ', ' ', ' '],
    [' ', 'X', ' ', 'X', ' ', 'X', ' ', 'X', '∧', 'X', ' ', 'X', ' ', 'X', ' ', 'X', ' ', 'X', ' '],
    [' ', '<', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '5', ' ', ' ', '>', ' ', '<', ' ', ' ', '4'],
    ['V', 'X', '∧', 'X', 'V', 'X', ' ', 'X', ' ', 'X', ' ', 'X', ' ', 'X', 'V', 'X', ' ', 'X', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '>', ' ', ' ', ' ', ' ', ' '],
    [' ', 'X', ' ', 'X', ' ', 'X', ' ', 'X', ' ', 'X', ' ', 'X', '∧', 'X', ' ', 'X', ' ', 'X', 'V'],
    [' ', ' ', ' ', '<', ' ', ' ', ' ', '<', ' ', ' ', ' ', '<', ' ', '<', ' ', ' ', ' ', '<', ' '],
    [' ', 'X', ' ', 'X', ' ', 'X', 'V', 'X', ' ', 'X', 'V', 'X', '∧', 'X', ' ', 'X', ' ', 'X', ' '],
    [' ', ' ', ' ', ' ', ' ', '>', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '>', ' ', ' ', '9', ' ', ' '],
    ['V', 'X', ' ', 'X', ' ', 'X', ' ', 'X', ' ', 'X', ' ', 'X', ' ', 'X', ' ', 'X', ' ', 'X', 'V'],
    [' ', '>', ' ', ' ', ' ', '>', ' ', ' ', ' ', ' ', '4', '<', ' ', '<', ' ', '<', '7', ' ', '2'],
])
binst = solver.Board(board=board)
solutions = binst.solve_and_print()
```
**Script Output**

```python
Solution found
[
    [ 6 5 9 1 7 2 0 8 4 3 ]
    [ 7 1 0 6 4 9 2 5 3 8 ]
    [ 3 4 2 8 5 0 6 9 1 7 ]
    [ 5 9 1 7 3 6 8 4 2 0 ]
    [ 8 3 5 4 0 7 1 2 6 9 ]
    [ 2 6 7 0 1 5 9 3 8 4 ]
    [ 0 7 4 9 2 8 3 1 5 6 ]
    [ 9 2 6 5 8 3 4 7 0 1 ]
    [ 4 8 3 2 6 1 7 0 9 5 ]
    [ 1 0 8 3 9 4 5 6 7 2 ]
]
Solutions found: 1
status: OPTIMAL
Time taken: 0.05 seconds
```

**Solved puzzle**

Applying the solution to the puzzle visually:

<img src="https://raw.githubusercontent.com/Ar-Kareem/puzzle_solver/master/images/puzzles/unequal_solved.png" alt="Unequal solved" width="500">
