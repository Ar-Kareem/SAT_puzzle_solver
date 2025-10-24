# Flip (Puzzle Type #44)

* [**Play online**](https://www.chiark.greenend.org.uk/~sgtatham/puzzles/js/flip.html)

* [**Instructions**](https://www.chiark.greenend.org.uk/~sgtatham/puzzles/doc/flip.html#flip)

You have a grid of squares, some light and some dark. Your aim is to light all the squares up at the same time. You can choose any square and flip its state from light to dark or dark to light, but when you do so, other squares around it change state as well. 

**Unsolved puzzle**

<img src="https://raw.githubusercontent.com/Ar-Kareem/puzzle_solver/master/images/flip_unsolved.png" alt="Flip unsolved" width="500">

Code to utilize this package and solve the puzzle:

(Note: the solver also supports random mapping of squares to the neighbors they flip, see the test cases in `tests/test_flip.py` for usage examples)

```python
import numpy as np
from puzzle_solver import flip_solver as solver
board = np.array([
    ['B', 'W', 'W', 'W', 'W', 'W', 'W'],
    ['B', 'B', 'W', 'W', 'W', 'B', 'B'],
    ['W', 'B', 'W', 'W', 'B', 'B', 'W'],
    ['B', 'B', 'B', 'W', 'W', 'B', 'W'],
    ['W', 'W', 'B', 'B', 'W', 'B', 'W'],
    ['B', 'W', 'B', 'B', 'W', 'W', 'W'],
    ['B', 'W', 'B', 'W', 'W', 'B', 'B'],
])
binst = solver.Board(board=board)
solutions = binst.solve_and_print()
```

**Script Output**

The output tells you which squares to tap to solve the puzzle.

```python
Solution found
[['T' ' ' 'T' 'T' 'T' ' ' ' ']
 [' ' ' ' ' ' 'T' ' ' 'T' ' ']
 [' ' 'T' ' ' ' ' 'T' ' ' ' ']
 ['T' ' ' 'T' ' ' ' ' 'T' ' ']
 [' ' ' ' ' ' 'T' ' ' ' ' 'T']
 ['T' ' ' 'T' ' ' 'T' 'T' 'T']
 [' ' ' ' ' ' ' ' ' ' 'T' 'T']]
Solutions found: 1
status: OPTIMAL
```

**Solved puzzle**

This picture won't mean much as the game is about the sequence of moves not the final frame as shown here.

<img src="https://raw.githubusercontent.com/Ar-Kareem/puzzle_solver/master/images/flip_solved.png" alt="Flip solved" width="500">
