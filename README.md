# SAT Puzzle Solver

Solve classic logic puzzles problems in Python.  
Each puzzle family lives in its own folder with a minimal, self-contained example.

Play the original puzzles online: https://www.chiark.greenend.org.uk/~sgtatham/puzzles

All the solvers in this repo use the CP-SAT solver from Google OR-Tools.

---

## Table of Contents

- [SAT Puzzle Solver](#sat-puzzle-solver)
  - [Table of Contents](#table-of-contents)
  - [Why SAT / CP-SAT?](#why-sat--cp-sat)
  - [What’s Inside](#whats-inside)
- [Puzzles](#puzzles)
  - [Nonograms (Puzzle Type #1)](#nonograms-puzzle-type-1)
  - [Sudoku (Puzzle Type #2)](#sudoku-puzzle-type-2)
  - [Light Up (Puzzle Type #3)](#light-up-puzzle-type-3)
  - [Tents (Puzzle Type #4)](#tents-puzzle-type-4)
  - [Filling (Puzzle Type #5)](#filling-puzzle-type-5)
  - [Keen (Puzzle Type #6)](#keen-puzzle-type-6)
  - [Towers (Puzzle Type #7)](#towers-puzzle-type-7)
  - [Singles (Puzzle Type #8)](#singles-puzzle-type-8)
  - [Magnets (Puzzle Type #9)](#magnets-puzzle-type-9)
  - [Range (Puzzle Type #10)](#range-puzzle-type-10)
  - [UnDead (Puzzle Type #11)](#undead-puzzle-type-11)
  - [Unruly (Puzzle Type #12)](#unruly-puzzle-type-12)
  - [Mosaic (Puzzle Type #13)](#mosaic-puzzle-type-13)
  - [Quick Start](#quick-start)
    - [1) Install Python deps](#1-install-python-deps)
    - [2) Explore a puzzle](#2-explore-a-puzzle)
  - [Testing](#testing)
  - [Contributing](#contributing)

---

## Why SAT / CP-SAT?

Many pencil puzzles can be modeled with:

- **Boolean decisions** (e.g., black/white, bulb/no-bulb)
- **Linear constraints** (counts, separations, adjacency)
- **All-different / visibility / reachability** constraints

This repo builds those constraints in Python and uses SAT/CP-SAT (e.g., OR-Tools) to search efficiently. It both demonstrates the modeling and provides usable solvers.

---

## What’s Inside

Each chapter directory targets a different puzzle type:

* `chapter10_nonograms` — Picross/Griddlers (run-length constraints). ()
* `chapter11_sudoku` — Sudoku (rows/cols/blocks all-different). ([Chapter 11][2])
* `chapter21_light_up` — *Akari* / Light Up (lighting & adjacency). ([Chapter 21][3])
* `chapter25_tents` — Tents (tree-tent matching). ([Chapter 25][4])
* `chapter29_filling` — Filling (Fillomino-style), region sizes. ([Chapter 29][5])
* `chapter30_keen` — Keen (arithmetic operations). ([Chapter 30][6])
* `chapter31_towers` — Skyscrapers (permutation + visibility). ([Chapter 31][7])
* `chapter32_singles` — Singles (hiding numbers). ([Chapter 32][8])
* `chapter33_magnets` — Magnets (polarized dominoes + counts). ([Chapter 33][9])
* `chapter35_range` — Range (rays & totals). ([Chapter 35][10])
* `chapter37_undead` — UnDead (Vampires/Zombies/Ghosts). ([Chapter 37][11])
* `chapter38_unruly` — Unruly (no triples + balance). ([Chapter 38][12])
* `chapter42_mosaic` — Mosaic (Tapa-like tiling). ([Chapter 42][13])

---

# Puzzles

The puzzles that have solvers implemented are listed below:

## Nonograms (Puzzle Type #1)

Called "Pattern" in the website.

* [**Play online**](https://www.chiark.greenend.org.uk/~sgtatham/puzzles/js/pattern.html)

* [**Instructions**](https://www.chiark.greenend.org.uk/~sgtatham/puzzles/doc/pattern.html#pattern)

* [**Solver Code**][1]

<details>
  <summary><strong>Rules</strong></summary>
You have a grid of squares, which must all be filled in either black or white. Beside each row of the grid are listed, in order, the lengths of the runs of black squares on that row; above each column are listed, in order, the lengths of the runs of black squares in that column. Your aim is to fill in the entire grid black or white. 
</details>

**Unsolved puzzle**

<img src="./images/nonogram_unsolved.png" alt="Nonogram unsolved" width="500">

Code to utilize this package and solve the puzzle:
```python
from . import board
top_numbers = [
  [8, 2],
  [5, 4],
  [2, 1, 4],
  [2, 4],
  [2, 1, 4],
  [2, 5],
  [2, 8],
  [3, 2],
  [1, 6],
  [1, 9],
  [1, 6, 1],
  [1, 5, 3],
  [3, 2, 1],
  [4, 2],
  [1, 5],
]
side_numbers = [
  [7, 3],
  [7, 1, 1],
  [2, 3],
  [2, 3],
  [3, 2],
  [1, 1, 1, 1, 2],
  [1, 6, 1],
  [1, 9],
  [9],
  [2, 4],
  [8],
  [11],
  [7, 1, 1],
  [4, 3],
  [3, 2],
]
binst = board.Board(top=top_numbers, side=side_numbers)
solutions = binst.solve_and_print()
```
**Script Output**
```
Solution found
B B B B B B B . B B B . . . .
B B B B B B B . . . . . B . B
B B . . . . . . . . . B B B .
B B . . . . . . . . . . B B B
B B B . . . . . . . . . . B B
B . . . B . B . . B . . . B B
B . . . . . B B B B B B . . B
B . . . . . B B B B B B B B B
. . . . . B B B B B B B B B .
. . . . . B B . B B B B . . .
. . . . B B B B B B B B . . .
B B B B B B B B B B B . . . .
B B B B B B B . . B . B . . .
. B B B B . . . . B B B . . .
. B B B . . . . . . . B B . .
Solutions found: 1
status: OPTIMAL
Time taken: 0.04 seconds
```

**Solved puzzle**

<img src="./images/nonogram_solved.png" alt="Nonogram solved" width="500">

---

## Sudoku (Puzzle Type #2)

Called "Solo" in the website.

* [**Play online**](https://www.chiark.greenend.org.uk/~sgtatham/puzzles/js/solo.html)

* [**Instructions**](https://www.chiark.greenend.org.uk/~sgtatham/puzzles/doc/solo.html#solo)

* [**Solver Code**][2]

<details>
  <summary><strong>Rules</strong></summary>
You have a square grid, which is divided into as many equally sized sub-blocks as the grid has rows. Each square must be filled in with a digit from 1 to the size of the grid, in such a way that

  - every row contains only one occurrence of each digit
  - every column contains only one occurrence of each digit
  - every block contains only one occurrence of each digit.

You are given some of the numbers as clues; your aim is to place the rest of the numbers correctly.
</details>

**Unsolved puzzle**

<img src="./images/sudoku_unsolved.png" alt="Sudoku unsolved" width="500">

Code to utilize this package and solve the puzzle:
```python
import numpy as np
from . import board
bor = np.array([
  ['*', '7', '5', '4',  '9', '1', 'c', 'e',  'd', 'f', '*', '*',  '2', '*', '3', '*'],
  ['*', '*', '*', '*',  'f', 'a', '*', '*',  '*', '6', '*', 'c',  '*', '*', '8', 'b'],
  ['*', '*', '1', '*',  '*', '6', '*', '*',  '*', '9', '*', '*',  '*', 'g', '*', 'd'],
  ['*', '6', '*', '*',  '*', '*', '*', '*',  '*', '*', '5', 'g',  'c', '7', '*', '*'],

  ['4', 'a', '*', '*',  '*', '*', '*', '*',  '*', '*', '*', '9',  '*', '*', '*', '*'],
  ['*', 'g', 'f', '*',  'e', '*', '*', '5',  '4', '*', '*', '1',  '*', '9', '*', '8'],
  ['*', '*', '*', '*',  'a', '3', 'b', '7',  'c', 'g', '*', '6',  '*', '*', '*', '4'],
  ['*', 'b', '*', '7',  '*', '*', '*', '*',  'f', '*', '3', '*',  '*', 'a', '*', '6'],

  ['2', '*', 'a', '*',  '*', 'c', '*', '1',  '*', '*', '*', '*',  '7', '*', '6', '*'],
  ['8', '*', '*', '*',  '3', '*', 'e', 'f',  '7', '5', 'c', 'd',  '*', '*', '*', '*'],
  ['9', '*', '3', '*',  '7', '*', '*', 'a',  '6', '*', '*', '2',  '*', 'b', '1', '*'],
  ['*', '*', '*', '*',  '4', '*', '*', '*',  '*', '*', '*', '*',  '*', '*', 'e', 'f'],

  ['*', '*', 'g', 'd',  '2', '9', '*', '*',  '*', '*', '*', '*',  '*', '*', '4', '*'],
  ['a', '*', 'b', '*',  '*', '*', '5', '*',  '*', '*', 'd', '*',  '*', '8', '*', '*'],
  ['e', '8', '*', '*',  '1', '*', '4', '*',  '*', '*', '6', '7',  '*', '*', '*', '*'],
  ['*', '3', '*', '9',  '*', '*', 'f', '8',  'a', 'e', 'g', '5',  'b', 'c', 'd', '*'],
])
binst = board.Board(board=bor)
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

<img src="./images/sudoku_solved.png" alt="Sudoku solved" width="500">

---

## Light Up (Puzzle Type #3)

* [**Play online**](https://www.chiark.greenend.org.uk/~sgtatham/puzzles/js/lightup.html)

* [**Instructions**](https://www.chiark.greenend.org.uk/~sgtatham/puzzles/doc/lightup.html#lightup)

* [**Solver Code**][3]

<details>
  <summary><strong>Rules</strong></summary>
You have a grid of squares. Some are filled in black; some of the black squares are numbered. Your aim is to ‘light up’ all the empty squares by placing light bulbs in some of them.

Each light bulb illuminates the square it is on, plus all squares in line with it horizontally or vertically unless a black square is blocking the way.

To win the game, you must satisfy the following conditions:

  - All non-black squares are lit.
  - No light is lit by another light.
  - All numbered black squares have exactly that number of lights adjacent to them (in the four squares above, below, and to the side).

Non-numbered black squares may have any number of lights adjacent to them. 
</details>

**Unsolved puzzle**

<img src="./images/lightup_unsolved.png" alt="Light Up unsolved" width="500">

Code to utilize this package and solve the puzzle:
```python
import numpy as np
from . import board
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

binst = board.Board(board=bor)
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

<img src="./images/lightup_solved.png" alt="Light Up solved" width="500">

---

## Tents (Puzzle Type #4)

* [**Play online**](https://www.chiark.greenend.org.uk/~sgtatham/puzzles/js/tents.html)

* [**Instructions**](https://www.chiark.greenend.org.uk/~sgtatham/puzzles/doc/tents.html#tents)

* [**Solver Code**][4]

<details>
  <summary><strong>Rules</strong></summary>
You have a grid of squares, some of which contain trees. Your aim is to place tents in some of the remaining squares, in such a way that the following conditions are met:

  - There are exactly as many tents as trees.
  - The tents and trees can be matched up in such a way that each tent is directly adjacent (horizontally or vertically, but not diagonally) to its own tree. However, a tent may be adjacent to other trees as well as its own.
  - No two tents are adjacent horizontally, vertically or diagonally.
  - The number of tents in each row, and in each column, matches the numbers given round the sides of the grid.
</details>

**Unsolved puzzle**

<img src="./images/tents_unsolved.png" alt="Tents unsolved" width="500">

Code to utilize this package and solve the puzzle:
```python
import numpy as np
from . import board
bor = np.array([
  ['*', 'T', '*', '*', '*', '*', '*', '*', 'T', '*', 'T', '*', 'T', '*', '*'],
  ['*', '*', '*', '*', 'T', '*', '*', 'T', '*', 'T', '*', '*', 'T', '*', '*'],
  ['*', 'T', '*', 'T', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*'],
  ['*', '*', '*', '*', '*', '*', '*', '*', 'T', '*', '*', '*', 'T', '*', 'T'],
  ['*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*'],
  ['*', 'T', '*', '*', 'T', '*', 'T', '*', '*', 'T', '*', '*', 'T', 'T', '*'],
  ['*', 'T', '*', '*', 'T', '*', '*', '*', 'T', '*', '*', '*', '*', '*', '*'],
  ['*', '*', '*', '*', '*', '*', 'T', '*', '*', '*', '*', '*', '*', '*', '*'],
  ['*', '*', '*', '*', '*', 'T', '*', '*', '*', '*', 'T', '*', '*', 'T', '*'],
  ['*', '*', '*', 'T', '*', '*', '*', '*', '*', '*', '*', '*', 'T', '*', 'T'],
  ['T', '*', '*', '*', '*', '*', '*', 'T', '*', '*', '*', 'T', '*', '*', '*'],
  ['T', '*', '*', '*', 'T', '*', 'T', '*', '*', '*', '*', '*', '*', '*', '*'],
  ['*', '*', '*', '*', '*', '*', '*', '*', 'T', '*', 'T', '*', '*', '*', 'T'],
  ['*', 'T', '*', '*', '*', 'T', '*', '*', '*', '*', '*', '*', 'T', '*', '*'],
  ['*', 'T', '*', '*', 'T', '*', '*', '*', '*', 'T', '*', 'T', '*', '*', '*'],
])
side = np.array([4, 1, 6, 0, 5, 2, 3, 1, 5, 2, 3, 2, 4, 3, 4])
top = np.array([4, 2, 4, 1, 3, 3, 3, 3, 3, 3, 2, 2, 6, 2, 4])

binst = board.Board(board=bor, sides={'top': top, 'side': side})
solutions = binst.solve_and_print()
```
**Script Output**
```
Solution found
[[' ' 'T' 'E' ' ' ' ' ' ' ' ' 'E' 'T' ' ' 'T' 'E' 'T' 'E' ' ']
 [' ' ' ' ' ' ' ' 'T' 'E' ' ' 'T' ' ' 'T' ' ' ' ' 'T' ' ' ' ']
 ['E' 'T' 'E' 'T' ' ' ' ' ' ' 'E' ' ' 'E' ' ' ' ' 'E' ' ' 'E']
 [' ' ' ' ' ' ' ' ' ' ' ' ' ' ' ' 'T' ' ' ' ' ' ' 'T' ' ' 'T']
 [' ' 'E' ' ' ' ' 'E' ' ' 'E' ' ' 'E' ' ' ' ' ' ' 'E' ' ' ' ']
 [' ' 'T' ' ' ' ' 'T' ' ' 'T' ' ' ' ' 'T' 'E' ' ' 'T' 'T' 'E']
 [' ' 'T' ' ' ' ' 'T' 'E' ' ' 'E' 'T' ' ' ' ' ' ' 'E' ' ' ' ']
 [' ' 'E' ' ' ' ' ' ' ' ' 'T' ' ' ' ' ' ' ' ' ' ' ' ' ' ' ' ']
 [' ' ' ' ' ' ' ' 'E' 'T' 'E' ' ' ' ' 'E' 'T' ' ' 'E' 'T' 'E']
 ['E' ' ' 'E' 'T' ' ' ' ' ' ' ' ' ' ' ' ' ' ' ' ' 'T' ' ' 'T']
 ['T' ' ' ' ' ' ' ' ' ' ' ' ' 'T' 'E' ' ' ' ' 'T' 'E' ' ' 'E']
 ['T' ' ' ' ' 'E' 'T' 'E' 'T' ' ' ' ' ' ' ' ' ' ' ' ' ' ' ' ']
 ['E' ' ' ' ' ' ' ' ' ' ' ' ' ' ' 'T' 'E' 'T' 'E' ' ' 'E' 'T']
 [' ' 'T' 'E' ' ' 'E' 'T' 'E' ' ' ' ' ' ' ' ' ' ' 'T' ' ' ' ']
 ['E' 'T' ' ' ' ' 'T' ' ' ' ' ' ' 'E' 'T' 'E' 'T' 'E' ' ' ' ']]
Solutions found: 1
status: OPTIMAL
Time taken: 0.02 seconds
```

**Solved puzzle**

<img src="./images/tents_solved.png" alt="Tents solved" width="500">

---

## Filling (Puzzle Type #5)

* [**Play online**](https://www.chiark.greenend.org.uk/~sgtatham/puzzles/js/filling.html)

* [**Instructions**](https://www.chiark.greenend.org.uk/~sgtatham/puzzles/doc/filling.html#filling)

* [**Solver Code**][5]

<details>
  <summary><strong>Rules</strong></summary>
You have a grid of squares, some of which contain digits, and the rest of which are empty. Your job is to fill in digits in the empty squares, in such a way that each connected region of squares all containing the same digit has an area equal to that digit.

(‘Connected region’, for the purposes of this game, does not count diagonally separated squares as adjacent.)

For example, it follows that no square can contain a zero, and that two adjacent squares can not both contain a one. No region has an area greater than 9 (because then its area would not be a single digit).
</details>

(Note: The solver for this puzzle is the only extremely slow solver in this repo and will take a minute to solve a simple 6x7 puzzle)

**Unsolved puzzle**

<img src="./images/filling_unsolved.png" alt="Filling unsolved" width="500">

Code to utilize this package and solve the puzzle:
```python
import numpy as np
from . import board
bor = np.array([
  ['*', '4', '2', '*', '*', '2', '*'],
  ['*', '*', '7', '*', '*', '3', '*'],
  ['*', '*', '*', '*', '4', '*', '3'],
  ['*', '6', '6', '*', '3', '*', '*'],
  ['*', '7', '*', '6', '4', '5', '*'],
  ['*', '6', '*', '*', '*', '*', '4'],
])
binst = board.Board(board=bor)
solutions = binst.solve_and_print()
assert len(solutions) == 1, f'unique solutions != 1, == {len(solutions)}'
```
**Script Output**
```
Solution found
[[4 4 2 2 4 2 2]
 [4 4 7 4 4 3 3]
 [7 7 7 3 4 5 3]
 [7 6 6 3 3 5 5]
 [7 7 6 6 4 5 5]
 [1 6 6 1 4 4 4]]
Solutions found: 1
status: OPTIMAL
Time taken: 46.27 seconds
```

**Solved puzzle**

<img src="./images/filling_solved.png" alt="Filling solved" width="500">

---

## Keen (Puzzle Type #6)

* [**Play online**](https://www.chiark.greenend.org.uk/~sgtatham/puzzles/js/keen.html)

* [**Instructions**](https://www.chiark.greenend.org.uk/~sgtatham/puzzles/doc/keen.html#keen)

* [**Solver Code**][6]

<details>
  <summary><strong>Rules</strong></summary>
You have a square grid; each square may contain a digit from 1 to the size of the grid. The grid is divided into blocks of varying shape and size, with arithmetic clues written in them. Your aim is to fully populate the grid with digits such that:

  - Each row contains only one occurrence of each digit
  - Each column contains only one occurrence of each digit
  - The digits in each block can be combined to form the number stated in the clue, using the arithmetic operation given in the clue. That is:
      - An addition clue means that the sum of the digits in the block must be the given number. For example, ‘15+’ means the contents of the block adds up to fifteen.
      - A multiplication clue (e.g. ‘60×’), similarly, means that the product of the digits in the block must be the given number.
      - A subtraction clue will always be written in a block of size two, and it means that one of the digits in the block is greater than the other by the given amount. For example, ‘2−’ means that one of the digits in the block is 2 more than the other, or equivalently that one digit minus the other one is 2. The two digits could be either way round, though.
      - A division clue (e.g. ‘3÷’), similarly, is always in a block of size two and means that one digit divided by the other is equal to the given amount.

  Note that a block may contain the same digit more than once (provided the identical ones are not in the same row and column). This rule is precisely the opposite of the rule in Solo's ‘Killer’ mode (see chapter 11).
</details>

**Unsolved puzzle**

<img src="./images/keen_unsolved.png" alt="Keen unsolved" width="500">

Code to utilize this package and solve the puzzle:
```python
import numpy as np
from . import board
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
binst = board.Board(board=bor, block_results=block_results)
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

<img src="./images/keen_solved.png" alt="Keen solved" width="500">

---

## Towers (Puzzle Type #7)

* [**Play online**](https://www.chiark.greenend.org.uk/~sgtatham/puzzles/js/towers.html)

* [**Instructions**](https://www.chiark.greenend.org.uk/~sgtatham/puzzles/doc/towers.html#towers)

* [**Solver Code**][7]

<details>
  <summary><strong>Rules</strong></summary>
You have a square grid. On each square of the grid you can build a tower, with its height ranging from 1 to the size of the grid. Around the edge of the grid are some numeric clues.

Your task is to build a tower on every square, in such a way that:

  - Each row contains every possible height of tower once
  - Each column contains every possible height of tower once
  - Each numeric clue describes the number of towers that can be seen if you look into the square from that direction, assuming that shorter towers are hidden behind taller ones. For example, in a 5×5 grid, a clue marked ‘5’ indicates that the five tower heights must appear in increasing order (otherwise you would not be able to see all five towers), whereas a clue marked ‘1’ indicates that the tallest tower (the one marked 5) must come first.

In harder or larger puzzles, some towers will be specified for you as well as the clues round the edge, and some edge clues may be missing. 
</details>

**Unsolved puzzle**

<img src="./images/towers_unsolved.png" alt="Towers unsolved" width="500">

Code to utilize this package and solve the puzzle:
```python
import numpy as np
from . import board
bor = np.array([
  ['*', '*', '*', '*', '*', '*'],
  ['*', '*', '*', '*', '*', '*'],
  ['*', '*', '3', '*', '*', '*'],
  ['*', '*', '*', '*', '*', '*'],
  ['*', '*', '*', '*', '*', '*'],
  ['*', '*', '*', '*', '*', '*'],
])
t = np.array([2, -1, 2, 2, 2, 3])
b = np.array([2, 4, -1, 4, -1, -1])
r = np.array([3, -1, 2, -1, -1, -1])
l = np.array([-1, -1, -1, 2, -1, 4])
binst = board.Board(board=bor, sides={'top': t, 'bottom': b, 'right': r, 'left': l})
solutions = binst.solve_and_print()
```
**Script Output**
```
Solution found
[[5 6 4 1 2 3]
 [3 4 2 6 1 5]
 [4 5 3 2 6 1]
 [2 1 6 5 3 4]
 [6 3 1 4 5 2]
 [1 2 5 3 4 6]]
Solutions found: 1
status: OPTIMAL
Time taken: 0.03 seconds
```

**Solved puzzle**

<img src="./images/towers_solved.png" alt="Towers solved" width="500">

---

## Singles (Puzzle Type #8)

* [**Play online**](https://www.chiark.greenend.org.uk/~sgtatham/puzzles/js/singles.html)

* [**Instructions**](https://www.chiark.greenend.org.uk/~sgtatham/puzzles/doc/singles.html#singles)

* [**Solver Code**][8]

<details>
  <summary><strong>Rules</strong></summary>
You have a grid of white squares, all of which contain numbers. Your task is to colour some of the squares black (removing the number) so as to satisfy all of the following conditions:

  - No number occurs more than once in any row or column.
  - No black square is horizontally or vertically adjacent to any other black square.
  - The remaining white squares must all form one contiguous region (connected by edges, not just touching at corners).
</details>

**Unsolved puzzle**

<img src="./images/singles_unsolved.png" alt="Singles unsolved" width="500">

Code to utilize this package and solve the puzzle:
```python
import numpy as np
from . import board
bor = np.array([
  [1, 6, 5, 4, 9, 8, 9, 3, 5, 1, 3, 7],
  [2, 8, 5, 7, 1, 1, 4, 3, 6, 3, 10, 7],
  [6, 7, 7, 11, 2, 6, 3, 10, 10, 2, 3, 3],
  [11, 9, 4, 3, 6, 1, 2, 5, 3, 10, 7, 8], 
  [5, 5, 4, 9, 7, 9, 6, 6, 11, 5, 4, 11],
  [1, 3, 7, 9, 12, 5, 4, 2, 9, 6, 12, 4],
  [6, 11, 1, 3, 6, 4, 11, 2, 2, 10, 8, 10],
  [3, 11, 12, 6, 2, 9, 9, 1, 4, 8, 12, 5],
  [4, 8, 8, 5, 11, 3, 3, 6, 5, 9, 1, 4],
  [2, 4, 6, 2, 1, 10, 1, 10, 8, 5, 4, 6],
  [5, 1, 6, 10, 9, 4, 8, 4, 8, 3, 2, 12],
  [11, 2, 12, 10, 8, 3, 5, 4, 10, 4, 8, 11],
])
binst = board.Board(board=bor)
solutions = binst.solve_and_print()
```
**Script Output**
```
Solution found
[['B' ' ' 'B' ' ' 'B' ' ' ' ' 'B' ' ' ' ' ' ' ' ']
 [' ' ' ' ' ' ' ' ' ' 'B' ' ' ' ' ' ' 'B' ' ' 'B']
 ['B' ' ' 'B' ' ' 'B' ' ' 'B' ' ' 'B' ' ' 'B' ' ']
 [' ' ' ' ' ' 'B' ' ' ' ' ' ' ' ' ' ' ' ' ' ' ' ']
 ['B' ' ' 'B' ' ' ' ' 'B' ' ' 'B' ' ' 'B' ' ' 'B']
 [' ' ' ' ' ' 'B' ' ' ' ' 'B' ' ' ' ' ' ' 'B' ' ']
 [' ' 'B' ' ' ' ' 'B' ' ' ' ' 'B' ' ' 'B' ' ' ' ']
 [' ' ' ' 'B' ' ' ' ' ' ' 'B' ' ' ' ' ' ' ' ' ' ']
 [' ' 'B' ' ' ' ' ' ' 'B' ' ' ' ' 'B' ' ' ' ' 'B']
 ['B' ' ' 'B' ' ' 'B' ' ' ' ' 'B' ' ' ' ' 'B' ' ']
 [' ' ' ' ' ' ' ' ' ' 'B' ' ' ' ' 'B' ' ' ' ' ' ']
 ['B' ' ' ' ' 'B' ' ' ' ' ' ' 'B' ' ' ' ' 'B' ' ']]
Solutions found: 1
status: OPTIMAL
Time taken: 2.14 seconds
```

**Solved puzzle**

<img src="./images/singles_solved.png" alt="Singles solved" width="500">

---

## Magnets (Puzzle Type #9)

* [**Play online**](https://www.chiark.greenend.org.uk/~sgtatham/puzzles/js/magnets.html)

* [**Instructions**](https://www.chiark.greenend.org.uk/~sgtatham/puzzles/doc/magnets.html#magnets)

* [**Solver Code**][9]

<details>
  <summary><strong>Rules</strong></summary>
A rectangular grid has been filled with a mixture of magnets (that is, dominoes with one positive end and one negative end) and blank dominoes (that is, dominoes with two neutral poles). These dominoes are initially only seen in silhouette. Around the grid are placed a number of clues indicating the number of positive and negative poles contained in certain columns and rows.

Your aim is to correctly place the magnets and blank dominoes such that all the clues are satisfied, with the additional constraint that no two similar magnetic poles may be orthogonally adjacent (since they repel). Neutral poles do not repel, and can be adjacent to any other pole. 
</details>

**Unsolved puzzle**

<img src="./images/magnets_unsolved.png" alt="Magnets unsolved" width="500">

Code to utilize this package and solve the puzzle:
```python
import numpy as np
from . import board
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
**Script Output**
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
Time taken: 0.02 seconds
```

**Solved puzzle**

<img src="./images/magnets_solved.png" alt="Magnets solved" width="500">


---

## Range (Puzzle Type #10)

* [**Play online**](https://www.chiark.greenend.org.uk/~sgtatham/puzzles/js/range.html)

* [**Instructions**](https://www.chiark.greenend.org.uk/~sgtatham/puzzles/doc/range.html#range)

* [**Solver Code**][10]

<details>
  <summary><strong>Rules</strong></summary>
You have a grid of squares; some squares contain numbers. Your job is to colour some of the squares black, such that several criteria are satisfied:

  - no square with a number is coloured black.
  - no two black squares are adjacent (horizontally or vertically).
  - for any two white squares, there is a path between them using only white squares.
  - for each square with a number, that number denotes the total number of white squares reachable from that square going in a straight line in any horizontal or vertical direction until hitting a wall or a black square; the square with the number is included in the total (once).

For instance, a square containing the number one must have four black squares as its neighbours by the last criterion; but then it's impossible for it to be connected to any outside white square, which violates the second to last criterion. So no square will contain the number one. 
</details>

(Note: The solver for this puzzle is slightly slower and could take several seconds to solve a 16x11 puzzle)

**Unsolved puzzle**

<img src="./images/range_unsolved.png" alt="Range unsolved" width="500">

Code to utilize this package and solve the puzzle:
```python
import numpy as np
from . import board
clues = np.array([
    [-1, 4, 2, -1, -1, 3, -1, -1, -1, 8, -1, -1, -1, -1, 6, -1],
    [-1, -1, -1, -1, -1, 13, -1, 18, -1, -1, 14, -1, -1, 22, -1, -1],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 12, -1, -1, -1, -1],
    [-1, -1, -1, -1, 12, -1, 11, -1, -1, -1, 9, -1, -1, -1, -1, -1],
    [7, -1, -1, -1, -1, -1, 6, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, 12, -1, -1, -1, -1, -1, 5],
    [-1, -1, -1, -1, -1, 9, -1, -1, -1, 9, -1, 4, -1, -1, -1, -1],
    [-1, -1, -1, -1, 6, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [-1, -1, 10, -1, -1, 7, -1, -1, 13, -1, 10, -1, -1, -1, -1, -1],
    [-1, 7, -1, -1, -1, -1, 6, -1, -1, -1, 6, -1, -1, 13, 5, -1],
])
board = board.Board(clues)
sols = board.solve_and_print()
```
**Script Output**
```
Solution:
B . . B . . B . B . B . B . . .
. . B . . . . . . . . . . . . B
B . . . . B . . . . . . . . . .
. B . B . . . . . . . B . . . .
. . . . . B . . B . B . . . B .
. . B . . . . . . . . B . . . B
B . . . B . B . . . . . B . . .
. . . . . . . B . . B . . . B .
. B . . . B . . . B . B . . . .
. . . . . . B . . . . . . . . B
B . . . . . . B . . . . B . . .
Solutions found: 1
status: OPTIMAL
Time taken: 3.32 seconds
```

**Solved puzzle**

<img src="./images/range_solved.png" alt="Range solved" width="500">

---

## UnDead (Puzzle Type #11)

* [**Play online**](https://www.chiark.greenend.org.uk/~sgtatham/puzzles/js/undead.html)

* [**Instructions**](https://www.chiark.greenend.org.uk/~sgtatham/puzzles/doc/undead.html#undead)

* [**Solver Code**][11]

<details>
  <summary><strong>Rules</strong></summary>
You are given a grid of squares, some of which contain diagonal mirrors. Every square which is not a mirror must be filled with one of three types of undead monster: a ghost, a vampire, or a zombie.

Vampires can be seen directly, but are invisible when reflected in mirrors. Ghosts are the opposite way round: they can be seen in mirrors, but are invisible when looked at directly. Zombies are visible by any means.

You are also told the total number of each type of monster in the grid. Also around the edge of the grid are written numbers, which indicate how many monsters can be seen if you look into the grid along a row or column starting from that position. (The diagonal mirrors are reflective on both sides. If your reflected line of sight crosses the same monster more than once, the number will count it each time it is visible, not just once.) 
</details>

**Unsolved puzzle**

<img src="./images/undead_unsolved.png" alt="UnDead unsolved" width="500">

Code to utilize this package and solve the puzzle:
```python
import numpy as np
from . import board
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
binst = board.Board(board=bor, sides={'top': t, 'bottom': b, 'right': r, 'left': l}, monster_count=counts)
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

<img src="./images/undead_solved.png" alt="UnDead solved" width="500">

---

## Unruly (Puzzle Type #12)

* [**Play online**](https://www.chiark.greenend.org.uk/~sgtatham/puzzles/js/unruly.html)

* [**Instructions**](https://www.chiark.greenend.org.uk/~sgtatham/puzzles/doc/unruly.html#unruly)

* [**Solver Code**][12]

<details>
  <summary><strong>Rules</strong></summary>
You are given a grid of squares, which you must colour either black or white. Some squares are provided as clues; the rest are left for you to fill in. Each row and column must contain the same number of black and white squares, and no row or column may contain three consecutive squares of the same colour. 
</details>

**Unsolved puzzle**

<img src="./images/unruly_unsolved.png" alt="Unruly unsolved" width="500">

Code to utilize this package and solve the puzzle:
```python
import numpy as np
from . import board
bor = np.array([
  ['W', 'W', '*', 'B', '*', '*', '*', '*', 'B', '*', '*', '*', '*', '*'],
  ['*', '*', '*', '*', '*', '*', '*', 'W', '*', '*', '*', '*', '*', 'W'],
  ['*', '*', '*', '*', '*', 'B', '*', 'W', '*', '*', 'B', '*', '*', '*'],
  ['*', '*', 'W', '*', '*', '*', '*', '*', '*', 'W', '*', 'W', '*', '*'],
  ['B', '*', '*', 'W', '*', '*', '*', '*', 'B', '*', '*', '*', '*', '*'],
  ['*', '*', '*', '*', '*', 'B', '*', '*', '*', 'B', '*', 'B', '*', '*'],
  ['*', 'B', 'B', '*', '*', 'B', '*', '*', '*', '*', '*', 'B', '*', '*'],
  ['*', '*', 'B', '*', '*', '*', '*', 'W', '*', 'B', 'B', '*', '*', 'W'],
  ['*', '*', '*', '*', '*', '*', '*', 'W', '*', '*', '*', '*', '*', 'W'],
  ['*', '*', '*', 'B', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*'],
  ['*', '*', 'W', '*', '*', '*', 'W', '*', '*', 'W', '*', 'W', '*', '*'],
  ['*', 'W', '*', 'W', '*', '*', '*', '*', '*', '*', '*', '*', '*', 'B'],
  ['*', '*', '*', '*', 'B', '*', '*', '*', '*', '*', '*', '*', '*', '*'],
  ['W', '*', '*', '*', 'W', '*', '*', '*', 'B', '*', 'W', '*', 'B', '*'],
])
binst = board.Board(board=bor)
solutions = binst.solve_and_print()
```
**Script Output**
```
Solution found
[['W' 'W' 'B' 'B' 'W' 'B' 'W' 'B' 'B' 'W' 'B' 'W' 'W' 'B']
 ['B' 'B' 'W' 'W' 'B' 'W' 'B' 'W' 'W' 'B' 'W' 'B' 'B' 'W']
 ['W' 'W' 'B' 'W' 'W' 'B' 'B' 'W' 'B' 'W' 'B' 'B' 'W' 'B']
 ['W' 'B' 'W' 'B' 'B' 'W' 'W' 'B' 'W' 'W' 'B' 'W' 'B' 'B']
 ['B' 'W' 'B' 'W' 'B' 'W' 'B' 'W' 'B' 'B' 'W' 'W' 'B' 'W']
 ['B' 'W' 'W' 'B' 'W' 'B' 'B' 'W' 'B' 'B' 'W' 'B' 'W' 'W']
 ['W' 'B' 'B' 'W' 'W' 'B' 'W' 'B' 'W' 'W' 'B' 'B' 'W' 'B']
 ['B' 'W' 'B' 'W' 'B' 'W' 'B' 'W' 'W' 'B' 'B' 'W' 'B' 'W']
 ['B' 'B' 'W' 'B' 'B' 'W' 'B' 'W' 'B' 'W' 'W' 'B' 'W' 'W']
 ['W' 'W' 'B' 'B' 'W' 'B' 'W' 'B' 'W' 'B' 'W' 'W' 'B' 'B']
 ['B' 'B' 'W' 'W' 'B' 'W' 'W' 'B' 'B' 'W' 'B' 'W' 'B' 'W']
 ['B' 'W' 'B' 'W' 'W' 'B' 'B' 'W' 'W' 'B' 'W' 'B' 'W' 'B']
 ['W' 'B' 'W' 'B' 'B' 'W' 'W' 'B' 'W' 'B' 'B' 'W' 'W' 'B']
 ['W' 'B' 'W' 'B' 'W' 'B' 'W' 'B' 'B' 'W' 'W' 'B' 'B' 'W']]
Solutions found: 1
status: OPTIMAL
Time taken: 0.01 seconds
```

**Solved puzzle**

<img src="./images/unruly_solved.png" alt="Unruly solved" width="500">

---

## Mosaic (Puzzle Type #13)

* [**Play online**](https://www.chiark.greenend.org.uk/~sgtatham/puzzles/js/mosaic.html)

* [**Instructions**](https://www.chiark.greenend.org.uk/~sgtatham/puzzles/doc/mosaic.html#mosaic)

* [**Solver Code**][13]

<details>
  <summary><strong>Rules</strong></summary>
You are given a grid of squares, which you must colour either black or white.

Some squares contain clue numbers. Each clue tells you the number of black squares in the 3×3 region surrounding the clue – including the clue square itself. 
</details>

**Unsolved puzzle**

<img src="./images/mosaic_unsolved.png" alt="Mosaic unsolved" width="500">

Code to utilize this package and solve the puzzle:
```python
import numpy as np
from . import board
bor = np.array([
  ['*', '*', '2', '1', '*', '*', '*', '3', '*', '4', '2', '2', '*', '*', '4'],
  ['3', '*', '*', '*', '4', '*', '*', '*', '*', '*', '4', '*', '2', '*', '*'],
  ['4', '*', '*', '5', '*', '5', '*', '*', '5', '*', '3', '3', '2', '5', '*'],
  ['*', '*', '7', '*', '4', '*', '*', '5', '*', '*', '*', '*', '*', '5', '*'],
  ['*', '6', '7', '*', '*', '4', '*', '7', '*', '*', '*', '*', '7', '7', '*'],
  ['3', '*', '*', '3', '*', '5', '7', '7', '6', '4', '*', '4', '*', '5', '*'],
  ['*', '*', '4', '*', '5', '7', '8', '*', '5', '*', '1', '3', '4', '5', '*'],
  ['*', '5', '*', '4', '3', '*', '*', '*', '7', '*', '3', '*', '3', '*', '*'],
  ['3', '*', '*', '*', '*', '*', '*', '5', '*', '6', '*', '*', '*', '*', '*'],
  ['4', '*', '7', '*', '5', '*', '*', '4', '6', '7', '*', '3', '*', '3', '*'],
  ['5', '*', '*', '*', '*', '*', '*', '*', '6', '*', '*', '3', '5', '*', '*'],
  ['*', '*', '*', '5', '4', '5', '3', '*', '7', '*', '*', '5', '6', '6', '*'],
  ['2', '*', '*', '*', '3', '4', '*', '*', '*', '7', '*', '*', '7', '*', '3'],
  ['1', '*', '*', '5', '*', '*', '*', '5', '*', '*', '*', '6', '*', '6', '*'],
  ['*', '*', '3', '*', '2', '*', '3', '*', '2', '*', '*', '*', '*', '*', '*']
])
binst = board.Board(board=bor)
solutions = binst.solve_and_print()
```
**Script Output**
```
Solution found
[[' ' 'B' ' ' ' ' ' ' ' ' ' ' ' ' 'B' ' ' 'B' ' ' ' ' 'B' 'B']
 [' ' 'B' ' ' ' ' 'B' 'B' ' ' 'B' 'B' ' ' 'B' ' ' ' ' 'B' 'B']
 [' ' 'B' 'B' ' ' 'B' 'B' ' ' ' ' ' ' 'B' 'B' ' ' ' ' ' ' 'B']
 ['B' 'B' 'B' 'B' ' ' ' ' 'B' 'B' 'B' ' ' ' ' ' ' 'B' ' ' 'B']
 [' ' 'B' 'B' ' ' ' ' 'B' ' ' 'B' 'B' 'B' ' ' 'B' 'B' 'B' ' ']
 [' ' 'B' ' ' 'B' ' ' 'B' 'B' ' ' 'B' ' ' ' ' 'B' 'B' 'B' 'B']
 ['B' ' ' 'B' ' ' ' ' 'B' 'B' 'B' 'B' ' ' ' ' ' ' ' ' ' ' ' ']
 [' ' ' ' 'B' ' ' 'B' 'B' 'B' 'B' 'B' ' ' ' ' ' ' 'B' ' ' 'B']
 [' ' 'B' 'B' ' ' ' ' ' ' ' ' 'B' 'B' 'B' 'B' 'B' ' ' 'B' ' ']
 ['B' 'B' 'B' 'B' 'B' 'B' ' ' ' ' ' ' 'B' 'B' ' ' ' ' 'B' ' ']
 [' ' 'B' ' ' 'B' 'B' ' ' 'B' ' ' 'B' 'B' ' ' ' ' ' ' 'B' ' ']
 ['B' 'B' ' ' ' ' 'B' ' ' ' ' 'B' 'B' 'B' ' ' 'B' 'B' 'B' 'B']
 [' ' ' ' 'B' ' ' 'B' ' ' 'B' ' ' 'B' 'B' 'B' 'B' 'B' ' ' 'B']
 [' ' ' ' 'B' 'B' ' ' ' ' 'B' ' ' 'B' 'B' ' ' 'B' 'B' ' ' ' ']
 ['B' ' ' 'B' ' ' ' ' 'B' 'B' ' ' ' ' ' ' ' ' ' ' 'B' 'B' 'B']]
Solutions found: 1
status: OPTIMAL
Time taken: 0.01 seconds
```

**Solved puzzle**

<img src="./images/mosaic_solved.png" alt="Mosaic solved" width="500">

---

---

## Quick Start

### 1) Install Python deps

Use a fresh conda environment:

```bash
conda create -p ./env python=3.11
conda activate ./env
pip install -r requirements.txt
````

### 2) Explore a puzzle

Each chapter has runnable scripts and importable modules.

Example: Nonograms (Pattern)
Docs: [https://www.chiark.greenend.org.uk/~sgtatham/puzzles/doc/pattern.html#pattern](https://www.chiark.greenend.org.uk/~sgtatham/puzzles/doc/pattern.html#pattern)

```bash
python -m chapter10_nonograms.test_solve
```

This runs code like:

```python
from . import board
top_numbers = [
  [8, 2],
  ...
  [1, 5],
]  # top clues, omitted here for brevity
side_numbers = [
  [7, 3],
  ...
  [3, 2],
]  # side clues, omitted here for brevity
binst = board.Board(top=top_numbers, side=side_numbers)
solutions = binst.solve_and_print()
```

You’ll see the solution grid and status in the terminal.

---

## Testing

To run the tests, simply follow the instructions in Install Python deps section ([here](#1-install-python-deps)) and then run:

```python -m pytest --import-mode=importlib```

## Contributing

Issues and PRs welcome!


* Python 3.11 recommended.
* Keep puzzle folders self-contained (inputs, solver, simple demo/CLI).
* Prefer small, readable encodings with comments explaining each constraint.
* If you add a new puzzle:

  1. Create `chapterXX_<name>/`,
  2. Add a minimal test script,
  3. Document the modeling in code comments,


[1]: https://github.com/Ar-Kareem/SAT_puzzle_solver/tree/master/chapter10_nonograms "SAT_puzzle_solver/chapter10_nonograms at master · Ar-Kareem/SAT_puzzle_solver · GitHub"
[2]: https://github.com/Ar-Kareem/SAT_puzzle_solver/tree/master/chapter11_sudoku "SAT_puzzle_solver/chapter11_sudoku at master · Ar-Kareem/SAT_puzzle_solver · GitHub"
[3]: https://github.com/Ar-Kareem/SAT_puzzle_solver/tree/master/chapter21_light_up "SAT_puzzle_solver/chapter21_light_up at master · Ar-Kareem/SAT_puzzle_solver · GitHub"
[4]: https://github.com/Ar-Kareem/SAT_puzzle_solver/tree/master/chapter25_tents "SAT_puzzle_solver/chapter25_tents at master · Ar-Kareem/SAT_puzzle_solver · GitHub"
[5]: https://github.com/Ar-Kareem/SAT_puzzle_solver/tree/master/chapter29_filling "SAT_puzzle_solver/chapter29_filling at master · Ar-Kareem/SAT_puzzle_solver · GitHub"
[6]: https://github.com/Ar-Kareem/SAT_puzzle_solver/tree/master/chapter30_keen "SAT_puzzle_solver/chapter30_keen at master · Ar-Kareem/SAT_puzzle_solver · GitHub"
[7]: https://github.com/Ar-Kareem/SAT_puzzle_solver/tree/master/chapter31_towers "SAT_puzzle_solver/chapter31_towers at master · Ar-Kareem/SAT_puzzle_solver · GitHub"
[8]: https://github.com/Ar-Kareem/SAT_puzzle_solver/tree/master/chapter32_singles "SAT_puzzle_solver/chapter32_singles at master · Ar-Kareem/SAT_puzzle_solver · GitHub"
[9]: https://github.com/Ar-Kareem/SAT_puzzle_solver/tree/master/chapter33_magnets "SAT_puzzle_solver/chapter33_magnets at master · Ar-Kareem/SAT_puzzle_solver · GitHub"
[10]: https://github.com/Ar-Kareem/SAT_puzzle_solver/tree/master/chapter35_range "SAT_puzzle_solver/chapter35_range at master · Ar-Kareem/SAT_puzzle_solver · GitHub"
[11]: https://github.com/Ar-Kareem/SAT_puzzle_solver/tree/master/chapter37_undead "SAT_puzzle_solver/chapter37_undead at master · Ar-Kareem/SAT_puzzle_solver · GitHub"
[12]: https://github.com/Ar-Kareem/SAT_puzzle_solver/tree/master/chapter38_unruly "SAT_puzzle_solver/chapter38_unruly at master · Ar-Kareem/SAT_puzzle_solver · GitHub"
[13]: https://github.com/Ar-Kareem/SAT_puzzle_solver/tree/master/chapter42_mosaic "SAT_puzzle_solver/chapter42_mosaic at master · Ar-Kareem/SAT_puzzle_solver · GitHub"