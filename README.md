# Python Puzzle Solver

Solve classic logic puzzles automatically in Python. 

The aim of this repo is to provide very efficient solvers (i.e. not brute force solvers) for many popular pencil logic puzzles like Nonograms, Sudoku, Minesweeper, and many more lesser known ones.

If you happen to have a puzzle similar to the ones listed below and want to solve it (or see how many potential solutions a partially covered board has), then this repo is perfect for you.

The simple use-case of this repo is if you want to solve a puzzle given the state of the board. But other use-cases exist such as checking if removing a clue would still result in a unique solution or would make the puzzle ambiguous and have multiple solutions.

**Why?** There are countless python packages that can solve popular puzzles like the ones below, so a valid question to ask is **why would I want to use this package and why did you create it?**. That is a fair question and the answer is that there are multiple problems with most of those packages that this package solves.

1. **Sophisticated solvers:** A lot of available online solvers are incredibly inefficient as they implement naive algorithms that brute force and backtrack through all possible solutions. This package solves that issue as all the solvers included here never use naive algorithms and instead use a very efficient CP-SAT solver which is a more sophisticated solver than any one person could possibly write.
2. **Numerous puzzles:** Most of the available python solvers are only designed for a single type of puzzle and each one requires a different way to encode the input and extract the solution. This package solves both those issues as this package provides solvers for many puzzles all with a similar interface that encodes the input and extracts the solution in a similar way.
3. **Esoteric puzzles:** Most packages you can find online are only designed for popular puzzles. This package partially solves this issue by providing solvers for many puzzles. I'm open to suggestions for implementing solvers for more puzzles.
4. **All possible solutions:** The available solvers often lack uniqueness checks and simply stop at the first possible solution without verifying uniqueness or completeness. This package supports checking whether puzzles are uniquely solvable, ambiguous, or unsolvable for all the puzzles.

Play the original puzzles online: https://www.chiark.greenend.org.uk/~sgtatham/puzzles

Almost all the solvers in this repo use the CP-SAT solver from Google OR-Tools.

---

## Table of Contents

