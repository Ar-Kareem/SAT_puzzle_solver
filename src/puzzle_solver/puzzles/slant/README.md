# Slant (Puzzle Type #36)

* [**Play online**](https://www.chiark.greenend.org.uk/~sgtatham/puzzles/js/slant.html)

* [**Instructions**](https://www.chiark.greenend.org.uk/~sgtatham/puzzles/doc/slant.html#slant)

You have a grid of squares. Your aim is to draw a diagonal line through each square, and choose which way each line slants so that the following conditions are met:

   - The diagonal lines never form a loop.
   - Any point with a circled number has precisely that many lines meeting at it. (Thus, a 4 is the centre of a cross shape, whereas a zero is the centre of a diamond shape – or rather, a partial diamond shape, because a zero can never appear in the middle of the grid because that would immediately cause a loop.)

**Unsolved puzzle**

<img src="https://raw.githubusercontent.com/Ar-Kareem/puzzle_solver/master/images/slant_unsolved.png" alt="Slant unsolved" width="500">

Code to utilize this package and solve the puzzle:

Note: For an NxM board you need an (N+1)x(M+1) array because the puzzle is to solve for the cells while the input is the values at the corners (there's always one more corner than cells in each dimension).

```python
from puzzle_solver import slant_solver as solver
board = np.array([
    [' ', ' ', '1', ' ', '1', ' ', '1', ' ', '1', ' ', ' ', ' ', ' '],
    [' ', '1', '2', ' ', ' ', '2', ' ', '2', ' ', '2', ' ', '1', '1'],
    [' ', '2', '2', ' ', '2', '3', '2', ' ', '3', ' ', ' ', '1', ' '],
    ['1', '1', ' ', '3', '1', '2', ' ', '1', ' ', ' ', '3', ' ', ' '],
    [' ', ' ', '1', '1', ' ', ' ', ' ', '1', '1', '3', ' ', '3', ' '],
    ['1', '2', ' ', '2', '2', ' ', '2', ' ', ' ', '1', '2', ' ', ' '],
    [' ', '2', '2', '2', ' ', ' ', '2', '3', '2', ' ', ' ', ' ', ' '],
    [' ', '1', '2', ' ', ' ', '2', ' ', '2', ' ', ' ', ' ', '1', ' '],
    [' ', ' ', ' ', '3', '2', '2', ' ', '3', '1', ' ', ' ', ' ', '1'],
    [' ', '2', '1', '1', '2', ' ', '1', ' ', '1', ' ', '1', '1', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '1', ' ', ' '],
])
binst = solver.Board(numbers=board)
solutions = binst.solve_and_print()
```
**Script Output**

```python
Solution found
[
    [ / \ \ / / / / \ \ \ / \ ]
    [ \ \ \ \ \ \ / \ / / \ \ ]
    [ \ \ \ / / \ / \ \ \ \ / ]
    [ \ / \ \ / \ / / \ / \ / ]
    [ / \ \ / \ \ \ / / / \ \ ]
    [ / \ \ / \ \ \ / \ / \ \ ]
    [ / \ \ / \ / / / \ / / \ ]
    [ \ \ \ \ \ / / / \ / \ \ ]
    [ / / / \ \ / / \ \ / \ \ ]
    [ \ \ / / / \ / \ / \ \ / ]
]
Solutions found: 1
status: OPTIMAL
Time taken: 0.06 seconds
```

**Solved puzzle**

Applying the solution to the puzzle visually:

<img src="https://raw.githubusercontent.com/Ar-Kareem/puzzle_solver/master/images/slant_solved.png" alt="Slant solved" width="500">
