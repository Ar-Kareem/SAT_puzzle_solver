# Keen (Puzzle Type #6)

This is a dedicated solver for Keen

Below are the details of how to utilize the solver. In addition, the solver gives all possible solutions to the input thus it can be utilized to figure out if a single partial input board has multiple possible solutions.

(The solver mainly utilizes the CP-SAT solver from Google OR-Tools)

* [**Play online**](https://www.chiark.greenend.org.uk/~sgtatham/puzzles/js/keen.html)

* [**Instructions**](https://www.chiark.greenend.org.uk/~sgtatham/puzzles/doc/keen.html#keen)

You have a square grid; each square may contain a digit from 1 to the size of the grid. The grid is divided into blocks of varying shape and size, with arithmetic clues written in them. Your aim is to fully populate the grid with digits such that:

  - Each row contains only one occurrence of each digit
  - Each column contains only one occurrence of each digit
  - The digits in each block can be combined to form the number stated in the clue, using the arithmetic operation given in the clue. That is:
      - An addition clue means that the sum of the digits in the block must be the given number. For example, ‘15+’ means the contents of the block adds up to fifteen.
      - A multiplication clue (e.g. ‘60×’), similarly, means that the product of the digits in the block must be the given number.
      - A subtraction clue will always be written in a block of size two, and it means that one of the digits in the block is greater than the other by the given amount. For example, ‘2−’ means that one of the digits in the block is 2 more than the other, or equivalently that one digit minus the other one is 2. The two digits could be either way round, though.
      - A division clue (e.g. ‘3÷’), similarly, is always in a block of size two and means that one digit divided by the other is equal to the given amount.

  Note that a block may contain the same digit more than once (provided the identical ones are not in the same row and column). This rule is precisely the opposite of the rule in Solo's ‘Killer’ mode (see chapter 11).

**Unsolved puzzle**

<img src="../images/keen_unsolved.png" alt="Keen unsolved" width="500">

Code to utilize this package and solve the puzzle:
```python
import numpy as np
from . import solver
# tells the api the shape of the blocks in the board
bor = np.array([
  ['d01', 'd01', 'd03', 'd03', 'd05', 'd05', 'd08', 'd08', 'd10'],
  ['d02', 'd02', 'd03', 'd04', 'd06', 'd06', 'd09', 'd09', 'd10'],
  ['d12', 'd13', 'd14', 'd04', 'd07', 'd07', 'd07', 'd11', 'd11'],
  ['d12', 'd13', 'd14', 'd14', 'd15', 'd16', 'd11', 'd11', 'd18'],
  ['d19', 'd20', 'd24', 'd26', 'd15', 'd16', 'd16', 'd17', 'd18'],
  ['d19', 'd20', 'd24', 'd26', 'd28', 'd28', 'd29', 'd17', 'd33'],
  ['d21', 'd21', 'd24', 'd27', 'd30', 'd30', 'd29', 'd33', 'd33'],
  ['d22', 'd23', 'd25', 'd27', 'd31', 'd32', 'd34', 'd34', 'd36'],
  ['d22', 'd23', 'd25', 'd25', 'd31', 'd32', 'd35', 'd35', 'd36'],
])
# tells the api the operation and the result for each block
block_results = {
  'd01': ('-', 1), 'd02': ('-', 1), 'd03': ('*', 378), 'd04': ('/', 4), 'd05': ('/', 2),
  'd06': ('-', 2), 'd07': ('*', 6), 'd08': ('+', 9), 'd09': ('/', 2), 'd10': ('+', 9),
  'd11': ('+', 22), 'd12': ('-', 1), 'd13': ('*', 30), 'd14': ('+', 12), 'd15': ('-', 1),
  'd16': ('*', 196), 'd17': ('*', 63), 'd18': ('-', 1), 'd19': ('/', 3), 'd20': ('/', 3),
  'd21': ('*', 21), 'd22': ('/', 4), 'd23': ('-', 7), 'd24': ('*', 64), 'd25': ('+', 15),
  'd26': ('-', 1), 'd27': ('+', 11), 'd28': ('-', 4), 'd29': ('/', 4), 'd30': ('*', 54),
  'd31': ('+', 11), 'd32': ('/', 4), 'd33': ('+', 16), 'd34': ('+', 15), 'd35': ('*', 30),
  'd36': ('-', 7),
}
binst = solver.Board(board=bor, block_results=block_results)
solutions = binst.solve_and_print()
```
**Script Output**
```
Solution found
[[5 4 7 9 3 6 8 1 2]
 [9 8 6 1 5 3 2 4 7]
 [7 5 9 4 2 1 3 8 6]
 [8 6 1 2 9 7 5 3 4]
 [6 1 2 5 8 4 7 9 3]
 [2 3 8 6 1 5 4 7 9]
 [3 7 4 8 6 9 1 2 5]
 [4 2 5 3 7 8 9 6 1]
 [1 9 3 7 4 2 6 5 8]]
Solutions found: 1
status: OPTIMAL
Time taken: 0.02 seconds
```

**Solved puzzle**

<img src="../images/keen_solved.png" alt="Keen solved" width="500">