- [Python Puzzle Solver](#python-puzzle-solver)
  - [Table of Contents](#table-of-contents)
- [Puzzles](#puzzles)
  - [Nonograms (Puzzle Type #1)](#nonograms-puzzle-type-1)
  - [Sudoku (Puzzle Type #2)](#sudoku-puzzle-type-2)
  - [Minesweeper (Puzzle Type #3)](#minesweeper-puzzle-type-3)
  - [Dominosa (Puzzle Type #4)](#dominosa-puzzle-type-4)
  - [Light Up (Puzzle Type #5)](#light-up-puzzle-type-5)
  - [Tents (Puzzle Type #6)](#tents-puzzle-type-6)
  - [Filling (Puzzle Type #7)](#filling-puzzle-type-7)
  - [Keen (Puzzle Type #8)](#keen-puzzle-type-8)
  - [Towers (Puzzle Type #9)](#towers-puzzle-type-9)
  - [Singles (Puzzle Type #10)](#singles-puzzle-type-10)
  - [Magnets (Puzzle Type #11)](#magnets-puzzle-type-11)
  - [Signpost (Puzzle Type #12)](#signpost-puzzle-type-12)
  - [Range (Puzzle Type #13)](#range-puzzle-type-13)
  - [UnDead (Puzzle Type #14)](#undead-puzzle-type-14)
  - [Unruly (Puzzle Type #15)](#unruly-puzzle-type-15)
  - [Tracks (Puzzle Type #16)](#tracks-puzzle-type-16)
  - [Mosaic (Puzzle Type #17)](#mosaic-puzzle-type-17)
  - [Map (Puzzle Type #18)](#map-puzzle-type-18)
  - [Pearl (Puzzle Type #19)](#pearl-puzzle-type-19)
  - [Bridges (Puzzle Type #20)](#bridges-puzzle-type-20)
  - [Inertia (Puzzle Type #21)](#inertia-puzzle-type-21)
  - [Guess (Puzzle Type #22)](#guess-puzzle-type-22)
  - [Quick Start](#quick-start)
    - [1) Install Python deps](#1-install-python-deps)
    - [2) Explore a puzzle](#2-explore-a-puzzle)
  - [Why SAT / CP-SAT?](#why-sat--cp-sat)
  - [What’s Inside](#whats-inside)
  - [Testing](#testing)
  - [Contributing](#contributing)

---

# Puzzles

The puzzles that have solvers implemented are listed below. Each puzzle has a simple example input board followed by the code to utilize this package and solve the puzzle, followed by the scripts output, and finally the solved puzzle.

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
from puzzle_solver import nonograms_solver as solver
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
binst = solver.Board(top=top_numbers, side=side_numbers)
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
from puzzle_solver import sudoku_solver as solver
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
binst = solver.Board(board=bor)
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

## Minesweeper (Puzzle Type #3)

This Minesweeper solver is a bit different from the other solvers in this repo because in Minesweeper is a uniquely different type of puzzle. 

In Minesweeper, you don't solve the puzzle in one go. You need to partially solve the puzzle and get new information to continue. Thus the solver is designed to take the state of the board at any timestep and always gives the most amount of garunteed next steps to take (i.e. garunteed safe positions, garunteed mine positions, and even warns you if you placed a flag in a potentially wrong position).

Then obviously, once the you act upon the guesses and get the new information, you simply put that new info back into the solver and repeat the process until the puzzle is fully solved. 

Below is an example of how to utilize the solver while in the middle of a puzzle. (notice how there's an intentionally placed incorrect flag in the example and the solver will warn you about it)

* [**Play online**](https://www.chiark.greenend.org.uk/~sgtatham/puzzles/js/mines.html)

* [**Instructions**](https://www.chiark.greenend.org.uk/~sgtatham/puzzles/doc/mines.html#mines)

* [**Solver Code**][3]

<details>
  <summary><strong>Rules</strong></summary>
You have a grid of covered squares, some of which contain mines, but you don't know which. Your job is to uncover every square which does not contain a mine. If you uncover a square containing a mine, you lose. If you uncover a square which does not contain a mine, you are told how many mines are contained within the eight surrounding squares.

This game needs no introduction; popularised by Windows, it is perhaps the single best known desktop puzzle game in existence.

This version of it has an unusual property. By default, it will generate its mine positions in such a way as to ensure that you never need to guess where a mine is: you will always be able to deduce it somehow. So you will never, as can happen in other versions, get to the last four squares and discover that there are two mines left but you have no way of knowing for sure where they are. 
</details>

**Partially solved puzzle**

<img src="./images/minesweeper_pre.png" alt="Minesweeper partially solved" width="500">

Code to utilize this package and solve the puzzle:
```python
import numpy as np
from puzzle_solver import minesweeper_solver as solver
bor = np.array([
  [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '1', '1', '1', '3', 'F', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
  [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '2', '2', '1', 'F', '4', 'F', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
  [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'F', '2', '1', '3', 'F', '5', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
  [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '2', '4', 'F', '3', '0', '3', 'F', 'F', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
  [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '3', '4', 'F', '3', '0', '2', 'F', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
  [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'F', '4', 'F', '2', '0', '2', '3', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
  [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'F', '4', '1', '1', '0', '1', 'F', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
  [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'F', '4', '2', '1', '1', '2', '2', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
  [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
  [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
  [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
  [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
  [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
  [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
  [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
  [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
])
mine_count = 30
safe_positions, new_garuneed_mine_positions, wrong_flag_positions = solver.give_next_guess(board=bor, mine_count=mine_count)
```
**Script Output**
```
Found 8 new guaranteed safe positions
{Pos(x=9, y=0), Pos(x=15, y=8), Pos(x=15, y=7), Pos(x=9, y=2), Pos(x=15, y=6), Pos(x=7, y=2), Pos(x=9, y=1), Pos(x=12, y=8)}
----------
Found 4 new guaranteed mine positions
{Pos(x=8, y=2), Pos(x=7, y=5), Pos(x=10, y=0), Pos(x=9, y=8)}
----------
WARNING | WARNING | WARNING | WARNING | WARNING
Found 1 wrong flag positions
{Pos(x=15, y=3)}
----------
Time taken: 0.92 seconds
```

**Progressed puzzle**

<img src="./images/minesweeper_post.png" alt="Minesweeper progressed" width="500">

---

## Dominosa (Puzzle Type #4)

* [**Play online**](https://www.chiark.greenend.org.uk/~sgtatham/puzzles/js/dominosa.html)

* [**Instructions**](https://www.chiark.greenend.org.uk/~sgtatham/puzzles/doc/dominosa.html#dominosa)

* [**Solver Code**][4]

<details>
  <summary><strong>Rules</strong></summary>
A normal set of dominoes – that is, one instance of every (unordered) pair of numbers from 0 to N – has been arranged irregularly into a rectangle; then the number in each square has been written down and the dominoes themselves removed. 

Your task is to reconstruct the pattern by arranging the set of dominoes to match the provided array of numbers. 
</details>

**Unsolved puzzle**

<img src="./images/dominosa_unsolved.png" alt="Dominosa unsolved" width="500">

Code to utilize this package and solve the puzzle:
```python
import numpy as np
from puzzle_solver import dominosa_solver as solver
bor = np.array([
  [6, 8, 2, 7, 1, 3, 3, 4, 6, 6, 0],
  [4, 9, 5, 6, 1, 0, 6, 1, 2, 2, 4],
  [8, 2, 8, 9, 1, 9, 3, 3, 8, 8, 5],
  [1, 1, 7, 3, 4, 7, 0, 8, 7, 7, 7],
  [4, 5, 3, 9, 9, 3, 0, 1, 6, 1, 5],
  [6, 9, 5, 8, 9, 2, 1, 2, 6, 7, 9],
  [2, 7, 4, 3, 5, 5, 9, 6, 4, 0, 9],
  [0, 7, 8, 0, 5, 4, 2, 7, 6, 7, 3],
  [0, 4, 5, 2, 8, 6, 1, 0, 9, 0, 4],
  [0, 8, 8, 3, 2, 1, 3, 2, 5, 5, 4],
])
binst = solver.Board(board=bor)
solutions = binst.solve_and_print()
assert len(solutions) == 1, f'unique solutions != 1, == {len(solutions)}'
```
**Script Output**
```
Solution found
[['R' 'L' 'R' 'L' 'D' 'R' 'L' 'R' 'L' 'R' 'L']
 ['D' 'D' 'R' 'L' 'U' 'D' 'D' 'D' 'R' 'L' 'D']
 ['U' 'U' 'D' 'R' 'L' 'U' 'U' 'U' 'R' 'L' 'U']
 ['D' 'D' 'U' 'D' 'D' 'R' 'L' 'D' 'R' 'L' 'D']
 ['U' 'U' 'D' 'U' 'U' 'R' 'L' 'U' 'D' 'D' 'U']
 ['D' 'D' 'U' 'R' 'L' 'D' 'R' 'L' 'U' 'U' 'D']
 ['U' 'U' 'R' 'L' 'D' 'U' 'R' 'L' 'R' 'L' 'U']
 ['D' 'D' 'D' 'D' 'U' 'R' 'L' 'R' 'L' 'R' 'L']
 ['U' 'U' 'U' 'U' 'D' 'D' 'R' 'L' 'D' 'D' 'D']
 ['R' 'L' 'R' 'L' 'U' 'U' 'R' 'L' 'U' 'U' 'U']]
Solutions found: 1
status: OPTIMAL
Time taken: 0.02 seconds
```

**Solved puzzle**

<img src="./images/dominosa_solved.png" alt="Dominosa solved" width="500">

---

## Light Up (Puzzle Type #5)

* [**Play online**](https://www.chiark.greenend.org.uk/~sgtatham/puzzles/js/lightup.html)

* [**Instructions**](https://www.chiark.greenend.org.uk/~sgtatham/puzzles/doc/lightup.html#lightup)

* [**Solver Code**][5]

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
from puzzle_solver import light_up_solver as solver
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

<img src="./images/lightup_solved.png" alt="Light Up solved" width="500">

---

## Tents (Puzzle Type #6)

* [**Play online**](https://www.chiark.greenend.org.uk/~sgtatham/puzzles/js/tents.html)

* [**Instructions**](https://www.chiark.greenend.org.uk/~sgtatham/puzzles/doc/tents.html#tents)

* [**Solver Code**][6]

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
from puzzle_solver import tents_solver as solver
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

binst = solver.Board(board=bor, sides={'top': top, 'side': side})
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

## Filling (Puzzle Type #7)

* [**Play online**](https://www.chiark.greenend.org.uk/~sgtatham/puzzles/js/filling.html)

* [**Instructions**](https://www.chiark.greenend.org.uk/~sgtatham/puzzles/doc/filling.html#filling)

* [**Solver Code**][7]

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
from puzzle_solver import filling_solver as solver
bor = np.array([
  ['*', '4', '2', '*', '*', '2', '*'],
  ['*', '*', '7', '*', '*', '3', '*'],
  ['*', '*', '*', '*', '4', '*', '3'],
  ['*', '6', '6', '*', '3', '*', '*'],
  ['*', '7', '*', '6', '4', '5', '*'],
  ['*', '6', '*', '*', '*', '*', '4'],
])
binst = solver.Board(board=bor)
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

## Keen (Puzzle Type #8)

* [**Play online**](https://www.chiark.greenend.org.uk/~sgtatham/puzzles/js/keen.html)

* [**Instructions**](https://www.chiark.greenend.org.uk/~sgtatham/puzzles/doc/keen.html#keen)

* [**Solver Code**][8]

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

  Note that a block may contain the same digit more than once (provided the identical ones are not in the same row and column).
</details>

**Unsolved puzzle**

<img src="./images/keen_unsolved.png" alt="Keen unsolved" width="500">

Code to utilize this package and solve the puzzle:
```python
import numpy as np
from puzzle_solver import keen_solver as solver
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

<img src="./images/keen_solved.png" alt="Keen solved" width="500">

---

## Towers (Puzzle Type #9)

* [**Play online**](https://www.chiark.greenend.org.uk/~sgtatham/puzzles/js/towers.html)

* [**Instructions**](https://www.chiark.greenend.org.uk/~sgtatham/puzzles/doc/towers.html#towers)

* [**Solver Code**][9]

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
from puzzle_solver import towers_solver as solver
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
binst = solver.Board(board=bor, sides={'top': t, 'bottom': b, 'right': r, 'left': l})
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

## Singles (Puzzle Type #10)

* [**Play online**](https://www.chiark.greenend.org.uk/~sgtatham/puzzles/js/singles.html)

* [**Instructions**](https://www.chiark.greenend.org.uk/~sgtatham/puzzles/doc/singles.html#singles)

* [**Solver Code**][10]

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
from puzzle_solver import singles_solver as solver
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
binst = solver.Board(board=bor)
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

## Magnets (Puzzle Type #11)

* [**Play online**](https://www.chiark.greenend.org.uk/~sgtatham/puzzles/js/magnets.html)

* [**Instructions**](https://www.chiark.greenend.org.uk/~sgtatham/puzzles/doc/magnets.html#magnets)

* [**Solver Code**][11]

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
from puzzle_solver import magnets_solver as solver
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

binst = solver.Board(board=bor, sides={'pos_v': pos_v, 'neg_v': neg_v, 'pos_h': pos_h, 'neg_h': neg_h})
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

## Signpost (Puzzle Type #12)

* [**Play online**](https://www.chiark.greenend.org.uk/~sgtatham/puzzles/js/signpost.html)

* [**Instructions**](https://www.chiark.greenend.org.uk/~sgtatham/puzzles/doc/signpost.html#signpost)

* [**Solver Code**][12]

<details>
  <summary><strong>Rules</strong></summary>
You have a grid of squares; each square (except the last one) contains an arrow, and some squares also contain numbers. Your job is to connect the squares to form a continuous list of numbers starting at 1 and linked in the direction of the arrows – so the arrow inside the square with the number 1 will point to the square containing the number 2, which will point to the square containing the number 3, etc. Each square can be any distance away from the previous one, as long as it is somewhere in the direction of the arrow.

By convention the first and last numbers are shown; one or more interim numbers may also appear at the beginning. 
</details>

**Unsolved puzzle**

<img src="./images/signpost_unsolved.png" alt="Signpost unsolved" width="500">

Code to utilize this package and solve the puzzle:
```python
import numpy as np
from puzzle_solver import signpost_solver as solver
# Q = up-left, W = up, E = up-right, A = left, D = right, Z = down-left, X = down, C = down-right
bor1 = np.array([
  ['C', 'D', 'D', 'X', 'D', 'Z', 'X'],
  ['D', 'C', 'D', 'X', 'X', 'A', 'A'],
  ['X', 'X', 'D', 'Q', 'Z', 'W', 'A'],
  ['W', 'D', 'W', 'W', 'X', 'Z', 'X'],
  ['X', 'A', 'Q', 'Q', 'A', 'Q', 'X'],
  ['D', 'W', 'W', 'A', 'E', 'A', 'Z'],
  ['D', 'E', 'D', 'E', 'D', 'A', ' '],
])
bor2 = np.array([
  [ 1,  0, 23,  0,  0,  0,  0],
  [30, 32,  0,  0,  0,  0,  0],
  [ 0,  0,  2,  0,  0,  0,  0],
  [ 0,  0,  0,  0,  0,  0,  0],
  [ 0, 45,  0,  0, 33,  0,  0],
  [ 0,  0, 22,  8, 39, 10,  0],
  [ 0,  0,  0,  0,  0, 20, 49],
])

binst = solver.Board(board=bor1, values=bor2)
solutions = binst.solve_and_print()
```
**Script Output**
```
Solution found
[[1 42 23 7 43 44 24]
 [30 32 36 5 37 4 31]
 [28 12 2 41 26 3 25]
 [29 13 35 6 38 14 17]
 [46 45 27 34 33 40 18]
 [9 11 22 8 39 10 19]
 [47 21 15 16 48 20 49]]
Solutions found: 1
status: OPTIMAL
Time taken: 0.03 seconds
```

**Solved puzzle**

<img src="./images/signpost_solved.png" alt="Signpost solved" width="500">


---

## Range (Puzzle Type #13)

* [**Play online**](https://www.chiark.greenend.org.uk/~sgtatham/puzzles/js/range.html)

* [**Instructions**](https://www.chiark.greenend.org.uk/~sgtatham/puzzles/doc/range.html#range)

* [**Solver Code**][13]

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
from puzzle_solver import range_solver as solver
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
binst = solver.Board(clues)
solutions = binst.solve_and_print()
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

## UnDead (Puzzle Type #14)

* [**Play online**](https://www.chiark.greenend.org.uk/~sgtatham/puzzles/js/undead.html)

* [**Instructions**](https://www.chiark.greenend.org.uk/~sgtatham/puzzles/doc/undead.html#undead)

* [**Solver Code**][14]

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

<img src="./images/undead_solved.png" alt="UnDead solved" width="500">

---

## Unruly (Puzzle Type #15)

* [**Play online**](https://www.chiark.greenend.org.uk/~sgtatham/puzzles/js/unruly.html)

* [**Instructions**](https://www.chiark.greenend.org.uk/~sgtatham/puzzles/doc/unruly.html#unruly)

* [**Solver Code**][15]

<details>
  <summary><strong>Rules</strong></summary>
You are given a grid of squares, which you must colour either black or white. Some squares are provided as clues; the rest are left for you to fill in. Each row and column must contain the same number of black and white squares, and no row or column may contain three consecutive squares of the same colour. 
</details>

**Unsolved puzzle**

<img src="./images/unruly_unsolved.png" alt="Unruly unsolved" width="500">

Code to utilize this package and solve the puzzle:
```python
import numpy as np
from puzzle_solver import unruly_solver as solver
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
binst = solver.Board(board=bor)
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

## Tracks (Puzzle Type #16)

* [**Play online**](https://www.chiark.greenend.org.uk/~sgtatham/puzzles/js/tracks.html)

* [**Instructions**](https://www.chiark.greenend.org.uk/~sgtatham/puzzles/doc/tracks.html#tracks)

* [**Solver Code**][16]

<details>
  <summary><strong>Rules</strong></summary>
Complete the track from A to B so that the rows and columns contain the same number of track segments as are indicated in the clues to the top and right of the grid. There are only straight and 90-degree curved rail sections, and the track may not cross itself. 

</details>

(Note: The solver for this puzzle is slightly slower and could take several seconds to solve a large 15x15 puzzle)

**Unsolved puzzle**

<img src="./images/tracks_unsolved.png" alt="Tracks unsolved" width="500">

Code to utilize this package and solve the puzzle:
```python
import numpy as np
from puzzle_solver import tracks_solver as solver
bor = np.array([
  ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', 'LD', '  ', '  ', ], 
  ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', 'LD', '  ', '  ', '  ', '  ', ], 
  ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', ], 
  ['  ', '  ', '  ', '  ', '  ', 'LD', 'UD', 'DR', '  ', '  ', '  ', '  ', '  ', '  ', '  ', ], 
  ['DR', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', ], 
  ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', 'DR', '  ', '  ', ], 
  ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', 'DR', '  ', '  ', '  ', '  ', '  ', '  ', ], 
  ['  ', '  ', 'UL', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', ], 
  ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', 'LR', '  ', '  ', '  ', '  ', ], 
  ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', 'LD', '  ', '  ', '  ', 'UD', ], 
  ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', 'UR', '  ', '  ', '  ', '  ', 'UD', 'UD', ], 
  ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', 'LR', '  ', '  ', '  ', '  ', '  ', ], 
  ['UL', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', 'LR', 'LR', '  ', '  ', '  ', ], 
  ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', ], 
  ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', 'DR', '  ', ], 
])
side = np.array([9, 7, 7, 7, 11, 10, 9, 8, 9, 10, 7, 9, 9, 2, 2])
top = np.array([6, 5, 7, 3, 3, 2, 7, 8, 13, 8, 9, 8, 10, 13, 14])
binst = solver.Board(board=bor, top=top, side=side)
solutions = binst.solve_and_print()
```
**Script Output**
```
[['  ' '  ' '  ' '  ' '  ' '  ' '┏━' '━━' '━━' '━━' '━━' '━━' '━┒' '┏━' '━┒']
 ['  ' '  ' '  ' '  ' '  ' '  ' '┃ ' '  ' '┏━' '━━' '━┒' '  ' '┗━' '━┛' '┃ ']
 ['  ' '  ' '  ' '  ' '  ' '  ' '┃ ' '  ' '┃ ' '  ' '┗━' '━━' '━━' '━━' '━┛']
 ['  ' '  ' '┏━' '━┒' '┏━' '━┒' '┃ ' '┏━' '━┛' '  ' '  ' '  ' '  ' '  ' '  ']
 ['┏━' '━━' '━┛' '┃ ' '┃ ' '┗━' '━┛' '┗━' '━┒' '  ' '  ' '  ' '  ' '┏━' '━┒']
 ['┗━' '━━' '━┒' '┗━' '━┛' '  ' '  ' '┏━' '━┛' '  ' '  ' '  ' '┏━' '━┛' '┃ ']
 ['  ' '  ' '┃ ' '  ' '  ' '  ' '┏━' '━┛' '┏━' '━━' '━━' '━━' '━┛' '  ' '┃ ']
 ['  ' '┏━' '━┛' '  ' '  ' '  ' '┗━' '━━' '━┛' '  ' '  ' '  ' '┏━' '━━' '━┛']
 ['  ' '┗━' '━┒' '  ' '  ' '  ' '  ' '  ' '┏━' '━━' '━━' '━┒' '┃ ' '┏━' '━┒']
 ['┏━' '━━' '━┛' '  ' '  ' '  ' '  ' '  ' '┃ ' '┏━' '━┒' '┗━' '━┛' '┃ ' '┃ ']
 ['┃ ' '  ' '  ' '  ' '  ' '  ' '  ' '  ' '┗━' '━┛' '┗━' '━┒' '  ' '┃ ' '┃ ']
 ['┃ ' '  ' '  ' '  ' '  ' '  ' '  ' '┏━' '━━' '━━' '━━' '━┛' '┏━' '━┛' '┃ ']
 ['━┛' '  ' '  ' '  ' '  ' '  ' '  ' '┗━' '━━' '━━' '━━' '━━' '━┛' '┏━' '━┛']
 ['  ' '  ' '  ' '  ' '  ' '  ' '  ' '  ' '  ' '  ' '  ' '  ' '  ' '┗━' '━┒']
 ['  ' '  ' '  ' '  ' '  ' '  ' '  ' '  ' '  ' '  ' '  ' '  ' '  ' '┏━' '━┛']]
Solutions found: 1
status: OPTIMAL
Time taken: 9.42 seconds
```

**Solved puzzle**

<img src="./images/tracks_solved.png" alt="Tracks solved" width="500">

---

## Mosaic (Puzzle Type #17)

* [**Play online**](https://www.chiark.greenend.org.uk/~sgtatham/puzzles/js/mosaic.html)

* [**Instructions**](https://www.chiark.greenend.org.uk/~sgtatham/puzzles/doc/mosaic.html#mosaic)

* [**Solver Code**][17]

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
from puzzle_solver import mosaic_solver as solver
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
binst = solver.Board(board=bor)
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

## Map (Puzzle Type #18)

* [**Play online**](https://www.chiark.greenend.org.uk/~sgtatham/puzzles/js/map.html)

* [**Instructions**](https://www.chiark.greenend.org.uk/~sgtatham/puzzles/doc/map.html#map)

* [**Solver Code**][18]

<details>
  <summary><strong>Rules</strong></summary>
You are given a map consisting of a number of regions. Your task is to colour each region with one of four colours, in such a way that no two regions sharing a boundary have the same colour. You are provided with some regions already coloured, sufficient to make the remainder of the solution unique, and these cannot be changed.

Only regions which share a length of border are required to be different colours. Two regions which meet at only one point (i.e. are diagonally separated) may be the same colour. 
</details>

**Unsolved puzzle**

<img src="./images/map_unsolved.png" alt="Map unsolved" width="500">

Code to utilize this package and solve the puzzle:
```python
from puzzle_solver import map_solver as solver
regions = {
  0: {1, 11, 12, 27},
  1: {11, 12, 13, 6, 2},
  2: {3, 4, 6, 7, 9, 10},
  # ...
  # ...
  37: {38, 46, 49, 51, 54, 59, 60, 61},
  38: {44, 45, 49, 51, 53, 58, 59},
  39: {40, 46},
  40: {55, 56},
  41: {42, 47},
  42: {48},
  # ...
  # ...
  # ommited for brevity ; this was a pain to type out by hand
}
fixed_colors = {
  0: 'Y', 3: 'R', 7: 'Y', 14: 'Y', 15: 'R', 16: 'Y', 20: 'G', 32: 'B', 33: 'Y', 34: 'R', 35: 'G',
  36: 'B', 39: 'G', 43: 'G', 47: 'R', 55: 'B', 60: 'R', 64: 'G', 66: 'Y', 67: 'G', 73: 'G', 74: 'G',
}
binst = solver.Board(regions=regions, fixed_colors=fixed_colors)
solutions = binst.solve_and_print()
```
**Script Output**
```
Solution found
{0: 'Y', 1: 'R', 2: 'G', 3: 'R', 4: 'B', 5: 'G', 6: 'B', 7: 'Y', 8: 'R', 9: 'Y', 10: 'B', 11: 'G', 12: 'B', 13: 'G', 14: 'Y', 15: 'R', 16: 'Y', 17: 'R', 18: 'G', 19: 'B', 20: 'G', 21: 'Y', 22: 'R', 23: 'Y', 24: 'Y', 25: 'B', 26: 'R', 27: 'G', 28: 'G', 29: 'B', 30: 'B', 31: 'R', 32: 'B', 33: 'Y', 34: 'R', 35: 'G', 36: 'B', 37: 'G', 38: 'B', 39: 'G', 40: 'Y', 41: 'Y', 42: 'R', 43: 'G', 44: 'R', 45: 'Y', 46: 'Y', 47: 'R', 48: 'Y', 49: 'Y', 50: 'G', 51: 'R', 52: 'R', 53: 'Y', 54: 'B', 55: 'B', 56: 'G', 57: 'B', 58: 'R', 59: 'Y', 60: 'R', 61: 'B', 62: 'B', 63: 'Y', 64: 'G', 65: 'R', 66: 'Y', 67: 'G', 68: 'B', 69: 'R', 70: 'Y', 71: 'R', 72: 'B', 73: 'G', 74: 'G'}
Solutions found: 1
status: OPTIMAL
Time taken: 0.01 seconds
```

**Solved puzzle**

<img src="./images/map_solved.png" alt="Map solved" width="500">

---

## Pearl (Puzzle Type #19)

* [**Play online**](https://www.chiark.greenend.org.uk/~sgtatham/puzzles/js/pearl.html)

* [**Instructions**](https://www.chiark.greenend.org.uk/~sgtatham/puzzles/doc/pearl.html#pearl)

* [**Solver Code**][19]

<details>
  <summary><strong>Rules</strong></summary>
You have a grid of squares. Your job is to draw lines between the centres of horizontally or vertically adjacent squares, so that the lines form a single closed loop. In the resulting grid, some of the squares that the loop passes through will contain corners, and some will be straight horizontal or vertical lines. (And some squares can be completely empty – the loop doesn't have to pass through every square.)

Some of the squares contain black and white circles, which are clues that the loop must satisfy.

A black circle in a square indicates that that square is a corner, but neither of the squares adjacent to it in the loop is also a corner.

A white circle indicates that the square is a straight edge, but at least one of the squares adjacent to it in the loop is a corner.

(In both cases, the clue only constrains the two squares adjacent in the loop, that is, the squares that the loop passes into after leaving the clue square. The squares that are only adjacent in the grid are not constrained.)
</details>

**Unsolved puzzle**

<img src="./images/pearl_unsolved.png" alt="Pearl unsolved" width="500">

Code to utilize this package and solve the puzzle:
```python
import numpy as np
from puzzle_solver import pearl_solver as solver
bor = np.array([
  ['B', ' ', ' ', 'W', ' ', ' ', 'W', ' ', 'B', ' ', ' ', 'B'],
  [' ', ' ', ' ', 'B', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
  [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'B', ' ', ' ', ' '],
  [' ', 'B', ' ', 'B', ' ', 'W', ' ', 'B', ' ', 'B', 'W', ' '],
  [' ', ' ', 'B', ' ', 'B', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
  [' ', ' ', ' ', ' ', ' ', ' ', ' ', 'W', 'W', ' ', ' ', 'B'],
  [' ', ' ', 'B', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
  ['B', ' ', ' ', ' ', ' ', 'B', 'B', ' ', ' ', ' ', ' ', 'B'],
])
binst = solver.Board(bor)
solutions = binst.solve_and_print()
```
**Script Output**
```
Solution found
[['┏━' '━━' '━━' '━━' '━┒' '┏━' '━━' '━┒' '┏━' '━━' '━━' '━┒']
 ['┃ ' '┏━' '━━' '━┒' '┗━' '━┛' '┏━' '━┛' '┃ ' '┏━' '━┒' '┃ ']
 ['┗━' '━┛' '  ' '┃ ' '┏━' '━┒' '┗━' '━━' '━┛' '┃ ' '┃ ' '┃ ']
 ['  ' '┏━' '━━' '━┛' '┃ ' '┃ ' '  ' '┏━' '━━' '━┛' '┃ ' '┃ ']
 ['  ' '┃ ' '┏━' '━━' '━┛' '┗━' '━┒' '┃ ' '┏━' '━┒' '┗━' '━┛']
 ['┏━' '━┛' '┃ ' '  ' '┏━' '━┒' '┃ ' '┃ ' '┃ ' '┗━' '━━' '━┒']
 ['┃ ' '  ' '┗━' '━━' '━┛' '┃ ' '┃ ' '┗━' '━┛' '  ' '  ' '┃ ']
 ['┗━' '━━' '━━' '━━' '━━' '━┛' '┗━' '━━' '━━' '━━' '━━' '━┛']]
Solutions found: 1
status: OPTIMAL
Time taken: 0.98 seconds
```

**Solved puzzle**

<img src="./images/pearl_solved.png" alt="Pearl solved" width="500">

---

## Bridges (Puzzle Type #20)

* [**Play online**](https://www.chiark.greenend.org.uk/~sgtatham/puzzles/js/bridges.html)

* [**Instructions**](https://www.chiark.greenend.org.uk/~sgtatham/puzzles/doc/bridges.html#bridges)

* [**Solver Code**][20]

<details>
  <summary><strong>Rules</strong></summary>
You have a set of islands distributed across the playing area. Each island contains a number. Your aim is to connect the islands together with bridges, in such a way that:

  - Bridges run horizontally or vertically.
  - The number of bridges terminating at any island is equal to the number written in that island.
  - Two bridges may run in parallel between the same two islands, but no more than two may do so.
  - No bridge crosses another bridge.
  - All the islands are connected together.

There are some configurable alternative modes, which involve changing the parallel-bridge limit to something other than 2
</details>

**Unsolved puzzle**

<img src="./images/bridges_unsolved.png" alt="Bridges unsolved" width="500">

Code to utilize this package and solve the puzzle:
```python
import numpy as np
from puzzle_solver import bridges_solver as solver
bor = np.array([
  [' ', ' ', ' ', ' ', ' ', '1', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '3'],
  ['2', ' ', ' ', ' ', ' ', ' ', ' ', '4', ' ', ' ', '4', ' ', ' ', '2', ' '],
  [' ', ' ', ' ', '2', ' ', '4', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
  [' ', '1', ' ', ' ', ' ', ' ', ' ', ' ', '1', ' ', '2', ' ', ' ', ' ', '4'],
  [' ', '2', ' ', '3', ' ', '6', ' ', '4', ' ', ' ', '3', ' ', '1', ' ', ' '],
  ['2', ' ', ' ', ' ', '2', ' ', ' ', ' ', '1', ' ', ' ', '2', ' ', ' ', ' '],
  [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
  ['2', ' ', ' ', ' ', ' ', ' ', '5', ' ', ' ', '3', ' ', '4', ' ', ' ', ' '],
  [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
  [' ', '3', ' ', ' ', ' ', '3', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
  [' ', ' ', '2', ' ', '2', ' ', ' ', ' ', ' ', ' ', ' ', '5', ' ', ' ', '4'],
  [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
  [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
  [' ', ' ', '1', ' ', ' ', '2', ' ', ' ', ' ', '1', ' ', '2', ' ', ' ', ' '],
  [' ', '4', ' ', ' ', '4', ' ', '3', ' ', ' ', ' ', '4', ' ', ' ', ' ', '4'],
])
binst = solver.Board(bor)
solutions = binst.solve_and_print()
```
**Script Output**

Note that the four numbers indicate how many bridges in the 4 directions (right, left, down, up) respectively.
```
Solution found
|    |    |    |    |    |1000|    |    |    |    |    |    |    |    |0120|

|1010|    |    |    |    |    |    |2110|    |    |2200|    |    |0200|    |

|    |    |    |2000|    |0220|    |    |    |    |    |    |    |    |    |

|    |0010|    |    |    |    |    |    |1000|    |1100|    |    |    |0112|

|    |1001|    |2100|    |2202|    |1201|    |    |1110|    |0100|    |    |

|1001|    |    |    |1100|    |    |    |0100|    |    |0020|    |    |    |

|    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |

|2000|    |    |    |    |    |2210|    |    |0210|    |0022|    |    |    |

|    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |

|    |1020|    |    |    |0120|    |    |    |    |    |    |    |    |    |

|    |    |1010|    |0110|    |    |    |    |    |    |1022|    |    |0121|

|    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |

|    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |

|    |    |0001|    |    |0002|    |    |    |0001|    |0002|    |    |    |

|    |2002|    |    |1201|    |1101|    |    |    |2101|    |    |    |0202|

Solutions found: 1
status: OPTIMAL
Time taken: 0.01 seconds
```

**Solved puzzle**

<img src="./images/bridges_solved.png" alt="Bridges solved" width="500">

---

## Inertia (Puzzle Type #21)

This solver is a bit different from the other solvers in this repo because this game does not have a unique solution (you simply move the ball to collect all the gems).

Thus the solver was developed with the additional much harder goal of collecting all the gems with the least number of moves.

It does so using the following high level steps:

1. Model the board as a directed graph where the cells are nodes and legal moves as directed edges with unit cost. Each gem has to a group of edges where traversing any one of them collects that gem.
2. Model step (1) as a [Generalized Traveling Salesman Problem (GTSP)](https://en.wikipedia.org/wiki/Set_TSP_problem), where each gem’s edge group forms a cluster.
3. Apply the [Noon–Bean transformation](https://deepblue.lib.umich.edu/bitstream/handle/2027.42/6834/ban3102.0001.001.pdf?sequence=5) **(Noon & Bean, 1991)** to convert the GTSP from step (2) into an equivalent Asymmetric TSP (ATSP) that can be solved with OR-Tools’ routing solver. (Noon-Bean transformation is mentioned but not described in the [TSP wikipedia page](https://en.wikipedia.org/wiki/Travelling_salesman_problem).)
4. Use a [Vehicle Routing Problem (VRP)](https://en.wikipedia.org/wiki/Vehicle_routing_problem) solver using the [OR-Tools VRP solver](https://developers.google.com/optimization/routing/routing_tasks) to solve the ATSP.

This achieves a final sequence of moves that is empirically always faster than the website's solution.

* [**Play online**](https://www.chiark.greenend.org.uk/~sgtatham/puzzles/js/inertia.html)

* [**Instructions**](https://www.chiark.greenend.org.uk/~sgtatham/puzzles/doc/inertia.html#inertia)

* [**Solver Code**][21]

<details>
  <summary><strong>Rules</strong></summary>
You are a small green ball sitting in a grid full of obstacles. Your aim is to collect all the gems without running into any mines.

You can move the ball in any orthogonal or diagonal direction. Once the ball starts moving, it will continue until something stops it. A wall directly in its path will stop it (but if it is moving diagonally, it will move through a diagonal gap between two other walls without stopping). Also, some of the squares are ‘stops’; when the ball moves on to a stop, it will stop moving no matter what direction it was going in. Gems do not stop the ball; it picks them up and keeps on going.

Running into a mine is fatal. Even if you picked up the last gem in the same move which then hit a mine, the game will count you as dead rather than victorious. 
</details>

**Unsolved puzzle**

<img src="./images/inertia_unsolved.png" alt="Inertia unsolved" width="500">

Code to utilize this package and solve the puzzle:

(Note: there is a script that parses a screenshot of the board and outputs the below array that the solver uses. The script uses classical computer vision techniques and is called `parse_map.py`)
```python
import numpy as np
from puzzle_solver import inertia_solver as solver
bor = np.array([
  ["O", "O", "M", " ", "G", "O", "G", "O", " ", " ", "M", " ", " ", "O", "G", "G", "W", "O", "O", "O"],
  ["O", " ", "W", " ", "W", "O", "G", "M", " ", " ", " ", "G", "M", "O", "W", "G", " ", "M", "M", "O"],
  ["O", "M", "O", "O", " ", "M", " ", "W", "W", "M", "G", "W", " ", " ", "G", " ", "W", "G", "O", "G"],
  ["O", " ", "O", "M", "G", "O", "W", "G", "M", "O", " ", " ", "G", "G", "G", " ", "M", "W", "M", "O"],
  ["M", "M", "O", "G", " ", "W", " ", " ", "O", "G", " ", "M", "M", " ", "W", "W", " ", "W", "W", "O"],
  ["G", " ", "G", "W", "M", "W", "W", " ", "G", "G", "W", "M", "G", "G", " ", "G", "O", "O", "M", "M"],
  ["M", " ", "M", " ", "W", "W", "M", "M", "M", "O", "M", "G", "O", "M", "M", "W", "B", "O", "W", "M"],
  ["G", "G", " ", "W", "M", "M", "W", "O", "W", "G", "W", "O", "O", "M", " ", "W", "W", "G", "G", "M"],
  [" ", "M", "M", " ", " ", " ", "G", "G", "M", "O", "M", "O", "M", "G", "W", "M", "W", " ", "O", " "],
  ["G", " ", "M", " ", " ", " ", "W", "O", "W", "W", "M", "M", "G", "W", " ", " ", "W", "M", "G", "W"],
  ["G", "O", "M", "M", "G", "M", "W", "O", "O", "G", "W", "M", "M", "G", "G", " ", "O", " ", "W", "W"],
  ["G", "G", "W", "G", "M", " ", "G", "W", "W", " ", "G", " ", "O", "W", "G", "G", "O", " ", "M", "M"],
  ["W", "M", "O", " ", "W", "O", "O", "M", "M", "O", "G", "W", " ", "G", "O", "G", "G", "O", "O", "W"],
  ["W", "W", "W", " ", "W", "O", "W", "M", "O", "M", "G", "O", "O", " ", " ", "W", "W", "G", "W", "W"],
  ["O", "W", "O", "M", "O", "G", " ", "O", "O", "M", "O", " ", "M", "M", "O", "G", "W", "G", "M", " "],
  ["M", "G", "O", "G", "O", "G", "O", "G", " ", "W", "W", "G", "O", " ", "W", "M", "G", " ", "W", " "]
])
start_pos, edges, edges_to_direction, gems_to_edges = solver.parse_nodes_and_edges(bor)
optimal_walk = solver.solve_optimal_walk(start_pos, edges, gems_to_edges)
moves = solver.get_moves_from_walk(optimal_walk, edges_to_direction, verbose=True)
```
**Script Output**

Note that the output is the sequence of moves to collect all the gems. This particular solution is 106 moves, which is 15 moves better than the website's solution.
```
number of moves 106
↗ ↖ ↖ ↙ ↙ ↖ ↖ ↙ → ↘ 
↙ → ↖ → ↙ ↓ → ↘ ↗ ↓
↘ → ↘ ↓ ↗ ↓ ↑ → ↗ ↖
↑ ↗ ↑ ↗ → ↓ ← ↙ ↖ ↗
↓ ↙ ↙ ↑ ← ↘ ↙ ↓ → ↘
↘ ↙ ↖ ↙ ↗ ↘ ↗ ↘ ↑ ↘
↖ ↑ ↗ → → ↘ → ↘ ↗ ↑
← ↑ ↖ ↖ ↗ → ↘ ↓ ↖ ←
↖ ↓ ← ↓ ↓ ↑ ↖ → ↗ ↗
↘ ↘ ↙ ↘ ↓ ↗ ↖ ↘ ↙ ←
↘ ↖ ↗ ↑ ↗ →
Time taken: 13.92 seconds
```

**Solved puzzle**

This picture won't mean much as the game is about the sequence of moves not the final frame as shown here.

<img src="./images/inertia_solved.png" alt="Inertia solved" width="500">

---

## Guess (Puzzle Type #22)

* [**Play online**](https://www.chiark.greenend.org.uk/~sgtatham/puzzles/js/guess.html)

* [**Instructions**](https://www.chiark.greenend.org.uk/~sgtatham/puzzles/doc/guess.html#guess)

* [**Solver Code**][22]

<details>
  <summary><strong>Rules</strong></summary>
You have a set of coloured pegs, and have to reproduce a predetermined sequence of them (chosen by the computer) within a certain number of guesses.

Each guess gets marked with the number of correctly-coloured pegs in the correct places (in black), and also the number of correctly-coloured pegs in the wrong places (in white). 
</details>


Unlike most other puzzles in this repo, 'Guess' is very different. Similar to minesweeper, Guess is a limited information dynamic puzzle where the next best move depends on information revealed by previous moves (The similarities to minesweeper stop here).

The solver is designed to take the state of the board at any timestep and always gives the next optimal guess. This might seem like an impossible task at first but it's actually not too bad. The optimal guess is defined to be the one that maximizes the Shannon entropy (i.e. maximizes the expected information gain).

The steps below formaly describe the algorithm that is also used in [this amazing 3Blue1Brown video](https://www.youtube.com/watch?v=v68zYyaEmEA) on solving Wordle using information theory. Where 3Blue1Browne describes the same steps below but for a slightly harder problem to solve wordle (a very similar game). The video intuitively justifies this algorithm and builds it from scratch using basic intuition.

To formalize the algorithm, let's first define our three inputs as
- $N :=$ the number of pegs (the length of every guess) 
  - must have $N \geq 1$ and by default $N = 4$ in the game
- $C :=$ the set of possible colors 
  - what actually matters is $|C|$, the number of possible choices for each peg, i.e. the number of colors
  - by default in the game, $C = \{R,Y,G,B,O,P\}$ (six distinct symbols; only $|C|$ matters) for Red, Yellow, Green, Blue, Orange, and Purple.
- $\mathrm{MR} := ((m_1, r_1), (m_2, r_2), ..., (m_k, r_k))$ be the sequence of previous guesses and results where $(m_i, r_i)$ is the previous guess and result at round $i$ and $k\geq 0$ is the number of previous guesses the player has made 
  - Note that $m_i$ has length $N$ and each element is $\in C$ by definition
  - $r_i$ is a triplet of non-negative integers that sum to $N$ by definition. This corresponds to counts of exact-match positions, color-only matches, and non-matches (visualized as black, white, and grey dots)

The algorithm is as follows

1. Define $G$ as the set of every possible guess that can be made

   $$G := \{(c_1, \dots, c_N) \mid \forall i \in \{1, \dots, N\},\ c_i \in C \}$$

    1. Note that $|G| = |C|^N$

    2. Note that $m_i \in G$ for all $i \in \{1, 2, ..., k\}$ by definition.

2. Define $T$ as the set of every possible result triplet 

    $$T := \{(t_1, t_2, t_3) \in \mathbb{N}_0^3 : t_1 + t_2 + t_3 = N\}$$

    1. Note that $r_i \in T$ for all $i \in \{1, 2, ..., k\}$ by definition.
    2. Note that $|T|=\binom{N+2}{2}$ (stars-and-bars)
    3. By default, $N = 4$ in the game so $|T|=15$

3. Define $f : G \times G \to T$ by $f(g_{\text{guess}}, g_{\text{truth}}) = t$ as the result triplet $(t_1, t_2, t_3)$ obtained when guessing $g_{\text{guess}}$ against ground truth $g_{\text{truth}}$. It is trivial to algorithmically make this function which simply counts from $g_1$ and $g_2.$ Look at the function `get_triplets` for a naive implementation of this.

4. Define $S$ as the subset of $G$ that is consistent with the previous guesses $m_i$ and results $r_i$

    $$
    S := \{g \in G : \forall i \in \{1, 2, ..., k\}, f(m_i, g) = r_i\}
    $$
    1. Note that if there aren't previous guesses ($\mathrm{MR} = \emptyset$) then $S = G$
    2. Note that if $S = \emptyset$ then something is wrong with the previous guesses $\mathrm{MR}$ and there is no possible solution to the puzzle. The algorithm stops here and informs the user that the puzzle is unsolvable with the given guesses $\mathrm{MR}$ and that this should never happen unless there is a typo in the guesses $\mathrm{MR}$ (which is usually the case).

5. For each possible guess $g \in G$ and each triplet $t \in T$, count the number of possible solutions $s \in S$ that result in the triplet $t$ when guessing $g$. i.e.

    $$D(g, t) := |\{s \in S: f(g, s) = t\}|$$

6. Calculate the entropy for each possible guess $g \in G$ as the sum of probability times the self-information for every triplet $t \in T$. i.e.

    $$H : G \to \mathbb{R}, \quad H(g) = -\sum_{t \in T} P(t \mid g) \log_2 P(t \mid g)$$

   1. where $P(t \mid g) = \frac{D(g, t)}{|S|}$
   2. By convention, terms with $P(t \mid g)=0$ contribute $0$ to the sum (interpreting $0\log 0 := 0)$.

7. Return the guess $g \in G$ that maximizes the entropy $H(g)$ (to break ties, choose $g$ that is also in $S$ such that it's possibly the correct solution as well, break further ties arbitrarily).
   1. i.e. return any $g^*\in (\mathrm{argmax}_{g\in G}\ H(g) \cap S)$ if exists
   2. otherwise return any $g\in \mathrm{argmax}_{g\in G}\ H(g)$.


If you are at all interested in the above steps and want to understand more, 
I highly recommend watching [this amazing 3Blue1Brown video](https://www.youtube.com/watch?v=v68zYyaEmEA) on solving Wordle using information theory where he describes the same steps but a bits more complicated problem to solve Wordle (a very similar game).

Below is an example of how to utilize the solver while in the middle of a puzzle.

(This is the only solver that under the hood does not utilize any packages besides numpy)

**Unsolved puzzle**

Let's say we start and made two guesses to end up with the following puzzle:

<img src="./images/guess_1.png" alt="Guess Pre Move" width="500">

Code to utilize this package and solve the puzzle:

We encode the puzzle as a Board object then retreive the optimal next guess:
```python
from puzzle_solver import guess_solver as solver
binst = solver.Board()
binst.add_guess(('R', 'Y', 'G', 'B'), (1, 1, 2))  # 1 black dot, 1 white dot, 2 grey dots
binst.add_guess(('R', 'G', 'O', 'P'), (0, 2, 2))  # 0 black dots, 2 white dots, 2 grey dots
binst.best_next_guess()
```

Note: the three numbers in each guess is the result of the guess: (# of black dots, # of white dots, # of grey dots)

Note: by default, the board will have 4 circles and 6 possible colors (R: Red, Y: Yellow, G: Green, B: Blue, O: Orange, P: Purple) but both of these are optional parameters to the Board to change behavior.

**Script Output 1/2**

Note that the output is next optimal guess that has the maximum Shannon entropy.
```
out of 1296 possible ground truths, only 57 are still possible.
max entropy guess is: ['P', 'Y', 'Y', 'G'] with entropy 3.4511
```

So we make our next guess as (Purple, Yellow, Yellow, Green) and let's say we get this result: (2 black, 1 white, 1 grey)

<img src="./images/guess_2.png" alt="Guess Post 1 Move" width="500">

So we input that again to the solver to retreive the next optimal guess:

```python
from puzzle_solver import guess_solver as solver
binst = solver.Board()
binst.add_guess(('R', 'Y', 'G', 'B'), (1, 1, 2))  # 1 black dot, 1 white dot, 2 grey dots
binst.add_guess(('R', 'G', 'O', 'P'), (0, 2, 2))  # 0 black dots, 2 white dots, 2 grey dots
binst.add_guess(('P', 'Y', 'Y', 'G'), (2, 1, 1))  # 2 black dots, 1 white dot, 1 grey dot
binst.best_next_guess()
```

**Script Output 2/2**

```
out of 1296 possible ground truths, only 3 are still possible.
max entropy guess is: ['G', 'Y', 'Y', 'O'] with entropy 1.5850
```

So we make our fourth guess as (Green, Yellow, Yellow, Orange) 

When we input the guess, we see that we correctly solve the puzzle!

<img src="./images/guess_3.png" alt="Guess Post 2 Moves" width="500">

Note that in this case, the correct guess was among multiple possible guesses

In the case when there's only one possible choice left, the solver will inform you that it's the garunteed solution.

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

Each puzzle has its own module which can be imported directly from the repo (i.e. `from puzzle_solver import minesweeper_solver`) or you can run the test scripts directly from the CLI.


Example: Nonograms (Pattern)
Docs: [https://www.chiark.greenend.org.uk/~sgtatham/puzzles/doc/pattern.html#pattern](https://www.chiark.greenend.org.uk/~sgtatham/puzzles/doc/pattern.html#pattern)

```bash
python -m tests.test_nonograms
```

This runs code like:

```python
from puzzle_solver import nonograms_solver as solver
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
binst = solver.Board(top=top_numbers, side=side_numbers)
solutions = binst.solve_and_print()
```

You’ll see the solution grid and status in the terminal.

---

## Why SAT / CP-SAT?

Many pencil puzzles can be modeled with:

- **Boolean decisions** (e.g., black/white, bulb/no-bulb)
- **Linear constraints** (counts, separations, adjacency)
- **All-different / visibility / reachability** constraints

This repo builds those constraints in Python and uses SAT/CP-SAT (e.g., OR-Tools) to search efficiently. It both demonstrates the modeling and provides usable solvers.

---

## What’s Inside

Each sub directory in `src/puzzle_solver/puzzles/` targets a different puzzle type. The following are the sub directories:

* `nonograms` — Picross/Griddlers (run-length constraints). ([Chapter 10][1])
* `sudoku` — Sudoku (rows/cols/blocks all-different). ([Chapter 11][2])
* `minesweeper` — Minesweeper (mines + counts). ([Chapter 12][3])
* `guess` — Guess (similar to wordle, guess the colored circles). ([Chapter 15][22])
* `dominosa` — Dominosa (dominoes + counts). ([Chapter 17][4])
* `light_up` — *Akari* / Light Up (lighting & adjacency). ([Chapter 21][5])
* `map` — Map (region coloring). ([Chapter 22][18])
* `inertia` — Inertia (collect all gems without dying (with least number of moves; my addition)). ([Chapter 24][21])
* `tents` — Tents (tree-tent matching). ([Chapter 25][6])
* `bridges` — Bridges (island connections). ([Chapter 26][20])
* `filling` — Filling (Fillomino-style), region sizes. ([Chapter 29][7])
* `keen` — Keen (arithmetic operations). ([Chapter 30][8])
* `towers` — Skyscrapers (permutation + visibility). ([Chapter 31][9])
* `singles` — Singles (hiding numbers). ([Chapter 32][10])
* `magnets` — Magnets (polarized dominoes + counts). ([Chapter 33][11])
* `signpost` — Signpost (visible dominoes + counts). ([Chapter 34][12])
* `range` — Range (rays & totals). ([Chapter 35][13])
* `pearl` — Pearl (pearl game). ([Chapter 36][19])
* `undead` — UnDead (Vampires/Zombies/Ghosts). ([Chapter 37][14])
* `unruly` — Unruly (no triples + balance). ([Chapter 38][15])
* `tracks` — Tracks (connected components). ([Chapter 40][16])
* `mosaic` — Mosaic (Tapa-like tiling). ([Chapter 42][17])

---

## Testing

To run the tests, simply follow the instructions in Install Python deps section ([here](#1-install-python-deps)) and then run:

```bash
conda activate ./env
pytest
```

the `pytest.ini` file is used to configure the pytest command to use `-n 4` to have 4 workers.

## Contributing

Issues and PRs welcome!


* Python 3.11 recommended but not required.
* Keep puzzle folders self-contained (inputs, solver, simple demo/CLI).
* Prefer small, readable encodings with comments explaining each constraint.
* If you add a new puzzle:

  1. Create a directory in `src/puzzle_solver/puzzles/<name>/`,
  2. Add a minimal test script in `tests/test_<name>.py`,
  3. Document the modeling in code comments,


[1]: https://github.com/Ar-Kareem/puzzle_solver/tree/master/src/puzzle_solver/puzzles/nonograms "puzzle_solver/src/puzzle_solver/puzzles/nonograms at master · Ar-Kareem/puzzle_solver · GitHub"
[2]: https://github.com/Ar-Kareem/puzzle_solver/tree/master/src/puzzle_solver/puzzles/sudoku "puzzle_solver/src/puzzle_solver/puzzles/sudoku at master · Ar-Kareem/puzzle_solver · GitHub"
[3]: https://github.com/Ar-Kareem/puzzle_solver/tree/master/src/puzzle_solver/puzzles/minesweeper "puzzle_solver/src/puzzle_solver/puzzles/minesweeper at master · Ar-Kareem/puzzle_solver · GitHub"
[22]: https://github.com/Ar-Kareem/puzzle_solver/tree/master/src/puzzle_solver/puzzles/guess "puzzle_solver/src/puzzle_solver/puzzles/guess at master · Ar-Kareem/puzzle_solver · GitHub"
[4]: https://github.com/Ar-Kareem/puzzle_solver/tree/master/src/puzzle_solver/puzzles/dominosa "puzzle_solver/src/puzzle_solver/puzzles/dominosa at master · Ar-Kareem/puzzle_solver · GitHub"
[5]: https://github.com/Ar-Kareem/puzzle_solver/tree/master/src/puzzle_solver/puzzles/light_up "puzzle_solver/src/puzzle_solver/puzzles/light_up at master · Ar-Kareem/puzzle_solver · GitHub"
[18]: https://github.com/Ar-Kareem/puzzle_solver/tree/master/src/puzzle_solver/puzzles/map "puzzle_solver/src/puzzle_solver/puzzles/map at master · Ar-Kareem/puzzle_solver · GitHub"
[21]: https://github.com/Ar-Kareem/puzzle_solver/tree/master/src/puzzle_solver/puzzles/inertia "puzzle_solver/src/puzzle_solver/puzzles/inertia at master · Ar-Kareem/puzzle_solver · GitHub"
[6]: https://github.com/Ar-Kareem/puzzle_solver/tree/master/src/puzzle_solver/puzzles/tents "puzzle_solver/src/puzzle_solver/puzzles/tents at master · Ar-Kareem/puzzle_solver · GitHub"
[20]: https://github.com/Ar-Kareem/puzzle_solver/tree/master/src/puzzle_solver/puzzles/bridges "puzzle_solver/src/puzzle_solver/puzzles/bridges at master · Ar-Kareem/puzzle_solver · GitHub"
[7]: https://github.com/Ar-Kareem/puzzle_solver/tree/master/src/puzzle_solver/puzzles/filling "puzzle_solver/src/puzzle_solver/puzzles/filling at master · Ar-Kareem/puzzle_solver · GitHub"
[8]: https://github.com/Ar-Kareem/puzzle_solver/tree/master/src/puzzle_solver/puzzles/keen "puzzle_solver/src/puzzle_solver/puzzles/keen at master · Ar-Kareem/puzzle_solver · GitHub"
[9]: https://github.com/Ar-Kareem/puzzle_solver/tree/master/src/puzzle_solver/puzzles/towers "puzzle_solver/src/puzzle_solver/puzzles/towers at master · Ar-Kareem/puzzle_solver · GitHub"
[10]: https://github.com/Ar-Kareem/puzzle_solver/tree/master/src/puzzle_solver/puzzles/singles "puzzle_solver/src/puzzle_solver/puzzles/singles at master · Ar-Kareem/puzzle_solver · GitHub"
[11]: https://github.com/Ar-Kareem/puzzle_solver/tree/master/src/puzzle_solver/puzzles/magnets "puzzle_solver/src/puzzle_solver/puzzles/magnets at master · Ar-Kareem/puzzle_solver · GitHub"
[12]: https://github.com/Ar-Kareem/puzzle_solver/tree/master/src/puzzle_solver/puzzles/signpost "puzzle_solver/src/puzzle_solver/puzzles/signpost at master · Ar-Kareem/puzzle_solver · GitHub"
[13]: https://github.com/Ar-Kareem/puzzle_solver/tree/master/src/puzzle_solver/puzzles/range "puzzle_solver/src/puzzle_solver/puzzles/range at master · Ar-Kareem/puzzle_solver · GitHub"
[19]: https://github.com/Ar-Kareem/puzzle_solver/tree/master/src/puzzle_solver/puzzles/pearl "puzzle_solver/src/puzzle_solver/puzzles/pearl at master · Ar-Kareem/puzzle_solver · GitHub"
[14]: https://github.com/Ar-Kareem/puzzle_solver/tree/master/src/puzzle_solver/puzzles/undead "puzzle_solver/src/puzzle_solver/puzzles/undead at master · Ar-Kareem/puzzle_solver · GitHub"
[15]: https://github.com/Ar-Kareem/puzzle_solver/tree/master/src/puzzle_solver/puzzles/unruly "puzzle_solver/src/puzzle_solver/puzzles/unruly at master · Ar-Kareem/puzzle_solver · GitHub"
[16]: https://github.com/Ar-Kareem/puzzle_solver/tree/master/src/puzzle_solver/puzzles/tracks "puzzle_solver/src/puzzle_solver/puzzles/tracks at master · Ar-Kareem/puzzle_solver · GitHub"
[17]: https://github.com/Ar-Kareem/puzzle_solver/tree/master/src/puzzle_solver/puzzles/mosaic "puzzle_solver/src/puzzle_solver/puzzles/mosaic at master · Ar-Kareem/puzzle_solver · GitHub"