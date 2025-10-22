# Black Box (Puzzle Type #34)

* [**Play online**](https://www.chiark.greenend.org.uk/~sgtatham/puzzles/js/blackbox.html)

* [**Instructions**](https://www.chiark.greenend.org.uk/~sgtatham/puzzles/doc/blackbox.html#blackbox)

A number of balls are hidden in a rectangular arena. You have to deduce the positions of the balls by firing lasers positioned at the edges of the arena and observing how their beams are deflected.

Beams will travel straight from their origin until they hit the opposite side of the arena (at which point they emerge), unless affected by balls in one of the following ways:

    A beam that hits a ball head-on is absorbed and will never re-emerge. This includes beams that meet a ball on the first rank of the arena.
    A beam with a ball in its front-left square and no ball ahead of it gets deflected 90 degrees to the right.
    A beam with a ball in its front-right square and no ball ahead of it gets similarly deflected to the left.
    A beam that would re-emerge from its entry location is considered to be ‘reflected’.
    A beam which would get deflected before entering the arena by a ball to the front-left or front-right of its entry point is also considered to be ‘reflected’.

Beams that are reflected appear as a ‘R’; beams that hit balls head-on appear as ‘H’. Otherwise, a number appears at the firing point and the location where the beam emerges (this number is unique to that shot).

You can place guesses as to the location of the balls, based on the entry and exit patterns of the beams; once you have placed enough balls a button appears enabling you to have your guesses checked.

Here is a diagram showing how the positions of balls can create each of the beam behaviours shown above:

      1 R H R - - - -  
    | . . O . O . . . |
    2 . . . . . . . . 3
    | . . . . . . . . |
    | . . . . . . . . |
    3 . . . . . . . . |
    | . . . . . . O . |
    H . . . . . . . . |
    | . . . . . O . . |
      1 2 - R R - - - 

As shown, it is possible for a beam to receive multiple reflections before re-emerging (see turn 3). Similarly, a beam may be reflected (possibly more than once) before receiving a hit (the ‘H’ on the left side of the example).

Note that any layout with more than 4 balls may have a non-unique solution. The following diagram illustrates this; if you know the board contains 5 balls, it is impossible to determine where the fifth ball is (possible positions marked with an x):

      - - - - - - - -  
    | . . . . . . . . |
    | . . . . . . . . |
    | . . O . . O . . |
    | . . . x x . . . |
    | . . . x x . . . |
    | . . O . . O . . |
    | . . . . . . . . |
    | . . . . . . . . |
      - - - - - - - - 

For this reason, when you have your guesses checked, the game will check that your solution produces the same results as the computer's, rather than that your solution is identical to the computer's. So in the above example, you could put the fifth ball at any of the locations marked with an x, and you would still win.

Note: This puzzle is one of the very rare puzzles where CP-SAT is not a good fit because for every placement of the balls the state of the beams is dynamically changes and thus required a lot of variables to construct and constraint. This is why the resulting model is large and slow.

**Unsolved puzzle**

<img src="https://raw.githubusercontent.com/Ar-Kareem/puzzle_solver/master/images/black_box_unsolved.png" alt="Black Box unsolved" width="500">

Code to utilize this package and solve the puzzle:
```python
from puzzle_solver import black_box_solver as solver
top = ['1', 'H', 'R', 'R', 'H', 'R', '2', '3']
left = ['H', '1', 'H', '7', '5', '6', 'H', 'H']
right = ['2', 'H', '4', 'H', '5', '6', 'H', 'H'] 
bottom = ['7', 'R', 'H', 'R', 'H', 'R', '4', '3']

# create board and solve; ball count if between 3 and 6
binst = solver.Board(top=top, left=left, bottom=bottom, right=right, ball_count=(3, 6))
solutions = binst.solve_and_print()
```
**Script Output**
```python
Solution found
[[' ' ' ' ' ' ' ' 'O' ' ' ' ' ' ']
 [' ' ' ' ' ' ' ' ' ' 'O' ' ' ' ']
 [' ' 'O' ' ' ' ' ' ' ' ' ' ' ' ']
 [' ' ' ' ' ' ' ' ' ' ' ' ' ' ' ']
 [' ' ' ' ' ' ' ' ' ' ' ' ' ' ' ']
 [' ' ' ' ' ' ' ' ' ' ' ' ' ' ' ']
 [' ' ' ' ' ' ' ' ' ' ' ' ' ' ' ']
 [' ' ' ' 'O' ' ' 'O' ' ' ' ' ' ']]
Solution found
[[' ' ' ' ' ' ' ' 'O' ' ' ' ' ' ']
 [' ' ' ' ' ' ' ' ' ' 'O' ' ' ' ']
 [' ' 'O' ' ' 'O' ' ' ' ' ' ' ' ']
 [' ' ' ' ' ' ' ' ' ' ' ' ' ' ' ']
 [' ' ' ' ' ' ' ' ' ' ' ' ' ' ' ']
 [' ' ' ' ' ' ' ' ' ' ' ' ' ' ' ']
 [' ' ' ' ' ' ' ' ' ' ' ' ' ' ' ']
 [' ' ' ' 'O' ' ' 'O' ' ' ' ' ' ']]
Solutions found: 2
status: OPTIMAL
Time taken: 30.33 seconds
```

**Solved puzzle**

<img src="https://raw.githubusercontent.com/Ar-Kareem/puzzle_solver/master/images/black_box_solved.png" alt="Black Box solved" width="500">
