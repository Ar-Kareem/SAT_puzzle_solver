# Minesweeper (Puzzle Type #3)

This is a dedicated solver for Minesweeper (Called "Mines" in the website)

This Minesweeper solver is a bit different from the other solvers in this repo because Minesweeper is a uniquely different type of puzzle. 

In Minesweeper, you don't solve the puzzle in one go. You need to partially solve the puzzle and get new information to continue. Thus the solver is designed to take the state of the board at any timestep and always gives the most amount of garunteed next steps to take (i.e. garunteed safe positions, garunteed mine positions, and even warns you if you placed a flag in a potentially wrong position).

Then obviously, once the you act upon the guesses and get the new information, you simply put that new info back into the solver and repeat the process until the puzzle is fully solved. 

Below is an example of how to utilize the solver while in the middle of a puzzle. (notice how there's an intentionally placed incorrect flag in the example and the solver will warn you about it)

(The solver under the hood mainly utilizes the CP-SAT solver from Google OR-Tools)

* [**Play online**](https://www.chiark.greenend.org.uk/~sgtatham/puzzles/js/mines.html)

* [**Instructions**](https://www.chiark.greenend.org.uk/~sgtatham/puzzles/doc/mines.html#mines)

You have a grid of covered squares, some of which contain mines, but you don't know which. Your job is to uncover every square which does not contain a mine. If you uncover a square containing a mine, you lose. If you uncover a square which does not contain a mine, you are told how many mines are contained within the eight surrounding squares.

This game needs no introduction; popularised by Windows, it is perhaps the single best known desktop puzzle game in existence.

This version of it has an unusual property. By default, it will generate its mine positions in such a way as to ensure that you never need to guess where a mine is: you will always be able to deduce it somehow. So you will never, as can happen in other versions, get to the last four squares and discover that there are two mines left but you have no way of knowing for sure where they are. 

**Partially solved puzzle**

<img src="../images/minesweeper_pre.png" alt="Minesweeper partially solved" width="500">

Code to utilize this package and solve the puzzle:
```python
import numpy as np
from puzzle_solver import minesweeper_solver as solver
board = np.array([
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
safe_positions, new_garuneed_mine_positions, wrong_flag_positions = solver.give_next_guess(board=board, mine_count=mine_count)
```
**Script Output**

Notice how not only did it output all garunteed new safe and mine positions, it also outputs a warning about the incorrectly placed flag position.

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

<img src="../images/minesweeper_post.png" alt="Minesweeper progressed" width="500">
