# Sudoku (Puzzle Type #2)

This is a dedicated solver for Sudoku (Called "Solo" in the website)

Below are the details of how to utilize the solver. In addition, the solver gives all possible solutions to the input thus it can be utilized to figure out if a single partial input board has multiple possible solutions.

(The solver under the hood mainly utilizes the CP-SAT solver from Google OR-Tools)

* [**Play online**](https://www.chiark.greenend.org.uk/~sgtatham/puzzles/js/solo.html)

* [**Instructions**](https://www.chiark.greenend.org.uk/~sgtatham/puzzles/doc/solo.html#solo)

You have a square grid, which is divided into as many equally sized sub-blocks as the grid has rows. Each square must be filled in with a digit from 1 to the size of the grid, in such a way that

  - every row contains only one occurrence of each digit
  - every column contains only one occurrence of each digit
  - every block contains only one occurrence of each digit.

You are given some of the numbers as clues; your aim is to place the rest of the numbers correctly.

**Unsolved puzzle**

<img src="https://raw.githubusercontent.com/Ar-Kareem/puzzle_solver/master/images/sudoku_unsolved.png" alt="Sudoku unsolved" width="500">

Code to utilize this package and solve the puzzle:

Note: 

- The solver also supports solving the ["Sandwich" sudoku variant](https://dkmgames.com/SandwichSudoku/) through the optional parameter ``sandwich={'side': [...], 'bottom': [...] }``。

- The solver also supports solving the ["Sudoku-X" variant](https://www.sudopedia.org/wiki/Sudoku-X) through the optional parameter ``unique_diagonal=True``。

```python
import numpy as np
from puzzle_solver import sudoku_solver as solver
board = np.array([
  [' ', '7', '5', '4',  '9', '1', 'c', 'e',  'd', 'f', ' ', ' ',  '2', ' ', '3', ' '],
  [' ', ' ', ' ', ' ',  'f', 'a', ' ', ' ',  ' ', '6', ' ', 'c',  ' ', ' ', '8', 'b'],
  [' ', ' ', '1', ' ',  ' ', '6', ' ', ' ',  ' ', '9', ' ', ' ',  ' ', 'g', ' ', 'd'],
  [' ', '6', ' ', ' ',  ' ', ' ', ' ', ' ',  ' ', ' ', '5', 'g',  'c', '7', ' ', ' '],

  ['4', 'a', ' ', ' ',  ' ', ' ', ' ', ' ',  ' ', ' ', ' ', '9',  ' ', ' ', ' ', ' '],
  [' ', 'g', 'f', ' ',  'e', ' ', ' ', '5',  '4', ' ', ' ', '1',  ' ', '9', ' ', '8'],
  [' ', ' ', ' ', ' ',  'a', '3', 'b', '7',  'c', 'g', ' ', '6',  ' ', ' ', ' ', '4'],
  [' ', 'b', ' ', '7',  ' ', ' ', ' ', ' ',  'f', ' ', '3', ' ',  ' ', 'a', ' ', '6'],

  ['2', ' ', 'a', ' ',  ' ', 'c', ' ', '1',  ' ', ' ', ' ', ' ',  '7', ' ', '6', ' '],
  ['8', ' ', ' ', ' ',  '3', ' ', 'e', 'f',  '7', '5', 'c', 'd',  ' ', ' ', ' ', ' '],
  ['9', ' ', '3', ' ',  '7', ' ', ' ', 'a',  '6', ' ', ' ', '2',  ' ', 'b', '1', ' '],
  [' ', ' ', ' ', ' ',  '4', ' ', ' ', ' ',  ' ', ' ', ' ', ' ',  ' ', ' ', 'e', 'f'],

  [' ', ' ', 'g', 'd',  '2', '9', ' ', ' ',  ' ', ' ', ' ', ' ',  ' ', ' ', '4', ' '],
  ['a', ' ', 'b', ' ',  ' ', ' ', '5', ' ',  ' ', ' ', 'd', ' ',  ' ', '8', ' ', ' '],
  ['e', '8', ' ', ' ',  '1', ' ', '4', ' ',  ' ', ' ', '6', '7',  ' ', ' ', ' ', ' '],
  [' ', '3', ' ', '9',  ' ', ' ', 'f', '8',  'a', 'e', 'g', '5',  'b', 'c', 'd', ' '],
])
binst = solver.Board(board=board)
solutions = binst.solve_and_print()
assert len(solutions) == 1, f'unique solutions != 1, == {len(solutions)}'
```
**Script Output**
```
Solution found
[['g' '7' '5' '4' '9' '1' 'c' 'e' 'd' 'f' 'b' '8' '2' '6' '3' 'a']
 ['3' '9' 'd' 'e' 'f' 'a' '7' 'g' '2' '6' '4' 'c' '5' '1' '8' 'b']
 ['b' 'c' '1' '8' '5' '6' '3' '2' 'e' '9' '7' 'a' '4' 'g' 'f' 'd']
 ['f' '6' '2' 'a' 'b' '8' 'd' '4' '1' '3' '5' 'g' 'c' '7' '9' 'e']
 ['4' 'a' 'e' '3' '8' 'f' '1' '6' '5' 'b' '2' '9' 'g' 'd' 'c' '7']
 ['6' 'g' 'f' 'c' 'e' 'd' '2' '5' '4' '7' 'a' '1' '3' '9' 'b' '8']
 ['d' '1' '9' '2' 'a' '3' 'b' '7' 'c' 'g' '8' '6' 'e' 'f' '5' '4']
 ['5' 'b' '8' '7' 'g' '4' '9' 'c' 'f' 'd' '3' 'e' '1' 'a' '2' '6']
 ['2' 'e' 'a' 'b' 'd' 'c' 'g' '1' '3' '8' '9' 'f' '7' '4' '6' '5']
 ['8' '4' '6' '1' '3' 'b' 'e' 'f' '7' '5' 'c' 'd' 'a' '2' 'g' '9']
 ['9' 'f' '3' 'g' '7' '5' '8' 'a' '6' '4' 'e' '2' 'd' 'b' '1' 'c']
 ['c' 'd' '7' '5' '4' '2' '6' '9' 'g' 'a' '1' 'b' '8' '3' 'e' 'f']
 ['7' '5' 'g' 'd' '2' '9' 'a' 'b' '8' 'c' 'f' '3' '6' 'e' '4' '1']
 ['a' '2' 'b' '6' 'c' 'e' '5' '3' '9' '1' 'd' '4' 'f' '8' '7' 'g']
 ['e' '8' 'c' 'f' '1' 'g' '4' 'd' 'b' '2' '6' '7' '9' '5' 'a' '3']
 ['1' '3' '4' '9' '6' '7' 'f' '8' 'a' 'e' 'g' '5' 'b' 'c' 'd' '2']]
Solutions found: 1
status: OPTIMAL
Time taken: 0.04 seconds
```

**Solved puzzle**

<img src="https://raw.githubusercontent.com/Ar-Kareem/puzzle_solver/master/images/sudoku_solved.png" alt="Sudoku solved" width="500">
