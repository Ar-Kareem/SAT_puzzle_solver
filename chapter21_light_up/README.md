# Light Up (Puzzle Type #3)

This is a dedicated solver for Light Up

Below are the details of how to utilize the solver. In addition, the solver gives all possible solutions to the input thus it can be utilized to figure out if a single partial input board has multiple possible solutions.

(The solver mainly utilizes the CP-SAT solver from Google OR-Tools)

* [**Play online**](https://www.chiark.greenend.org.uk/~sgtatham/puzzles/js/lightup.html)

* [**Instructions**](https://www.chiark.greenend.org.uk/~sgtatham/puzzles/doc/lightup.html#lightup)

You have a grid of squares. Some are filled in black; some of the black squares are numbered. Your aim is to ‘light up’ all the empty squares by placing light bulbs in some of them.

Each light bulb illuminates the square it is on, plus all squares in line with it horizontally or vertically unless a black square is blocking the way.

To win the game, you must satisfy the following conditions:

  - All non-black squares are lit.
  - No light is lit by another light.
  - All numbered black squares have exactly that number of lights adjacent to them (in the four squares above, below, and to the side).

Non-numbered black squares may have any number of lights adjacent to them. 

**Unsolved puzzle**

<img src="../images/lightup_unsolved.png" alt="Light Up unsolved" width="500">

Code to utilize this package and solve the puzzle:
```python
import numpy as np
from . import solver
bor = np.array([
  ['*', '0', '*', '*', '*', '*', 'W', '*', '*', '*'],
  ['*', '*', '*', '0', '*', '*', '*', '*', '*', '1'],
  ['W', '*', 'W', '*', '*', 'W', '*', '*', '0', '*'],
  ['0', '*', '*', '*', '3', '*', 'W', '*', '0', '*'],
  ['*', '*', '*', '*', 'W', '*', '2', '*', 'W', '*'],
  ['*', '1', '*', 'W', '*', '2', '*', '*', '*', '*'],
  ['*', '0', '*', 'W', '*', 'W', '*', '*', '*', 'W'],
  ['*', '0', '*', '*', '1', '*', '*', '2', '*', 'W'],
  ['0', '*', '*', '*', '*', '*', '1', '*', '*', '*'],
  ['*', '*', '*', '2', '*', '*', '*', '*', 'W', '*'],
])  # W is wall, * is space, # is number

binst = solver.Board(board=bor)
solutions = binst.solve_and_print()
```
**Script Output**
```
Solution found
[[' ' '0' ' ' ' ' ' ' 'L' 'W' ' ' ' ' 'L']
 ['L' ' ' ' ' '0' ' ' ' ' 'L' ' ' ' ' '1']
 ['W' 'L' 'W' ' ' 'L' 'W' ' ' ' ' '0' ' ']
 ['0' ' ' ' ' 'L' '3' 'L' 'W' ' ' '0' ' ']
 [' ' ' ' 'L' ' ' 'W' ' ' '2' 'L' 'W' 'L']
 ['L' '1' ' ' 'W' 'L' '2' 'L' ' ' ' ' ' ']
 [' ' '0' ' ' 'W' ' ' 'W' ' ' ' ' ' ' 'W']
 [' ' '0' ' ' ' ' '1' 'L' ' ' '2' 'L' 'W']
 ['0' ' ' ' ' 'L' ' ' ' ' '1' 'L' ' ' ' ']
 [' ' 'L' ' ' '2' 'L' ' ' ' ' ' ' 'W' 'L']]
Solutions found: 1
status: OPTIMAL
Time taken: 0.01 seconds
```

**Solved puzzle**

Which exactly matches the true solutions (Remember, the goal of the puzzle is to find where to place the lights, marked as 'L' in the solution above):

<img src="../images/lightup_solved.png" alt="Light Up solved" width="500">
