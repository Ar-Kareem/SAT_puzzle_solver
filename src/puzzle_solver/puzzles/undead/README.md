# UnDead (Puzzle Type #14)

This is a dedicated solver for UnDead

Below are the details of how to utilize the solver. In addition, the solver gives all possible solutions to the input thus it can be utilized to figure out if a single partial input board has multiple possible solutions.

(The solver under the hood mainly utilizes the CP-SAT solver from Google OR-Tools)

* [**Play online**](https://www.chiark.greenend.org.uk/~sgtatham/puzzles/js/undead.html)

* [**Instructions**](https://www.chiark.greenend.org.uk/~sgtatham/puzzles/doc/undead.html#undead)

You are given a grid of squares, some of which contain diagonal mirrors. Every square which is not a mirror must be filled with one of three types of undead monster: a ghost, a vampire, or a zombie.

Vampires can be seen directly, but are invisible when reflected in mirrors. Ghosts are the opposite way round: they can be seen in mirrors, but are invisible when looked at directly. Zombies are visible by any means.

You are also told the total number of each type of monster in the grid. Also around the edge of the grid are written numbers, which indicate how many monsters can be seen if you look into the grid along a row or column starting from that position. (The diagonal mirrors are reflective on both sides. If your reflected line of sight crosses the same monster more than once, the number will count it each time it is visible, not just once.) 

**Unsolved puzzle**

<img src="../images/undead_unsolved.png" alt="UnDead unsolved" width="500">

Code to utilize this package and solve the puzzle:
```python
import numpy as np
from puzzle_solver import undead_solver as solver
bor = np.array([
  ['**', '//', '**', '**', '**', '**', '\\'],
  ['**', '**', '**', '//', '**', '**', '**'],
  ['**', '//', '//', '**', '**', '\\', '//'],
  ['//', '\\', '//', '**', '//', '\\', '**'],
  ['//', '**', '//', '\\', '**', '//', '//'],
  ['**', '\\', '\\', '\\', '**', '**', '**'],
  ['**', '//', '**', '**', '**', '**', '**'],
])
t = np.array([3, 0, 3, 0, 5, 6, 0])
b = np.array([5, 2, 1, 3, 8, 2, 0])
r = np.array([0, 8, 0, 4, 2, 2, 4])
l = np.array([1, 4, 8, 0, 0, 2, 2])
counts = {Monster.GHOST: 5, Monster.VAMPIRE: 12, Monster.ZOMBIE: 11}

# create board and solve
binst = solver.Board(board=bor, sides={'top': t, 'bottom': b, 'right': r, 'left': l}, monster_count=counts)
solutions = binst.solve_and_print()
```
**Script Output**
```
Solution found
[['VA' '//' 'GH' 'GH' 'ZO' 'GH' '\\']
 ['VA' 'VA' 'VA' '//' 'ZO' 'ZO' 'ZO']
 ['VA' '//' '//' 'ZO' 'ZO' '\\' '//']
 ['//' '\\' '//' 'VA' '//' '\\' 'VA']
 ['//' 'VA' '//' '\\' 'ZO' '//' '//']
 ['ZO' '\\' '\\' '\\' 'ZO' 'VA' 'GH']
 ['ZO' '//' 'VA' 'VA' 'ZO' 'VA' 'GH']]
Solutions found: 1
status: OPTIMAL
Time taken: 0.01 seconds
```

**Solved puzzle**

<img src="../images/undead_solved.png" alt="UnDead solved" width="500">
