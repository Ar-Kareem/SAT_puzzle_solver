# Sudoku (Puzzle Type #2)

This is a dedicated solver for Sudoku. Also known as Number Place and Solo. 

The code can:

1. Solve arbitrarily sized valid board sizes, thus can be used to solve:
   - Hex Sudoku (a 16x16 variant) 
   - Kidoku (a kid-friendly sudoku variant)
2. Solve the ["Sandwich" sudoku variant](https://dkmgames.com/SandwichSudoku/) using the optional parameter `sandwich={'side': [...], 'bottom': [...]}`
3. Solve the ["Sudoku-X" variant](https://www.sudopedia.org/wiki/Sudoku-X) using the optional parameter `unique_diagonal=True`

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

<img src="https://raw.githubusercontent.com/Ar-Kareem/puzzle_solver/master/images/puzzles/sudoku_unsolved.png" alt="Sudoku unsolved" width="500">

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
    0   0   0   0   0   0   0   0   0   0   1   1   1   1   1   1  
    0   1   2   3   4   5   6   7   8   9   0   1   2   3   4   5
  ┌───┬───┬───┬───┬───┬───┬───┬───┬───┬───┬───┬───┬───┬───┬───┬───┐
 0│ g │ 7 │ 5 │ 4 │ 9 │ 1 │ c │ e │ d │ f │ b │ 8 │ 2 │ 6 │ 3 │ a │
  ├───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┤
 1│ 3 │ 9 │ d │ e │ f │ a │ 7 │ g │ 2 │ 6 │ 4 │ c │ 5 │ 1 │ 8 │ b │
  ├───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┤
 2│ b │ c │ 1 │ 8 │ 5 │ 6 │ 3 │ 2 │ e │ 9 │ 7 │ a │ 4 │ g │ f │ d │
  ├───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┤
 3│ f │ 6 │ 2 │ a │ b │ 8 │ d │ 4 │ 1 │ 3 │ 5 │ g │ c │ 7 │ 9 │ e │
  ├───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┤
 4│ 4 │ a │ e │ 3 │ 8 │ f │ 1 │ 6 │ 5 │ b │ 2 │ 9 │ g │ d │ c │ 7 │
  ├───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┤
 5│ 6 │ g │ f │ c │ e │ d │ 2 │ 5 │ 4 │ 7 │ a │ 1 │ 3 │ 9 │ b │ 8 │
  ├───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┤
 6│ d │ 1 │ 9 │ 2 │ a │ 3 │ b │ 7 │ c │ g │ 8 │ 6 │ e │ f │ 5 │ 4 │
  ├───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┤
 7│ 5 │ b │ 8 │ 7 │ g │ 4 │ 9 │ c │ f │ d │ 3 │ e │ 1 │ a │ 2 │ 6 │
  ├───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┤
 8│ 2 │ e │ a │ b │ d │ c │ g │ 1 │ 3 │ 8 │ 9 │ f │ 7 │ 4 │ 6 │ 5 │
  ├───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┤
 9│ 8 │ 4 │ 6 │ 1 │ 3 │ b │ e │ f │ 7 │ 5 │ c │ d │ a │ 2 │ g │ 9 │
  ├───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┤
10│ 9 │ f │ 3 │ g │ 7 │ 5 │ 8 │ a │ 6 │ 4 │ e │ 2 │ d │ b │ 1 │ c │
  ├───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┤
11│ c │ d │ 7 │ 5 │ 4 │ 2 │ 6 │ 9 │ g │ a │ 1 │ b │ 8 │ 3 │ e │ f │
  ├───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┤
12│ 7 │ 5 │ g │ d │ 2 │ 9 │ a │ b │ 8 │ c │ f │ 3 │ 6 │ e │ 4 │ 1 │
  ├───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┤
13│ a │ 2 │ b │ 6 │ c │ e │ 5 │ 3 │ 9 │ 1 │ d │ 4 │ f │ 8 │ 7 │ g │
  ├───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┤
14│ e │ 8 │ c │ f │ 1 │ g │ 4 │ d │ b │ 2 │ 6 │ 7 │ 9 │ 5 │ a │ 3 │
  ├───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┤
15│ 1 │ 3 │ 4 │ 9 │ 6 │ 7 │ f │ 8 │ a │ e │ g │ 5 │ b │ c │ d │ 2 │
  └───┴───┴───┴───┴───┴───┴───┴───┴───┴───┴───┴───┴───┴───┴───┴───┘
Solutions found: 1
status: OPTIMAL
Time taken: 0.04 seconds
```

**Solved puzzle**

<img src="https://raw.githubusercontent.com/Ar-Kareem/puzzle_solver/master/images/puzzles/sudoku_solved.png" alt="Sudoku solved" width="500">

# Sudoku Jigsaw (Puzzle Type #52)

* [**Play online**](https://www.puzzle-jigsaw-sudoku.com/)

1. The basic Sudoku rules apply.
2. The difference is that instead of having 3x3 rectangular blocks these blocks have irregular shapes

**Unsolved puzzle**

<img src="https://raw.githubusercontent.com/Ar-Kareem/puzzle_solver/master/images/puzzles/sudoku_jigsaw_unsolved.png" alt="Sudoku Jigsaw unsolved" width="500">

Code to utilize this package and solve the puzzle:

(Note: the ids are arbitrary and simply represent cells that share a block)

```python
import numpy as np
from puzzle_solver import sudoku_solver as solver
board = np.array([
  [ '1', ' ', ' ', '2', ' ', ' ', '8', '5', ' ' ],
  [ '2', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ' ],
  [ ' ', ' ', '8', ' ', ' ', ' ', ' ', ' ', ' ' ],
  [ '7', ' ', ' ', '5', ' ', '1', ' ', ' ', ' ' ],
  [ ' ', ' ', ' ', '1', ' ', '3', ' ', ' ', ' ' ],
  [ ' ', ' ', ' ', '8', ' ', '4', ' ', ' ', '6' ],
  [ ' ', ' ', ' ', ' ', ' ', ' ', '5', ' ', ' ' ],
  [ ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '5' ],
  [ ' ', '2', '6', ' ', ' ', '9', ' ', ' ', '1' ],
])
jigsaw_ids = np.array([
  ['00', '00', '01', '01', '01', '01', '02', '02', '02'],
  ['00', '00', '01', '01', '03', '01', '01', '02', '02'],
  ['00', '00', '01', '04', '03', '03', '02', '02', '02'],
  ['00', '04', '04', '04', '03', '03', '03', '03', '02'],
  ['00', '00', '04', '04', '03', '03', '05', '05', '05'],
  ['06', '04', '04', '04', '05', '05', '05', '07', '05'],
  ['06', '08', '08', '08', '08', '05', '05', '07', '07'],
  ['06', '06', '06', '06', '08', '07', '07', '07', '07'],
  ['06', '06', '06', '08', '08', '08', '08', '07', '07'],
])
binst = solver.Board(board=board, jigsaw=jigsaw_ids, constrain_blocks=False)
solutions = binst.solve_and_print()
```

**Script Output**

```python
Solution found

    0   1   2   3   4   5   6   7   8
  ┌───┬───┬───┬───┬───┬───┬───┬───┬───┐
 0│ 1 │ 9 │ 4 │ 2 │ 3 │ 6 │ 8 │ 5 │ 7 │
  ├───┼───┼───┼───┼───┼───┼───┼───┼───┤
 1│ 2 │ 8 │ 5 │ 9 │ 4 │ 7 │ 1 │ 6 │ 3 │
  ├───┼───┼───┼───┼───┼───┼───┼───┼───┤
 2│ 6 │ 3 │ 8 │ 4 │ 7 │ 5 │ 9 │ 1 │ 2 │
  ├───┼───┼───┼───┼───┼───┼───┼───┼───┤
 3│ 7 │ 6 │ 3 │ 5 │ 9 │ 1 │ 2 │ 8 │ 4 │
  ├───┼───┼───┼───┼───┼───┼───┼───┼───┤
 4│ 4 │ 5 │ 2 │ 1 │ 6 │ 3 │ 7 │ 9 │ 8 │
  ├───┼───┼───┼───┼───┼───┼───┼───┼───┤
 5│ 5 │ 7 │ 9 │ 8 │ 1 │ 4 │ 3 │ 2 │ 6 │
  ├───┼───┼───┼───┼───┼───┼───┼───┼───┤
 6│ 3 │ 1 │ 7 │ 6 │ 8 │ 2 │ 5 │ 4 │ 9 │
  ├───┼───┼───┼───┼───┼───┼───┼───┼───┤
 7│ 9 │ 4 │ 1 │ 7 │ 2 │ 8 │ 6 │ 3 │ 5 │
  ├───┼───┼───┼───┼───┼───┼───┼───┼───┤
 8│ 8 │ 2 │ 6 │ 3 │ 5 │ 9 │ 4 │ 7 │ 1 │
  └───┴───┴───┴───┴───┴───┴───┴───┴───┘
Solutions found: 1
status: OPTIMAL
Time taken: 0.01 seconds
```

**Solved puzzle**

<img src="https://raw.githubusercontent.com/Ar-Kareem/puzzle_solver/master/images/puzzles/sudoku_jigsaw_solved.png" alt="Sudoku Jigsaw solved" width="500">

# Sudoku Killer (Puzzle Type #53)

* [**Play online**](https://www.puzzle-killer-sudoku.com/)

1. The basic Sudoku rules apply.
2. The sum of all numbers in a cage must match the small number printed in its corner.
3. No number appears more than once in a cage.

**Unsolved puzzle**

<img src="https://raw.githubusercontent.com/Ar-Kareem/puzzle_solver/master/images/puzzles/sudoku_killer_unsolved.png" alt="Sudoku Killer unsolved" width="500">

Code to utilize this package and solve the puzzle:

(Note: the ids are arbitrary and simply represent cells that share a cage)

```python
import numpy as np
from puzzle_solver import sudoku_solver as solver
board = np.full((9, 9), ' ')
killer_board = np.array([
  ['01', '01', '03', '03', '03', '12', '12', '13', '14'],
  ['02', '01', '04', '16', '16', '17', '17', '13', '14'],
  ['02', '02', '04', '18', '19', '19', '15', '15', '14'],
  ['11', '11', '05', '18', '19', '19', '20', '15', '23'],
  ['10', '10', '05', '30', '31', '32', '20', '22', '23'],
  ['08', '07', '06', '30', '31', '32', '21', '22', '24'],
  ['08', '07', '06', '29', '31', '33', '21', '24', '24'],
  ['09', '34', '34', '29', '28', '33', '26', '26', '25'],
  ['09', '34', '34', '28', '28', '27', '27', '25', '25'],
])
killer_clues = {
  '01': 16, '02': 11, '03': 24, '04': 10, '05': 11, '06': 7, '07': 10, '08': 10, '09': 16,
  '10': 11, '11': 10, '12': 7, '13': 11, '14': 16, '15': 16, '16': 8, '17': 12, '18': 8, '19': 15,
  '20': 7, '21': 10, '22': 5, '23': 13, '24': 16, '25': 9, '26': 14, '27': 15, '28': 13, '29': 11,
  '30': 9, '31': 15, '32': 13, '33': 11, '34': 15,
}
binst = solver.Board(board=board, block_size=(3, 3), killer=(killer_board, killer_clues))
solutions = binst.solve_and_print()
```

**Script Output**

```python
Solution found

    0   1   2   3   4   5   6   7   8
  ┌───┬───┬───┬───┬───┬───┬───┬───┬───┐
 0│ 5 │ 4 │ 8 │ 7 │ 9 │ 1 │ 6 │ 2 │ 3 │
  ├───┼───┼───┼───┼───┼───┼───┼───┼───┤
 1│ 3 │ 7 │ 1 │ 6 │ 2 │ 8 │ 4 │ 9 │ 5 │
  ├───┼───┼───┼───┼───┼───┼───┼───┼───┤
 2│ 2 │ 6 │ 9 │ 5 │ 4 │ 3 │ 1 │ 7 │ 8 │
  ├───┼───┼───┼───┼───┼───┼───┼───┼───┤
 3│ 1 │ 9 │ 4 │ 3 │ 6 │ 2 │ 5 │ 8 │ 7 │
  ├───┼───┼───┼───┼───┼───┼───┼───┼───┤
 4│ 8 │ 3 │ 7 │ 1 │ 5 │ 9 │ 2 │ 4 │ 6 │
  ├───┼───┼───┼───┼───┼───┼───┼───┼───┤
 5│ 6 │ 2 │ 5 │ 8 │ 7 │ 4 │ 3 │ 1 │ 9 │
  ├───┼───┼───┼───┼───┼───┼───┼───┼───┤
 6│ 4 │ 8 │ 2 │ 9 │ 3 │ 5 │ 7 │ 6 │ 1 │
  ├───┼───┼───┼───┼───┼───┼───┼───┼───┤
 7│ 7 │ 1 │ 3 │ 2 │ 8 │ 6 │ 9 │ 5 │ 4 │
  ├───┼───┼───┼───┼───┼───┼───┼───┼───┤
 8│ 9 │ 5 │ 6 │ 4 │ 1 │ 7 │ 8 │ 3 │ 2 │
  └───┴───┴───┴───┴───┴───┴───┴───┴───┘
Solutions found: 1
status: OPTIMAL
Time taken: 0.02 seconds
```

**Solved puzzle**

<img src="https://raw.githubusercontent.com/Ar-Kareem/puzzle_solver/master/images/puzzles/sudoku_killer_solved.png" alt="Sudoku Killer solved" width="500">
