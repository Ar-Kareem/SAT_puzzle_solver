
# Galaxies (Puzzle Type #35)

* [**Play online**](https://www.chiark.greenend.org.uk/~sgtatham/puzzles/js/galaxies.html)

* [**Instructions**](https://www.chiark.greenend.org.uk/~sgtatham/puzzles/doc/galaxies.html#galaxies)

You have a rectangular grid containing a number of dots. Your aim is to partition the rectangle into connected regions of squares, in such a way that every region is 180° rotationally symmetric, and contains exactly one dot which is located at its centre of symmetry.

To enter your solution, you draw lines along the grid edges to mark the boundaries of the regions. The puzzle is complete when the marked lines on the grid are precisely those that separate two squares belonging to different regions.

**Unsolved puzzle**

<img src="https://raw.githubusercontent.com/Ar-Kareem/puzzle_solver/master/images/galaxies_unsolved.png" alt="Galaxies unsolved" width="500">

Code to utilize this package and solve the puzzle:

Note: The number are arbitrary and simply number each galaxy as an integer.

```python
import numpy as np
from puzzle_solver import galaxies_solver as solver
galaxies = np.array([
    ['  ', '  ', '00', '  ', '  ', '01', '01', '02', '02', '03', '03', '  ', '04', '04', '  '],
    ['05', '05', '  ', '  ', '06', '01', '01', '02', '02', '  ', '  ', '  ', '07', '  ', '  '],
    ['08', '  ', '  ', '  ', '06', '  ', '09', '09', '  ', '  ', '10', '  ', '  ', '  ', '  '],
    ['  ', '  ', '  ', '  ', '  ', '  ', '11', '11', '12', '  ', '  ', '  ', '  ', '13', '13'],
    ['14', '  ', '  ', '  ', '15', '  ', '11', '11', '  ', '  ', '  ', '  ', '16', '  ', '  '],
    ['  ', '17', '  ', '  ', '15', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '16', '  ', '18'],
    ['  ', '17', '19', '  ', '  ', '  ', '  ', '  ', '  ', '20', '  ', '  ', '  ', '21', '18'],
    ['  ', '22', '  ', '  ', '23', '  ', '  ', '  ', '  ', '20', '  ', '24', '24', '21', '25'],
    ['26', '27', '27', '28', '28', '29', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '30', '30'],
    ['  ', '27', '27', '28', '28', '31', '31', '  ', '  ', '  ', '  ', '32', '  ', '30', '30'],
    ['  ', '  ', '  ', '33', '33', '31', '31', '34', '  ', '  ', '35', '  ', '  ', '  ', '  '],
    ['36', '  ', '  ', '33', '33', '  ', '  ', '34', '  ', '  ', '  ', '  ', '  ', '37', '  '],
    ['  ', '  ', '38', '38', '  ', '39', '  ', '40', '40', '41', '41', '42', '  ', '37', '  '],
    ['43', '44', '38', '38', '45', '45', '46', '40', '40', '41', '41', '42', '  ', '  ', '  '],
    ['43', '  ', '  ', '  ', '  ', '  ', '  ', '47', '  ', '  ', '  ', '  ', '48', '48', '  ']
])
binst = solver.Board(galaxies=galaxies)
solutions = binst.solve_and_print()
```
**Script Output**

As the instructions say, the solution to this puzzle is not garunteed to be unique.

```python
Solution found
    0   0   0   0   0   0   0   0   0   0   1   1   1   1   1  
    0   1   2   3   4   5   6   7   8   9   0   1   2   3   4
  ┌───────────────────┬───────┬───────┬───────┬───────────────┐
 0│         .         │ .   . │ .   . │ .   . │     .   .     │
  ├───────┬───┬───────┤       │       ├───────┼───────────┬───┤
 1│ .   . │   │     . │ .   . │ .   . │       │     .     │   │
  ├───┬───┘   └───┐   └───┬───┴───┬───┘       └───────┬───┘   │
 2│ . │           │ .     │ .   . │         .         │       │
  ├───┤           └───────┼───────┼───┬───┐       ┌───┤       │
 3│   │                   │ .   . │ . │   │       │   │ .   . │
  │   │                   │       ├───┘   └───────┤   │       │
 4│ . │             .     │ .   . │               │ . │       │
  │   ├───────┐           └───────┤               │   │   ┌───┤
 5│   │ .     │     .             │               │ . │   │ . │
  ├───┘   ┌───┤                   │           ┌───┤   ├───┤   │
 6│     . │ . │                   │     .     │   │   │ . │ . │
  ├───┬───┼───┴───┬───┐           │           │   └───┤   ├───┤
 7│   │ . │       │ . │           │     .     │ .   . │ . │ . │
  │   ├───┘   ┌───┴───┼───┐   ┌───┘           ├───┐   ├───┴───┤
 8│ . │ .   . │ .   . │ . │   │               │   │   │ .   . │
  │   │       │       ├───┴───┤               │   ├───┤       │
 9│   │ .   . │ .   . │ .   . │               │ . │   │ .   . │
  ├───┘   ┌───┴───────┤       ├───────┐   ┌───┤   │   └───────┤
10│       │     .   . │ .   . │ .     │   │ . │   │           │
  ├───┬───┴───┐       └───┬───┘   ┌───┴───┴───┴───┤           │
11│ . │       │ .   .     │     . │               │     .     │
  ├───┴───┐   └───┬───┬───┼───┬───┴───┐       ┌───┤           │
12│       │ .   . │   │ . │   │ .   . │ .   . │ . │     .     │
  ├───┐   │       │   └───┤   │       │       │   │           │
13│ . │ . │ .   . │ .   . │ . │ .   . │ .   . │ . │           │
  │   │   └───┐   └───┐   │   ├───┬───┘       └───┼───────┐   │
14│ . │       │       │   │   │ . │               │ .   . │   │
  └───┴───────┴───────┴───┴───┴───┴───────────────┴───────┴───┘
Solutions found: 1
status: OPTIMAL
Time taken: 0.06 seconds
```

**Solved puzzle**

Applying the solution to the puzzle visually:

<img src="https://raw.githubusercontent.com/Ar-Kareem/puzzle_solver/master/images/galaxies_solved.png" alt="Galaxies solved" width="500">
