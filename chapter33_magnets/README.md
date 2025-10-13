# Magnets (Puzzle Type #4)

This is a dedicated solver for Magnets

Below are the details of how to utilize the solver. In addition, the solver gives all possible solutions to the input thus it can be utilized to figure out if a single output has multiple possible solutions.

(The solver mainly utilizes the CP-SAT solver from Google OR-Tools)

Game: https://www.chiark.greenend.org.uk/~sgtatham/puzzles/js/magnets.html

Instructions: https://www.chiark.greenend.org.uk/~sgtatham/puzzles/doc/magnets.html#magnets

Unsolved puzzle:

<img src="../images/magnets_unsolved.png" alt="Magnets unsolved" width="500">

Code to utilize this package and solve the puzzle:
```python
import numpy as np
import board
bor = np.array([
  ['H', 'H', 'H', 'H', 'V', 'V', 'V', 'V', 'H', 'H'],
  ['H', 'H', 'H', 'H', 'V', 'V', 'V', 'V', 'V', 'V'],
  ['H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'V', 'V'],
  ['V', 'V', 'V', 'H', 'H', 'H', 'H', 'H', 'H', 'V'],
  ['V', 'V', 'V', 'V', 'V', 'V', 'V', 'H', 'H', 'V'],
  ['V', 'H', 'H', 'V', 'V', 'V', 'V', 'V', 'V', 'V'],
  ['V', 'V', 'V', 'V', 'V', 'H', 'H', 'V', 'V', 'V'],
  ['V', 'V', 'V', 'V', 'V', 'V', 'H', 'H', 'H', 'H'],
  ['V', 'H', 'H', 'H', 'H', 'V', 'H', 'H', 'H', 'H'],
])
pos_v = np.array([-1, -1, 3, 5, 3, 3, -1, 3, -1, 4])
neg_v = np.array([-1, 2, 3, 4, -1, 3, 4, 3, 4, 4])
pos_h = np.array([5, -1, -1, -1, 5, -1, 3, 1, -1])
neg_h = np.array([4, -1, 4, -1, 5, 4, -1, 2, -1])

binst = board.Board(board=bor, sides={'pos_v': pos_v, 'neg_v': neg_v, 'pos_h': pos_h, 'neg_h': neg_h})
solutions = binst.solve_and_print()
```
Output:
```
Solution found
[['-' '+' '-' '+' ' ' '+' '-' '+' '-' '+']
 [' ' ' ' '+' '-' ' ' '-' '+' '-' '+' '-']
 ['-' '+' '-' '+' ' ' ' ' '-' '+' '-' '+']
 ['+' '-' '+' '-' '+' '-' '+' '-' '+' '-']
 ['-' '+' '-' '+' '-' '+' '-' '+' '-' '+']
 [' ' '-' '+' '-' '+' '-' '+' ' ' '+' '-']
 [' ' ' ' ' ' '+' '-' '+' '-' ' ' '-' '+']
 ['-' ' ' ' ' '-' '+' ' ' ' ' ' ' ' ' ' ']
 ['+' ' ' ' ' '+' '-' ' ' '+' '-' '+' '-']]
Solutions found: 1
status: OPTIMAL
```

Which exactly matches the true solutions:

<img src="../images/magnets_solved.png" alt="Magnets solved" width="500">
